from aweber_tools import App, AppException
from future.builtins.misc import input

try:
    app = App('config.cfg')
    app.run()
except AppException as exception:
    print(str(exception))
    input('Press any key to exit..')