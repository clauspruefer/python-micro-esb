service_metadata1 = {
    'SYSServiceID': 'insertUserDomain',
    'data': [
        {
            'User':
            {
                'SYSServiceMethod': 'init',
                'name': 'testuser1',
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

service_metadata2 = {
    'SYSServiceID': 'insertUserDomain',
    'data': [
        {
            'User':
            {
                'SYSServiceMethod': 'init',
                'name': 'testuser1',
                'Domain': {
                    'SYSServiceMethod': 'add',
                    'name': 'testdomain2',
                    'ending': 'de',
                    'Host': [
                        {
                            'SYSServiceMethod': 'add',
                            'name': 'bla01',
                            'type': 'A',
                            'value': '2.37.51.21',
                            'ttl': 36000
                        },
                        {
                            'SYSServiceMethod': 'add',
                            'name': 'bla02',
                            'type': 'A',
                            'value': '2.37.51.21',
                            'ttl': 36000
                        }
                    ]
                }
            }
        }
    ]
}

service_metadata3 = {
    'SYSServiceID': 'insertUserDomain',
    'data': [
        {
            'User':
            {
                'SYSServiceMethod': 'init',
                'name': 'testuser1',
                'Domain': {
                    'SYSServiceMethod': 'add',
                    'name': 'ola-amigos',
                    'ending': 'org',
                    'Host': [
                        {
                            'SYSServiceMethod': 'add',
                            'name': 'amigo1',
                            'type': 'A',
                            'value': '145.20.83.4'
                        },
                        {
                            'SYSServiceMethod': 'add',
                            'name': 'amigo2',
                            'type': 'A',
                            'value': '145.20.83.5'
                        }
                    ]
                }
            }
        }
    ]
}
