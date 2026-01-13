# ]*[ --------------------------------------------------------------------- ]*[
#  .                    Micro ESB Test Classes Module                        .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Copyright Claus Prüfer (2016 - 2026)                                   .
#  .                                                                         .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

from microesb import microesb


class Cert(microesb.ClassHandler):
    """ Certificate handler class.

    Base class for certificate types (CA, Server, Client).
    """


class CertCA(Cert):
    """ Certificate Authority handler class.

    Handles CA certificate instances.
    """
    def __init__(self):
        """
        :ivar str type: certificate type identifier
        """
        self.type = 'ca'
        super().__init__()


class CertServer(Cert):
    """ Server certificate handler class.

    Handles server certificate instances.
    """
    def __init__(self):
        """
        :ivar str type: certificate type identifier
        """
        self.type = 'server'
        super().__init__()


class CertClient(Cert):
    """ Client certificate handler class.

    Handles client certificate instances.
    """
    def __init__(self):
        """
        :ivar str type: certificate type identifier
        """
        self.type = 'client'
        super().__init__()


class Smartcard(microesb.ClassHandler):
    """ Smartcard handler class.

    Handles smartcard instances for certificate storage.
    """
    def __init__(self):
        super().__init__()


class SmartcardContainer(microesb.ClassHandler):
    """ Smartcard container handler class.

    Handles smartcard container instances for key pair storage.
    """
    def __init__(self):
        super().__init__()


class Shipment(microesb.ClassHandler):
    """ Shipment handler class.

    Handles shipment instances.
    """
    def __init__(self):
        super().__init__()


class Palette(microesb.MultiClassHandler):
    """ Palette handler class.

    Handles multiple palette instances using MultiClassHandler.
    """
    def __init__(self):
        super().__init__()
