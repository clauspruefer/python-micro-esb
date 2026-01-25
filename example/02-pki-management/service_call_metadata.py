service_metadata_ca = {
    'SYSServiceID': 'generateCertCA',
    'data': [
        {
            'SYSBackendMethod': { 'CertCA': 'gen_cert' },
            'CertCA': {
                'id': 'test-ca1',
                'Smartcard': {
                    'label': 'smartcard_ca_card',
                    'user_pin': 'pin1',
                    'SmartcardContainer': {
                        'label': 'keypair_ca1'
                    }
                },
                'country': 'DE',
                'state': 'Berlin',
                'locality': 'Berlin',
                'org': 'WEBcodeX',
                'org_unit': 'Security',
                'common_name': 'testca@domain.com',
                'email': 'pki@webcodex.de',
                'valid_days': 365
            }
        }
    ]
}

service_metadata_server = {
    'SYSServiceID': 'generateCertServer',
    'data': [
        {
            'SYSBackendMethod': { 'CertServer': 'gen_cert' },
            'CertServer': {
                'id': 'test-server1',
                'CertCA': {
                    'id': 'test-ca1'
                },
                'Smartcard': {
                    'label': 'smartcard_customer1',
                    'user_pin': 'pin2',
                    'SmartcardContainer': {
                        'label': 'testserver1_keypair'
                    }
                },
                'country': 'DE',
                'state': 'Berlin',
                'locality': 'Berlin',
                'org': 'WEBcodeX',
                'org_unit': 'Security',
                'common_name': 'testserver@domain.com',
                'email': 'pki@webcodex.de',
                'valid_days': 365
            }
        }
    ]
}

service_metadata_client = {
    'SYSServiceID': 'generateCertClient',
    'data': [
        {
            'SYSBackendMethod': { 'CertClient': 'gen_cert' },
            'CertClient': {
                'id': 'test-client1',
                'CertCA': {
                    'id': 'test-ca1'
                },
                'CertServer': {
                    'id': 'test-server1'
                },
                'Smartcard': {
                    'label': 'smartcard_customer1',
                    'user_pin': 'pin2',
                    'SmartcardContainer': {
                        'label': 'testserver1_client1_keypair'
                    }
                },
                'country': 'DE',
                'state': 'Berlin',
                'locality': 'Berlin',
                'org': 'WEBcodeX',
                'org_unit': 'Security',
                'common_name': 'testclient1@domain.com',
                'email': 'pki@webcodex.de',
                'valid_days': 365
            }
        }
    ]
}
