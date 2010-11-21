isotoma.plone.defang
====================

This package provides a console_script entry point for buildout, to help with "defanging" of Data.fs files.

Defanging (& refanging)
-----------------------

When you run separate production and staging/test/dev environments you often have to transfer data between them.  This might be for testing, debugging, pre-launch content staging or whatever.

When you do this you often have to obliterate or obscure production data, such as passwords, before you can commission the database in the other environment.  We call this process "defanging" - pulling the dangerous "fangs" of the Database.

In reverse if you are providing a pre-launch content staging environment and then you wish to copy the Data.fs to production then you need to "refang" the database - put in production passwords and whatever other production data is required or operation.

Using the package
-----------------

When installed using buildout the package will create a script `defang` in the bin directory of your buildout.

You can then run the script, and it will:

 1. copy the Data.fs files you specify to new temporary names
 2. defang them, using the fangs you specify in the configuration
 3. rename the temporary file to Data.fs.defanged (based on the input filenames)

Refanging works in the same way, except you run `defang --refang`.

Configuration
-------------

The package should be installed using a `zc.buildout.egg` stanza in buildout.  Here is an example of it's use::

    [defang]
    recipe = zc.recipe.egg
    eggs = 
        isotoma.plone.defang
        ${buildout:eggs}
    extra-paths = 
        ${zope:location}/lib/python
        ${instance:location}
        ${productdistros:location}
    scripts = defang
    arguments =
        fangs = {
            "${buildout:directory}/var/filestorage/Data.fs": [
                isotoma.plone.defang.UserFang('/acl_users/admin:admin')
        ],
        productdistros="${productdistros:location}",
        instance="${instance:location}",
        zconfig="${instance:location}/etc/zope.conf"

fangs
~~~~~

The fangs argument is a dictionary of lists, keyed on the full paths to Data.fs files.  This allows you to specify defanging of multiple files, if you use them.  I've not tested it with more than a single Data.fs file.

Your configuration should look something like::

    fangs = {
        "${buildout:directory}/var/filestorage/Data.fs": [
            # FANGS
        ],
    }

For the list of available fangs, and how to write your own fangs, see below.

Fangs
-----

The package comes with knowledge of (currently) two different kinds of "fangs":

 UserFang
  A user who needs a password changing when migrating environments
 ArchetypesFieldFang
  A field on an archetypes object that needs to be changed when migrating environments

UserFang
~~~~~~~~

This accepts as an initialisation one or more strings that indicate users who you wish to reset, and the passwords on "safe" environments (which are presumed to be behind firewalls etc.)

For example::

    isotoma.plone.defang.UserFang('/acl_users/admin:admin')

Specifies that you wish to reset the "admin" user's password in the root acl_users.

You can have multiple acl_users and users::


    isotoma.plone.defang.UserFang(
        '/acl_users/admin:admin',
        '/portal/acl_users/manager:password'
    )

Refanging users
###############

When the UserFang is run in refanging mode it will prompt on the console for the live passwords.

ArchetypesFieldFang
~~~~~~~~~~~~~~~~~~~

This is used to execute an Archetypes mutator when defanging/refanging.  You provide the name of the mutator to call and the safe and live values::

    ArchetypesFieldFang('portal.foo.bar.setThing', "safe_value", "live_value")

Writing your own Fangs
----------------------

Fangs are referred to using the full package path in the buildout configuration.  You can therefore provide your own fangs in your own packages, as long as these packages are available on the python path.

Your fang should be a class that has these two methods::

    class ExampleFang:

        def defang(self, app):
            """ Perform defanging on app """

        def refang(self, app):
            """ Perform refanging on app """

`app` is an object just like the app object you get in zope debug mode. 

You should be careful about what you do in your class initialisation - at this point Zope does not yet exist - postpone imports or method calls to Zopeish things until the defang/refang methods.


