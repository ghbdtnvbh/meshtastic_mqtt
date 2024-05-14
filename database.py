from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, create_engine, DateTime

Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer, primary_key=True)
    node_id = Column(String, unique=True)
    longname = Column(String)
    shortname = Column(String)
    hardware_id = Column(Integer)
    inserted_at = Column(DateTime, default=datetime.now)


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    altitude = Column(Integer, nullable=True)
    lat_lon = Column(String)
    rssi = Column(Integer)
    snr = Column(Float)
    inserted_at = Column(DateTime, default=datetime.now)

class Telemetry(Base):
    __tablename__ = 'telemetries'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    battery_level = Column(Integer)
    voltage = Column(Float)
    channel_utilization = Column(Float, nullable=True)
    air_util_tx = Column(Float)
    snr = Column(Float)
    rssi = Column(Integer)
    inserted_at = Column(DateTime, default=datetime.now)


engine = create_engine('postgresql://pi:pi@localhost/meshtastic')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def node_exists(node_id):
    node = session.query(Node).filter_by(node_id=node_id).first()
    return node is not None

def add_node(node_id, longname, shortname, hardware):
    user = Node(node_id=node_id,
                longname=longname,
                shortname=shortname,
                hardware_id=hardware
    )
    session.add(user)
    session.commit()

def add_position(user_id, altitude, lat_lon, rssi, snr):
    position = Position(user_id=user_id, altitude=altitude, lat_lon=lat_lon, rssi=rssi, snr=snr)
    session.add(position)
    session.commit()

def add_telemetry(user_id, battery_level, voltage, air_util_tx, channel_utilization, snr, rssi):
    telemetry = Telemetry(user_id=user_id, 
                          battery_level=battery_level,
                          voltage=voltage,  
                          air_util_tx = air_util_tx,
                          channel_utilization=channel_utilization, 
                          snr = snr,
                          rssi = rssi
    )
    session.add(telemetry)
    session.commit()
