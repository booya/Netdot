from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Engine = create_engine('mysql+pymysql://netdot:netdot@10.242.89.51/netdot')
Session = sessionmaker(bind=Engine)

#class IPBlock(Base):
#    __tablename__ = 'ipblock'
#    id = Column(Integer, primary_key=True)
#    address = Column(Integer)
#    description = Column(String(128))
#    prefix = Column(Integer)
#    version = Column(Integer)
#
#    def __repr__(self):
#        return "IPBlock {}/{}".format(self.address, self.prefix)

