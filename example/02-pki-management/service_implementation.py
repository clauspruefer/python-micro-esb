import abc
import logging
import datetime

from microesb import microesb

logger = logging.getLogger(__name__)


class Cert(microesb.ClassHandler, metaclass=abc.ABCMeta):

    def __init__(self):
        super().__init__()

        self._register_property(
            'generation_timestamp',
            {
                'type': 'str',
                'default': None,
                'required': False,
                'description': 'SysInternal Certificate Generation Date'
            }
        )

        self._register_property(
            'cert_data',
            {
                'type': 'str',
                'default': None,
                'required': False,
                'description': 'SysInternal Generated Certificate Base64 encoded'
            }
        )

    @abc.abstractmethod
    def _load_ref_cert_data(self):
        """ Abstract _load_ref_cert_data() method.
        """

    @abc.abstractmethod
    def _gen_openssl_cert(self):
        """ Abstract _gen_openssl_cert() method.
        """

    @abc.abstractmethod
    def _store_cert_data(self):
        """ Abstract _store_cert_data() method.
        """

    def gen_cert(self):

        self._load_ref_cert_data()

        if getattr(self, 'Smartcard') is not None:
            logger.info('Gen HSM Keypair')
            self._hsm_gen_keypair()
        if getattr(self, 'Smartcard') is None:
            logger.info('Gen OpenSSL PrivKey')
            self._gen_openssl_privkey()

        self._gen_openssl_cert()
        self.generation_timestamp = datetime.datetime.now().isoformat('T')
        self._store_cert_data()

    def _gen_openssl_privkey(self):
        logger.info('Gen openssl private key.')

    def _get_cert_data_by_id(self):
        logger.info('Get cert data from ESB. Type:{}.'.format(self.type))
        self.set_properties(
            self._ServiceRouter.send('CertGetById', metadata=self.id)
        )

    def _hsm_gen_keypair(self):
        logger.info('Smartcard container label:{}'.format(
            self.Smartcard.SmartcardContainer.label)
        )
        self.Smartcard.gen_keypair()

    def _store_cert_data(self):
        logger.info('Store {} cert metadata.'.format(self.type))
        self.json_transform()
        self._ServiceRouter.send('CertStore', metadata=self.json_dict)


class CertCA(Cert):

    def __init__(self):
        self.type = 'ca'
        super().__init__()

    def _load_ref_cert_data(self):
        pass

    def _gen_openssl_cert(self):
        logger.info('Generating {} cert.'.format(self.type))

        self.json_transform()

        srv_metadata = {
            "CertCA": self.json_dict
        }

        self.cert_data = 'dummy_cacert_data'
        logger.info('Generating cert with metadata:{}'.format(self.json))


class CertServer(Cert):

    def __init__(self):
        self.type = 'server'
        super().__init__()

    def _load_ref_cert_data(self):
        self.CertCA._get_cert_data_by_id()

    def _gen_openssl_cert(self):
        logger.info('Generating {} cert.'.format(self.type))

        self.json_transform()

        srv_metadata = {
            "CertServer": self.json_dict,
            "CertCA": self.CertCA.json_dict
        }

        logger.info('Generating cert with metadata:{}'.format(srv_metadata))

        self.cert_data = 'dummy_servercert_data'


class CertClient(Cert):

    def __init__(self):
        self.type = 'client'
        super().__init__()

    def _load_ref_cert_data(self):
        self.CertCA._get_cert_data_by_id()
        self.CertServer._get_cert_data_by_id()

    def _gen_openssl_cert(self):
        logger.info('Route {} cert gen request (rel to CA and Server) to ESB external service.'.format(self.type))

        self.json_transform()

        srv_metadata = {
            "CertClient": self.json,
            "CertServer": self.CertServer.json,
            "CertCA": self.CertCA.json
        }

        logger.info('Generating cert with metadata:{}'.format(srv_metadata))
        self.cert_data = 'dummy_clientcert_data'


class Smartcard(microesb.ClassHandler):

    def __init__(self):
        super().__init__()

        self._register_property(
            'gen_status',
            {
                'type': bool,
                'default': False,
                'required': False,
                'description': 'SysInternal Generated Smartcard Keypair Status'
            }
        )

    def gen_keypair(self):
        logger.info('Gen keypair on smartcard:{} with keypair label:{}'.format(
            self.label,
            self.SmartcardContainer.label
        ))

        srv_metadata = {
            "SmartcardID": self.label,
            "SmartcardContainerLabel": self.SmartcardContainer.label
        }

        self.gen_status = self._ServiceRouter.send('KeypairGenerate', metadata=srv_metadata)


class SmartcardContainer(microesb.ClassHandler):

    def __init__(self):
        super().__init__()
