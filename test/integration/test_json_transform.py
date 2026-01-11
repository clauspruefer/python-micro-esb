import pytest

from microesb import microesb


@pytest.fixture
def config_class_listobject():
    config = {
        'class_mapping': {
            'Shipment': 'Shipment',
            'Palette': 'Palette',
        },
        'class_reference': {
            'Shipment': {
                'property_ref': 'Shipment',
                'children': {
                    'Palette': {
                        'property_ref': 'Palette',
                    }
                }
            }
        }
    }
    return config


@pytest.fixture
def config_properties_listobject():
    config = {
        'Shipment': {
            'properties': {
                'id': {
                    'type': 'int',
                    'default': None,
                    'required': True,
                    'description': '',
                }
            }
        },
        'Palette': {
            'properties': {
                'id': {
                    'type': 'str',
                    'default': None,
                    'required': True,
                    'description': '',
                },
                'label': {
                    'type': 'str',
                    'default': None,
                    'required': True,
                    'description': '',
                }
            }
        }
    }
    return config


@pytest.fixture
def config_service_listobject():
    config = {
        'id': 'processScan',
        'data': [
            {
                'Shipment': {
                    'id': 'testshipment1',
                    'Palette': [
                        {
                            'id': 1,
                            'label': 'label1',
                        },
                        {
                            'id': 2,
                            'label': 'label2',
                        }
                    ]
                }
            }
        ]
    }
    return config


@pytest.fixture
def config_class_pki_service():
    config = {
        'class_mapping': {
            'CertCA': 'CertCA',
            'SmartcardCA': 'Smartcard',
            'SmartcardREQ': 'Smartcard',
            'SmartcardContainer': 'SmartcardContainer'
        },
        'class_reference': {
            'CertCA': {
                'property_ref': 'Cert',
                'children': {
                    'SmartcardCA': {
                        'property_ref': 'Smartcard',
                        'children': {
                            'SmartcardContainer': {'property_ref': 'SmartcardContainer'}
                        }
                    },
                    'SmartcardREQ': {
                        'property_ref': 'Smartcard',
                        'children': {
                            'SmartcardContainer': {'property_ref': 'SmartcardContainer'}
                        }
                    }
                }
            }
        }
    }
    return config


@pytest.fixture
def config_properties_pki_service():
    config = {
        'Cert': {
            'properties': {
                'id': {
                    'type': 'str',
                    'default': None,
                    'required': True,
                    'description': '',
                },
                'country': {
                    'type': 'str',
                    'default': 'DE',
                    'required': True,
                    'description': '',
                }
            }
        },
        'Smartcard': {
            'properties': {
                'label': {
                    'type': 'str',
                    'default': None,
                    'required': True,
                    'description': '',
                }
            }
        },
        'SmartcardContainer': {
            'properties': {
                'label': {
                    'type': 'str',
                    'default': None,
                    'required': True,
                    'description': '',
                }
            }
        }
    }
    return config


@pytest.fixture
def config_service_pki():
    config = {
        'id': 'addCACertificate',
        'data': [
            {
                'CertCA': {
                    'id': 'testid1',
                    'country': 'DE',
                    'state': 'Berlin',
                    'locality': 'Berlin',
                    'org': 'WEBcodeX',
                    'org_unit': 'Security',
                    'common_name': 'testcn1',
                    'email': 'pki@webcodex.de',
                    'valid_days': 365,
                    'key_ref': 'Smartcard',
                    'SmartcardCA': {
                        'label': 'label1',
                        'user_pin': 'pin1',
                        'SmartcardContainer': {
                            'label': 'container_label1'
                        }
                    },
                    'SmartcardREQ': {
                        'label': 'label2',
                        'user_pin': 'pin2',
                        'SmartcardContainer': {
                            'label': 'container_label2'
                        }
                    }
                }
            }
        ]
    }
    return config


class TestJSONTransform:

    def test_transform_pki(
            self,
            config_class_pki_service,
            config_properties_pki_service,
            config_service_pki
        ):

        class_mapper = microesb.ClassMapper(
            class_references=config_class_pki_service['class_reference'],
            class_mappings=config_class_pki_service['class_mapping'],
            class_properties=config_properties_pki_service
        )

        r = microesb.ServiceExecuter().execute_get_hierarchy(
            class_mapper=class_mapper,
            service_data=config_service_pki
        )

        root_object = r[0]['CertCA']['object_instance']

        assert root_object.json_dict == {
            'CertCA': {
                'id': 'testid1',
                'country': 'DE',
                'state': 'Berlin',
                'locality': 'Berlin',
                'org': 'WEBcodeX',
                'org_unit': 'Security',
                'common_name': 'testcn1',
                'email': 'pki@webcodex.de',
                'valid_days': 365,
                'key_ref': 'Smartcard',
                'SmartcardCA': {
                    'label': 'label1',
                    'user_pin': 'pin1',
                    'SmartcardContainer': {
                        'label': 'container_label1'
                    }
                },
                'SmartcardREQ': {
                    'label': 'label2',
                    'user_pin': 'pin2',
                    'SmartcardContainer': {
                        'label': 'container_label2'
                    }
                }
            }
        }
