service_metadata = {
    'SYSServiceID': 'insertUserDomain',
    'data': [
        {
            'User':
            {
                'SYSServiceMethod': 'init',
                'name': 'testuser1',
                'dbcon': None,
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
                            'name': 'host1',
                            'type': 'A',
                            'value': '5.44.111.165',
                            'ttl': 36000
                        }
                    ]
                }
            }
        }
    ]
}
