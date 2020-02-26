import sys

from pyojo.tools.shell import init_app_shell

import app

init_app_shell()

sys.exit(app.Application(sys.argv).run())
