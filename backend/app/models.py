from sqlalchemy import Column, Integer, Float, String, Date, Index
from sqlalchemy.orm import relationship
from .db import Base

class Profile(Base):
	__tablename__ = 'profiles'

	id = Column(Integer, primary_key=True, index=True)
	float_id = Column(String, index=True)
	latitude = Column(Float, index=True)
	longitude = Column(Float, index=True)
	depth = Column(Float)
	temperature = Column(Float)
	salinity = Column(Float)
	month = Column(Integer, index=True)
	year = Column(Integer, index=True)
	date = Column(Date, nullable=True)

	__table_args__ = (
		Index('idx_profiles_lat_lon', 'latitude', 'longitude'),
	)
