service_properties = {
    'Cert': {
        'properties': {
            'id': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Textual cert database id'
            },
            'country': {
                'type': 'str',
                'default': 'DE',
                'required': True,
                'description': 'Certificate country ref'
            },
            'state': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Certificate state ref'
            },
            'locality': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Certificate locality ref'
            },
            'org': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Certificate organization ref'
            },
            'org_unit': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Certificate organization unit ref'
            },
            'common_name': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Certificate common name'
            },
            'email': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Certificate email ref'
            },
            'valid_days': {
                'type': 'int',
                'default': 365,
                'required': True,
                'description': 'Certificate validity range in days'
            }
        },
        'methods': ['gen_cert']
    },
    'Smartcard': {
        'properties': {
            'label': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Smartcard textual label'
            },
            'user_pin': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Smartcard pin'
            }
        }
    },
    'SmartcardContainer': {
        'properties': {
            'label': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Container object on smartcards textual label'
            }
        }
    }
}
