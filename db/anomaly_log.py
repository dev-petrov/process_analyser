from sqlalchemy import Column, DateTime, Integer, String

from db.base import Base


class AnomalyLog(Base):
    __tablename__ = "anomaly_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dttm = Column(DateTime)
    reason = Column(String)
