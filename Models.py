from Netdot import Base

from sqlalchemy import Column, Integer, String
from ipcalc import Network

class IPBlock(Base):
    __tablename__ = 'ipblock'
    id = Column(Integer, primary_key=True)
    address = Column(Integer)
    description = Column(String(128))
    prefix = Column(Integer)
    version = Column(Integer)

    def __repr__(self):
        return "IPBlock {}/{}".format(Network(self.address), self.prefix)

