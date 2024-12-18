service_properties = {
    'User': {
        'properties': {
            'name': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Textual UserID'
            }
        }
    },
    'Domain': {
        'properties': {
            'name': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Domain Name'
            },
            'ending': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Domain Ending'
            }
        }
    },
    'Host': {
        'properties': {
            'type': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'DNS Type'
            },
            'value': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'DNS Value'
            },
            'ttl': {
                'type': 'int',
                'default': 3600,
                'required': False,
                'description': 'DNS Time To Live'
            },
            'priority': {
                'type': 'int',
                'default': None,
                'required': False,
                'description': 'MX Type Priority'
            }
        }
    }
}
