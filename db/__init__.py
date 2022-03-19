from sqlalchemy import (
    create_engine,
    Column, 
    Integer, 
    DateTime,
    String,
    Float,
)
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///anomaly.db')
Base = declarative_base()

class RawValue(Base):
    __tablename__ = 'raw_values'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dttm = Column(DateTime) 
    pid = Column(Integer)
    name = Column(String(512))
    username = Column(String(256))
    ppid = Column(Integer, nullable=True)
    parent_name = Column(String(512), nullable=True)
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    num_threads = Column(Integer) 
    terminal = Column(String(512))
    nice = Column(Integer)
    cmdline = Column(String)
    exe = Column(String)
    status = Column(String(64))
    create_time = Column(DateTime)
    connections = Column(Integer) 
    open_files = Column(Integer)


class AnomalyLog(Base):
    __tablename__ = 'anomaly_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dttm = Column(DateTime)
    reason = Column(String)

Base.metadata.create_all(engine)
