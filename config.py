import os


class DB:
    def __init__(self):
        db = self
        db.host = os.getenv('DB_HOST') or "127.0.0.1"
        db.port = os.getenv('DB_PORT') or "5432"
        db.user = os.getenv('DB_USER') or "postgres"
        db.pswd = os.getenv('DB_PASS') or ""
    
    def print(self,db_name:str="postgres"):
        db = self
        return f'postgresql://{db.user}:{db.pswd}@{db.host}:{db.port}/{db_name}'
