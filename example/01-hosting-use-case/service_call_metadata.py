service_metadata = {
    'SYSServiceID': 'insertUserDomain',
    'data': [
        {
            'User':
            {
                'id': 'testuser1',
                'Domain': {
                    'SYSServiceMethod': 'add',
                    'name': 'testdomain1',
                    'ending': 'com',
                    'Host': [
                        {
                            'SYSServiceMethod': 'add',
                            'type': 'MX',
                            'value': 'mx01.mailserver.com',
                            'priority': 1
                        },
                        {
                            'SYSServiceMethod': 'add',
                            'type': 'A',
                            'value': 'host1',
                            'ttl': 36000
                        }
                    ]
                }
            }
        }
    ]
}
