from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseRawValue(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    dttm = Column(DateTime, index=True)
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
