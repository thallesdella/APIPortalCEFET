from apicefet.models import Model


class Jwk(Model):
    def __init__(self):
        Model.__init__(self, 'secret_key')

    def bootstrap(self, secret):
        return self.loads({'secret': secret})
