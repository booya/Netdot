from Netdot import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table, Boolean, DateTime
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
    parent_id = Column('parent', Integer, ForeignKey('ipblock.id'))
    parent = relationship('IPBlock', remote_side=[id])
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


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)

    aliases = Column(String(255))
    sysname = Column(String(255))
    sysdescription = Column(String(255))
    syslocation = Column(String(255))
    os = Column(String(128))
    info = Column(Text)

    # Management
    customer_managed = Column(Boolean)
    auto_dns = Column(Boolean)
    canautoupdate = Column(Boolean)
    date_installed = Column(DateTime)
    last_updated = Column(DateTime)
    oobname = Column(String(255))
    oobnumber = Column(String(32))
    oobname_2 = Column(String(255))
    oobnumber_2 = Column(String(32))
    power_outlet = Column(String(255))
    power_outlet_2 = Column(String(255))
    extension = Column(Integer)

    # Monitoring
    monitored = Column(Boolean)
    monitoring_template = Column(String(255))
    monitoring_path_cost = Column(Integer)
    monitor_config = Column(Boolean)
    monitor_config_group = Column(String(64))
    down_from = Column(DateTime)
    down_until = Column(DateTime)
    monitorstatus = Column(Integer)

    # Network related
    layers = Column(String(8))
    ipforwarding = Column(Boolean)
    collect_arp = Column(Boolean)
    collect_fwt = Column(Boolean)
    collect_stp = Column(Boolean)
    last_arp = Column(DateTime)
    last_fwt = Column(DateTime)
    bgpid = Column(String(64))
    bgplocalas = Column(Integer)
    stp_enabled = Column(Boolean)
    stp_mst_digest = Column(String(255))
    stp_mst_region = Column(String(128))
    stp_mst_rev = Column(Integer)
    stp_type = Column(String(128))

    # SNMP
    snmp_polling = Column(Boolean)
    snmp_managed = Column(Boolean)
    snmp_community = Column('community', String(64))
    snmp_version = Column(Integer)
    snmp_bulk = Column(Boolean)
    snmp_conn_attempts = Column(Integer)
    snmp_down = Column(Boolean)
    snmp_target = Column(Integer)
    snmp_authkey = Column(String(255))
    snmp_authprotocol = Column(String(32))
    snmp_privkey = Column(String(255))
    snmp_privprotocol = Column(String(32))
    snmp_securitylevel = Column(String(32))
    snmp_securityname = Column(String(255))

    # Foreign tables
    site_id = Column('site', Integer, ForeignKey('site.id'))
    site = relationship(Site, primaryjoin=site_id == Site.id)

    owner_id = Column('owner', Integer, ForeignKey('entity.id'))
    owner = relationship(Entity, primaryjoin=owner_id == Entity.id)

    usedby_id = Column('used_by', Integer, ForeignKey('entity.id'))
    user = relationship(Entity, primaryjoin=usedby_id == Entity.id)

    host_device_id = Column('host_device', Integer, ForeignKey('device.id'))
    host_device = relationship('Device', remote_side=[id])

    name_id = Column('name', Integer)
    # name = relationship()

    #asset_id = Column(Integer)
    #asset = relationship()
    #type = router
    #room
    #rack

    def __repr__(self):
        return 'Device {}'.format(self.sysname)

    def is_virtual(self):
        if self.host_device_id:
            return True


class Interface(Base):
    __tablename__ = 'interface'
    id = Column(Integer, primary_key=True)

    admin_duplex = Column(String(16))
    admin_status = Column(String(16))
    auto_dns = Column(Boolean)
    bpdu_filter_enabled = Column(Boolean)
    bpdu_guard_enabled = Column(Boolean)
    circuit = Column(Integer)
    contactlist = Column(Integer)
    description = Column(String(128))
    dlci = Column(String(64))
    doc_status = Column(String(32))
    down_from = Column(DateTime)
    down_until = Column(DateTime)
    dp_remote_id = Column(String(128))
    dp_remote_ip = Column(String(128))
    dp_remote_port = Column(String(128))
    dp_remote_type = Column(String(255))
    ignore_ip = Column(Boolean)
    info = Column(Text)
    jack = Column(Integer)
    jack_char = Column(String(32))
    loop_guard_enabled = Column(Boolean)
    monitored = Column(Boolean)
    monitorstatus = Column(Integer)
    name = Column(String(255))
    neighbor_fixed = Column(Boolean)
    neighbor_missed = Column(Integer)
    number = Column(String(64))
    oper_duplex = Column(String(16))
    oper_status = Column(String(16))
    overwrite_descr = Column(Boolean)
    physaddr = Column(Integer)
    room_char = Column(String(32))
    root_guard_enabled = Column(Boolean)
    snmp_managed = Column(Boolean)
    speed = Column(Integer)
    stp_id = Column(String(32))
    type = Column(String(32))

    # Foreign Associations
    device_id = Column('device', Integer, ForeignKey('device.id'))
    device = relationship(Device, primaryjoin=device_id == Device.id,
                          backref='interfaces')

    neighbor = Column(Integer)

    def __repr__(self):
        return self.name


# Association Tables
SiteSubnet = Table('sitesubnet', Base.metadata,
                   Column('site', Integer, ForeignKey('site.id')),
                   Column('subnet', Integer, ForeignKey('ipblock.id')))

EntityRoles = Table('entityrole', Base.metadata,
                    Column('entity', Integer, ForeignKey('entity.id')),
                    Column('type', Integer, ForeignKey('entitytype.id')))
