from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Engine = create_engine('mysql+pymysql://netdot:netdot@192.168.1.242/netdot')
Session = sessionmaker(bind=Engine)
