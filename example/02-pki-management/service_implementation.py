import abc

from microesb import microesb


class Cert(microesb.ClassHandler):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def _load_ref_cert_data(self):
        """ Abstract _load_ref_cert_data() method.
        """

    @abc.abstractmethod
    def _gen_openssl_cert(self):
        """ Abstract _gen_openssl_cert() method.
        """

    @abc.abstractmethod
    def _insert_cert_db_data(self):
        """ Abstract _insert_cert_db_data() method.
        """

    def gen_cert(self):

        self._load_ref_cert_data()

        if getattr(self, 'Smartcard') is not None:
            self._hsm_gen_keypair()
        else:
            self._gen_openssl_privkey()

        self._gen_openssl_cert()
        self._insert_cert_db_data()

    def _gen_openssl_privkey(self):
        print('Gen openssl private key.')

    def _get_cert_dbdata_by_id(self):
        print('Get cert data from db. Type: {}.'.format(self.type))

    def _hsm_gen_keypair(self):
        print('Smartcard container label:{}'.format(
            self.Smartcard.SmartcardContainer.label)
        )
        self.Smartcard.gen_keypair()


class CertCA(Cert):
    def __init__(self):
        self.type = 'ca'
        super().__init__()

    def _load_ref_cert_data(self):
        pass

    def _gen_openssl_cert(self):
        print('Gen openssl cert type:{}.'.format(self.type))

    def _insert_cert_db_data(self):
        print('Insert cert data type:{} into db.'.format(self.type))


class CertServer(Cert):
    def __init__(self):
        self.type = 'server'
        super().__init__()

    def _load_ref_cert_data(self):
        self.CertCA._get_cert_dbdata_by_id()

    def _gen_openssl_cert(self):
        print('Gen openssl cert type:{}, rel to CA.'.format(self.type))

    def _insert_cert_db_data(self):
        print('Insert cert data type:{} into db.'.format(self.type))


class CertClient(Cert):
    def __init__(self):
        self.type = 'client'
        super().__init__()

    def _load_ref_cert_data(self):
        self.CertCA._get_cert_dbdata_by_id()
        self.CertServer._get_cert_dbdata_by_id()

    def _gen_openssl_cert(self):
        print('Gen openssl cert type:{}, rel to cCA and cServer.'.format(self.type))

    def _insert_cert_db_data(self):
        print('Insert cert data type:{} into db.'.format(self.type))


class Smartcard(microesb.ClassHandler):
    def __init__(self):
        super().__init__()

    def gen_keypair(self):
        print('Gen keypair on smartcard:{} with keypair label:{}'.format(
            self.label,
            self.SmartcardContainer.label
        ))


class SmartcardContainer(microesb.ClassHandler):
    def __init__(self):
        super().__init__()
