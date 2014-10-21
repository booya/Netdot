from Netdot import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship, backref, reconstructor
from netaddr import IPAddress, IPNetwork

class EntityType(Base):
    __tablename__ = 'entitytype'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    def __repr__(self):
        return self.name


class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    short_name = Column(String(64))
    aliases = Column(String(255))
    asname = Column(String(32))
    asnumber = Column(Integer)
    oid = Column(String(32))
    info = Column(Text)

    roles = relationship(EntityType,
                         secondary='entityrole',
                         backref='entities')

    def __repr__(self):
        return self.name

    def has_role(self, role):
        for r in self.roles:
            if r.name == role:
                return True


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
    prefix = Column(Integer)
    version = Column(Integer)
    status = Column(Integer, ForeignKey('ipblockstatus.id'))
    blocktype = relationship('IPBlockStatus', backref=backref('IPBlockStatus'))

    # asn = Column(Integer)
    description = Column(String(128))
    info = Column(Text)

    owner_id = Column('owner', Integer, ForeignKey('entity.id'))
    owner = relationship(Entity, primaryjoin=owner_id == Entity.id)
    usedby_id = Column('used_by', Integer, ForeignKey('entity.id'))
    usedby = relationship(Entity, primaryjoin=usedby_id == Entity.id)

    # This doesn't get run when creating objects from the database.
    # see init_on_load below.
    def __init__(self, address, prefix, version, blocktype, asn, description,
                 info, owner, usedby):
        print str(address)
        self.network = IPAddress(int(address))
        self.prefix = prefix
        self.cidr = IPNetwork('{}/{}'.format(self.network, self.prefix))
        self.version = version
        self.blocktype = blocktype
        self.asn = asn
        self.description = description
        self.info = info
        self.owner = owner.name
        self.usedby = usedby.name

    @reconstructor
    def init_on_load(self):
        self.network = IPAddress(int(self.address)).format()
        self.cidr = '{}/{}'.format(self.network, self.prefix)

    def __repr__(self):
        return self.cidr


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    siteid = Column('number', String(64))
    aliases = Column(String(255))
    info = Column(Text)

    street1 = Column(String(128))
    street2 = Column(String(128))
    pobox = Column(String(32))
    city = Column(String(64))
    state = Column(String(32))
    country = Column(String(64))
    postcode = Column('zip', String(16))

    subnets = relationship(IPBlock,
                           secondary='sitesubnet',
                           backref='sites')

    def __repr__(self):
        return 'Site {}'.format(self.aliases)

# Association Tables
SiteSubnet = Table('sitesubnet', Base.metadata,
                   Column('site', Integer, ForeignKey('site.id')),
                   Column('subnet', Integer, ForeignKey('ipblock.id')))

EntityRoles = Table('entityrole', Base.metadata,
                    Column('entity', Integer, ForeignKey('entity.id')),
                    Column('type', Integer, ForeignKey('entitytype.id')))
