from datetime import datetime
from sqlalchemy.orm import Session
from db import AnomalyLog, engine

class BaseAnomalyLogger:

    def get_message(self, data):
        return str(data)
    
    def log(self, data):
        self._log(self.get_message(data))

    def _log(self, log_data):
        raise NotImplementedError()

class FileAnomalyLogger(BaseAnomalyLogger):

    def __init__(self, file_name):
        if not file_name:
            file_name = 'anomaly_logger.log'
        self.file_name = file_name
    
    def _log(self, log_data):
        with open(self.file_name, 'a') as file:
            file.write(log_data)
        
    def __str__(self):
        return f"FileAnomalyLogger, filename: {self.filename}"

class DataBaseAnomalyLogger(BaseAnomalyLogger):
    def _log(self, log_data):
        with Session(engine) as session, session.begin():
            session.add(
                AnomalyLog(
                    dttm=datetime.now(),
                    reason=log_data,
                )
            )

    def __str__(self):
        return "DataBaseAnomalyLogger"

class ConsoleAnomalyLogger(BaseAnomalyLogger):
    def _log(self, log_data):
        print(log_data)

    def __str__(self):
        return "ConsoleAnomalyLogger"
