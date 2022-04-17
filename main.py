from detector import Detector
from detector.db import Base, Session, get_engine

if __name__ == "__main__":
    engine = get_engine()
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

    detector = Detector()
    detector.execute()
