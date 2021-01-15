from server import app

from server.resources.routes import *

if __name__ == '__main__':
    app.run('0.0.0.0', 5468)
