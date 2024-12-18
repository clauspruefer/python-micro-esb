from microesb import microesb


class Cert(microesb.ClassHandler):
    pass


class CertCA(Cert):
    def __init__(self):
        self.type = 'ca'
        super().__init__()


class CertServer(Cert):
    def __init__(self):
        self.type = 'server'
        super().__init__()


class CertClient(Cert):
    def __init__(self):
        self.type = 'client'
        super().__init__()


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
        super().__init__()
