class Config(object):
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 5000
    DEBUG = False
    TESTING = False
    DB_SERVER = '127.0.0.1'

    @property
    def DATABASE_URI(self):
        return 'mysql://user@{}/foo'.format(self.DB_SERVER)
