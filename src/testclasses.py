# application classes used by unit tests

from microesb import handler
from microesb import microesb


class Cert(microesb.ClassHandler):
    pass


class CertCA(Cert):
    def __init__(self):
        self.type = 'ca'
        super().__init__()


class CertServer(Cert):
    def __init__(self):
        super().__init__()
        self.type = 'server'


class CertClient(Cert):
    def __init__(self):
        super().__init__()
        self.type = 'client'


class Smartcard(microesb.ClassHandler):
    def __init__(self):
        super().__init__()


class SmartcardContainer(microesb.ClassHandler):
    def __init__(self):
        super().__init__()


class Shipment(microesb.ClassHandler):
    def __init__(self):
        super().__init__()


class Palette(microesb.MultiClassHandler):
    def __init__(self):
        # self.service_id = 'test'
        self.retry_count = 1
        super().__init__()
