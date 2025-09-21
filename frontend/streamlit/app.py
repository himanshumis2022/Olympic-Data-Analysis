import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import numpy as np
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="FloatChat Analytics Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def fetch_data(endpoint, params=None):
    """Fetch data from API with caching"""
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🌊 FloatChat Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("🔧 Controls")
    
    # Data filters
    st.sidebar.subheader("📊 Data Filters")
    
    # Depth range
    depth_range = st.sidebar.slider(
        "Depth Range (m)",
        min_value=0,
        max_value=1000,
        value=(0, 500),
        step=10
    )
    
    # Temperature range
    temp_range = st.sidebar.slider(
        "Temperature Range (°C)",
        min_value=-5.0,
        max_value=35.0,
        value=(-2.0, 30.0),
        step=0.5
    )
    
    # Salinity range
    salinity_range = st.sidebar.slider(
        "Salinity Range (PSU)",
        min_value=30.0,
        max_value=40.0,
        value=(32.0, 38.0),
        step=0.1
    )
    
    # Geographic bounds
    st.sidebar.subheader("🗺️ Geographic Bounds")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        lat_min = st.number_input("Min Latitude", value=-90.0, min_value=-90.0, max_value=90.0)
        lon_min = st.number_input("Min Longitude", value=-180.0, min_value=-180.0, max_value=180.0)
    
    with col2:
        lat_max = st.number_input("Max Latitude", value=90.0, min_value=-90.0, max_value=90.0)
        lon_max = st.number_input("Max Longitude", value=180.0, min_value=-180.0, max_value=180.0)
    
    # Main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", "🗺️ Geographic Analysis", "📊 Depth Profiles", 
        "🔍 Advanced Analytics", "📤 Data Export"
    ])
    
    with tab1:
        show_overview(depth_range, temp_range, salinity_range, lat_min, lat_max, lon_min, lon_max)
    
    with tab2:
        show_geographic_analysis(depth_range, temp_range, salinity_range, lat_min, lat_max, lon_min, lon_max)
    
    with tab3:
        show_depth_profiles(depth_range, temp_range, salinity_range, lat_min, lat_max, lon_min, lon_max)
    
    with tab4:
        show_advanced_analytics()
    
    with tab5:
        show_data_export(depth_range, temp_range, salinity_range, lat_min, lat_max, lon_min, lon_max)

def show_overview(depth_range, temp_range, salinity_range, lat_min, lat_max, lon_min, lon_max):
    """Show overview statistics and charts"""
    st.header("📈 Data Overview")
    
    # Fetch data with filters
    params = {
        'depth_min': depth_range[0],
        'depth_max': depth_range[1],
        'temp_min': temp_range[0],
        'temp_max': temp_range[1],
        'salinity_min': salinity_range[0],
        'salinity_max': salinity_range[1],
        'lat_min': lat_min,
        'lat_max': lat_max,
        'lon_min': lon_min,
        'lon_max': lon_max,
        'limit': 1000
    }
    
    data = fetch_data("/data/profiles", params)
    if not data:
        st.error("Failed to load data")
        return
    
    profiles = data.get('results', [])
    if not profiles:
        st.warning("No data found with current filters")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(profiles)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Profiles", f"{len(df):,}")
    
    with col2:
        avg_temp = df['temperature'].mean()
        st.metric("Avg Temperature", f"{avg_temp:.2f}°C")
    
    with col3:
        avg_salinity = df['salinity'].mean()
        st.metric("Avg Salinity", f"{avg_salinity:.2f} PSU")
    
    with col4:
        depth_range_actual = f"{df['depth'].min():.0f}-{df['depth'].max():.0f}m"
        st.metric("Depth Range", depth_range_actual)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature distribution
        fig_temp = px.histogram(
            df, x='temperature', 
            title="Temperature Distribution",
            nbins=30,
            color_discrete_sequence=['#1f77b4']
        )
        fig_temp.update_layout(showlegend=False)
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Salinity distribution
        fig_salinity = px.histogram(
            df, x='salinity', 
            title="Salinity Distribution",
            nbins=30,
            color_discrete_sequence=['#ff7f0e']
        )
        fig_salinity.update_layout(showlegend=False)
        st.plotly_chart(fig_salinity, use_container_width=True)
    
    # Temperature vs Salinity scatter
    fig_scatter = px.scatter(
        df, x='temperature', y='salinity',
        color='depth',
        title="Temperature vs Salinity (colored by depth)",
        labels={'temperature': 'Temperature (°C)', 'salinity': 'Salinity (PSU)'},
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

def show_geographic_analysis(depth_range, temp_range, salinity_range, lat_min, lat_max, lon_min, lon_max):
    """Show geographic analysis"""
    st.header("🗺️ Geographic Analysis")
    
    # Fetch geographic distribution
    geo_data = fetch_data("/data/analytics/geographic-distribution", {'grid_size': 5.0})
    if not geo_data:
        st.error("Failed to load geographic data")
        return
    
    distribution = geo_data.get('distribution', [])
    if not distribution:
        st.warning("No geographic data available")
        return
    
    df_geo = pd.DataFrame(distribution)
    
    # World map
    fig_map = px.scatter_mapbox(
        df_geo,
        lat="latitude",
        lon="longitude",
        size="count",
        color="avg_temperature",
        hover_data=["avg_salinity", "count"],
        color_continuous_scale="Viridis",
        mapbox_style="open-street-map",
        title="ARGO Float Distribution (colored by temperature)",
        zoom=1
    )
    fig_map.update_layout(height=600)
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Geographic statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Geographic Coverage")
        st.write(f"**Grid Cells:** {len(df_geo)}")
        st.write(f"**Latitude Range:** {df_geo['latitude'].min():.1f}° to {df_geo['latitude'].max():.1f}°")
        st.write(f"**Longitude Range:** {df_geo['longitude'].min():.1f}° to {df_geo['longitude'].max():.1f}°")
    
    with col2:
        st.subheader("Data Density")
        st.write(f"**Max Profiles per Cell:** {df_geo['count'].max()}")
        st.write(f"**Avg Profiles per Cell:** {df_geo['count'].mean():.1f}")
        st.write(f"**Total Profiles:** {df_geo['count'].sum()}")

def show_depth_profiles(depth_range, temp_range, salinity_range, lat_min, lat_max, lon_min, lon_max):
    """Show depth profile analysis"""
    st.header("📊 Depth Profile Analysis")
    
    # Fetch depth profile data
    depth_data = fetch_data("/data/analytics/depth-profiles", {
        'depth_min': depth_range[0],
        'depth_max': depth_range[1]
    })
    if not depth_data:
        st.error("Failed to load depth profile data")
        return
    
    depths = depth_data.get('depths', [])
    temperatures = depth_data.get('temperatures', [])
    salinities = depth_data.get('salinities', [])
    
    if not depths:
        st.warning("No depth profile data available")
        return
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Temperature Profile", "Salinity Profile"),
        horizontal_spacing=0.1
    )
    
    # Temperature profile
    fig.add_trace(
        go.Scatter(
            x=temperatures, y=depths,
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6)
        ),
        row=1, col=1
    )
    
    # Salinity profile
    fig.add_trace(
        go.Scatter(
            x=salinities, y=depths,
            mode='lines+markers',
            name='Salinity',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=6)
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=500,
        showlegend=False,
        title="Depth Profiles"
    )
    
    # Update axes
    fig.update_xaxes(title_text="Temperature (°C)", row=1, col=1)
    fig.update_xaxes(title_text="Salinity (PSU)", row=1, col=2)
    fig.update_yaxes(title_text="Depth (m)", row=1, col=1)
    fig.update_yaxes(title_text="Depth (m)", row=1, col=2)
    
    # Reverse y-axis for depth (deeper = lower on chart)
    fig.update_yaxes(autorange="reversed")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Depth distribution
    depth_dist = fetch_data("/data/analytics/depth-distribution")
    if depth_dist and 'distribution' in depth_dist:
        df_depth = pd.DataFrame(depth_dist['distribution'])
        
        fig_depth_dist = px.bar(
            df_depth, x='depth', y='count',
            title="Profile Count by Depth",
            color='count',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_depth_dist, use_container_width=True)

def show_advanced_analytics():
    """Show advanced analytics"""
    st.header("🔍 Advanced Analytics")
    
    # Correlation analysis
    st.subheader("Temperature-Salinity Correlation")
    corr_data = fetch_data("/data/analytics/correlation")
    if corr_data:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Correlation Coefficient", f"{corr_data.get('correlation', 0):.4f}")
        with col2:
            st.metric("R² Value", f"{corr_data.get('r_squared', 0):.4f}")
    
    # Outlier analysis
    st.subheader("Outlier Detection")
    outlier_data = fetch_data("/data/analytics/outliers", {'threshold': 2.0})
    if outlier_data:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temperature Outliers", outlier_data.get('temperature_outliers', []).__len__())
        with col2:
            st.metric("Salinity Outliers", outlier_data.get('salinity_outliers', []).__len__())
    
    # Temporal analysis
    st.subheader("Temporal Analysis")
    temporal_data = fetch_data("/data/analytics/temporal")
    if temporal_data and 'monthly' in temporal_data:
        df_monthly = pd.DataFrame(temporal_data['monthly'])
        
        fig_monthly = px.line(
            df_monthly, x='month', y='count',
            title="Profile Count by Month",
            markers=True
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

def show_data_export(depth_range, temp_range, salinity_range, lat_min, lat_max, lon_min, lon_max):
    """Show data export options"""
    st.header("📤 Data Export")
    
    st.info("Export filtered data in various formats")
    
    # Export parameters
    export_params = {
        'depth_min': depth_range[0],
        'depth_max': depth_range[1],
        'temp_min': temp_range[0],
        'temp_max': temp_range[1],
        'salinity_min': salinity_range[0],
        'salinity_max': salinity_range[1],
        'lat_min': lat_min,
        'lat_max': lat_max,
        'lon_min': lon_min,
        'lon_max': lon_max
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export CSV", type="primary"):
            try:
                response = requests.get(f"{API_URL}/data/export/csv", params=export_params)
                if response.status_code == 200:
                    st.download_button(
                        label="Download CSV",
                        data=response.content,
                        file_name=f"floatchat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("Export failed")
            except Exception as e:
                st.error(f"Export error: {str(e)}")
    
    with col2:
        if st.button("📝 Export ASCII"):
            try:
                response = requests.get(f"{API_URL}/data/export/ascii", params=export_params)
                if response.status_code == 200:
                    st.download_button(
                        label="Download ASCII",
                        data=response.content,
                        file_name=f"floatchat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Export failed")
            except Exception as e:
                st.error(f"Export error: {str(e)}")
    
    with col3:
        if st.button("📋 Export JSON"):
            try:
                response = requests.get(f"{API_URL}/data/export/json", params=export_params)
                if response.status_code == 200:
                    st.download_button(
                        label="Download JSON",
                        data=response.content,
                        file_name=f"floatchat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    st.error("Export failed")
            except Exception as e:
                st.error(f"Export error: {str(e)}")
    
    # Export summary
    st.subheader("Export Summary")
    st.write(f"**Filters Applied:**")
    st.write(f"- Depth: {depth_range[0]}m to {depth_range[1]}m")
    st.write(f"- Temperature: {temp_range[0]}°C to {temp_range[1]}°C")
    st.write(f"- Salinity: {salinity_range[0]} PSU to {salinity_range[1]} PSU")
    st.write(f"- Latitude: {lat_min}° to {lat_max}°")
    st.write(f"- Longitude: {lon_min}° to {lon_max}°")

if __name__ == "__main__":
    main()