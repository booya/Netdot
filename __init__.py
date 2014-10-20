from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Engine = create_engine('mysql+pymysql://netdot:netdot@10.242.89.51/netdot')
Session = sessionmaker(bind=Engine)
