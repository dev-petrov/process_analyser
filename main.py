from detector import Detector
from sqlalchemy import create_engine

from db import Base, Session
from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

if __name__ == "__main__":
    engine = create_engine(
        "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            DB_USER,
            DB_PASSWORD,
            DB_HOST,
            DB_PORT,
            DB_NAME,
        )
    )
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

    detector = Detector()
    detector.execute()
