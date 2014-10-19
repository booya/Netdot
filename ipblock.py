from Netdot import Session
from Netdot.Models import IPBlock

def listall():
    sess = Session()
    for ipblock in sess.query(IPBlock).all():
        yield ipblock
    sess.close()

