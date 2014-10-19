from Netdot import Session
from Netdot.Models import IPBlock

def listall():
    sess = Session()
    for ipblock in sess.query(IPBlock).order_by(IPBlock.address):
        yield ipblock
    sess.close()

