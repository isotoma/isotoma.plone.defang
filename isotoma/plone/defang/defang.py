import os
from ZODB import FileStorage, DB
import transaction

def defang_acl_users(acl_users):
    print acl_users

def opendb(zodbfile):
    if not os.path.exists(zodbfile):
        raise OSError("%s does not exist" % zodbfile)
    storage = FileStorage.FileStorage(zodbfile)
    db = DB(storage)
    conn = db.open()
    dbroot = conn.root()
    app = dbroot['Application']
    return app

def defang(fangs, zodbfile):
    app = opendb(zodbfile)
    tx = transaction.begin()
    for f in fangs:
        f.defang(app)
    transaction.commit()

def refang(fangs, zodbfile):
    app = opendb(zodbfile)
    tx = transaction.begin()
    for f in fangs:
        f.refang(app)
    transaction.commit()
