
import defang
import os
import optparse
import Products
import Globals
import shutil
import traceback
import sys

from fangs import *

import App.config
from Zope2.Startup import zopectl
from Zope2.Startup.handlers import root_handler

usage = "%prog [options] zodbfile"

def initialize_zope(instance, zconfig, productdistros):
    """ This is about 85% evil (+/- 10%). We set up enough of zope's insane startup
    process that we can access all our Python and unpickle stuff, but not so
    much that it opens the ZODB. """
    if productdistros is not None:
        ppath = Products.__path__[:]
        ppath.append(productdistros)
        Products.__path__ = ppath
    Globals.INSTANCE_HOME = instance
    options = zopectl.ZopeCtlOptions()
    options.configfile = zconfig
    sys.argv = sys.argv[:1]
    options.realize()
    root_handler(options.configroot) # wild guess
    App.config.setConfiguration(options.configroot)

def main(instance, zconfig, fangs, productdistros=None):
    """ productdistros should be the full path to the location of additional products to be loaded """
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-r", "--refang", action="store_true", help="refang, don't defang", default=False)
    opts, args = parser.parse_args()
    initialize_zope(instance, zconfig, productdistros)
    for zodbfile, file_fangs in fangs.items():
        if opts.refang:
            output = zodbfile + ".refanged"
        else:
            output = zodbfile + ".defanged"
        tmp = os.path.join(os.path.dirname(output), "." + os.path.basename(output))
        print "Copying", zodbfile, "to", tmp
        shutil.copy(zodbfile, tmp)
        try:
            if opts.refang:
                print "Refanging", tmp
                defang.refang(file_fangs, tmp)
            else:
                print "Defanging", tmp
                defang.defang(file_fangs, tmp)
            print "Renaming", tmp, "to", output
            os.rename(tmp, output)
        except Exception, e:
            traceback.print_exc()
            sys.exit(-1)

