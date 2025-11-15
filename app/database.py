from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://aiquest_mppx_user:gCSo3ckjyZEzokLooTdeClRprRRMjB3m@dpg-d4cgk0mr433s73dhlp1g-a/aiquest_mppx'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
     db = SesionLocal()
     try:
          yield db
     finally:
          db.close()