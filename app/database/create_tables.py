import sys
from os import path
from sqlalchemy import create_engine

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(base_dir)
from app.common.constants import DB
from app.database.models import Base

def create_table():
    engine = create_engine(DB.db_url)
    Base.metadata.create_all(bind=engine)
    
if __name__=="__main__":
    create_table()