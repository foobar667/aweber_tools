from aweber_tools import App, AppException

try:
    app = App('config/config.cfg')
    app.run()
except AppException as exception:
    print(str(exception))