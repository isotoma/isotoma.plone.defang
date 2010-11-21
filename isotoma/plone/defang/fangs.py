import os
import sys
import util
import getpass

class UserFang(object):

    ignore = False
    verbose = False

    def __init__(self, *users):
        self.users = users

    def split(self, app, userpath):
        parts = userpath.split("/")
        username = parts[-1]
        path = parts[:-1]
        if path[0] == '':
            path = path[1:]
        acl_users = util.unrestrictedTraverse(app, path)
        if ':' in username:
            username, password = username.split(":", 1)
        else:
            password = "password"
        return acl_users, username, password

    def change_password(self, acl_users, user, password):
        """ The wild and whacky world of Plone. Try lots of ways of changing
        the password to accommodate the complete lack of a coherent interface
        on user management. """
        from Products.PlonePAS.interfaces.plugins import IUserManagement
        userid = user.getId()
        modified = False
        try:
            managers = acl_users.plugins.listPlugins(IUserManagement)
        except KeyError:
            pass
        else:
            for mid, manager in managers:
                try:
                    manager.doChangeUser(userid, password)
                except RuntimeError:
                    pass
                else:
                    modified = True
            if modified:
                return
        if hasattr(user, 'changePassword'):
            user.changePassword(password)
        else:
            acl_users.users.updateUserPassword(userid, password)

    def defang(self, app):
        print "Defanging users"
        for userpath in self.users:
            acl_users, username, password = self.split(app, userpath)
            user = acl_users.getUserById(username)
            self.change_password(acl_users, user, password)
            print user, "defanged"

    def refang(self, app):
        # unbuffer stdout so getpass works
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
        print "Refanging users"
        for userpath in self.users:
            acl_users, username, safe_password = self.split(app, userpath)
            user = acl_users.getUserById(username)
            password = getpass.getpass("Please enter the live password for '%s':" % username)
            self.change_password(acl_users, user, password)
            print user, "refanged"

class ArchetypesFieldFang(object):

    def __init__(self, mutator, safe, live):
        parts = mutator.split(".")
        self.mutator = parts[-1]
        self.path = parts[:-1]
        self.safe = safe
        self.live = live

    def imports(self):
        """ We need to do this as late as possible, to ensure Products has
        been correctly set up. """
        from Products.Archetypes.Schema.factory import instanceSchemaFactory
        from zope import component
        component.provideAdapter(instanceSchemaFactory)

    def defang(self, app):
        self.imports()
        obj = util.unrestrictedTraverse(app, self.path)
        mutator = getattr(obj, self.mutator)
        mutator(self.safe)

    def refang(self, app):
        self.imports()
        obj = util.unrestrictedTraverse(app, self.path)
        mutator = getattr(obj, self.mutator)
        mutator(self.live)
