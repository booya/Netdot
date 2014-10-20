from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Netdot.config import DBENGINE, DBUSER, DBPASS, DBHOST, DBNAME

Base = declarative_base()
Engine = create_engine('{}://{}:{}@{}/{}'.format(DBENGINE, DBUSER, DBPASS, DBHOST, DBNAME))
Session = sessionmaker(bind=Engine)
