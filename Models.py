from Netdot import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from netaddr import IPAddress, IPNetwork

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    short_name = Column(String(64))
    aliases = Column(String(255))
    asname = Column(String(32))
    asnumber = Column(Integer)
    oid = Column(String(32))

    #ipblocks = relationship('IPBlock', backref=backref('IPBlock'))
    #ipblocks = relationship('IPBlock', foreign_keys='[IPBlock.owner]')

    def __repr__(self):
        return self.name

class IPBlockStatus(Base):
    __tablename__ = 'ipblockstatus'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    
    def __repr__(self):
        return self.name

class IPBlock(Base):
    __tablename__ = 'ipblock'
    id = Column(Integer, primary_key=True)
    address = Column(Integer)
    description = Column(String(128))
    prefix = Column(Integer)
    version = Column(Integer)
    status = Column(Integer, ForeignKey('ipblockstatus.id'))
    blocktype = relationship('IPBlockStatus', backref=backref('IPBlockStatus'))

    asn = Column(Integer)
    description = Column(String(128))
    info = Column(String)

    owner_id = Column('owner', Integer, ForeignKey('entity.id'))
    owner = relationship(Entity, primaryjoin=owner_id == Entity.id)
    usedby_id = Column('used_by', Integer, ForeignKey('entity.id'))
    usedby = relationship(Entity, primaryjoin=usedby_id == Entity.id)

    def __init__(self):
        self.network = IPAddress(int(self.address))
        self.cidr = IPNetwork('{}/{}'.format(self.network, self.prefix))

    def __repr__(self):
        #self.network = IPNetwork('{}/{}'.format(IPAddress(int(self.address)), self.prefix))
        return self.cidr

