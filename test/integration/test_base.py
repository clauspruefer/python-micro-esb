import pytest

from microesb import microesb


@pytest.fixture
def config_class_multiobject():
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
def config_properties_multiobject():
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
def config_service_multiobject():
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
def config_class_extended_service():
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
def config_properties_extended_service():
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
def config_service_extended_service():
    config = {
        'id': 'addCACertificate',
        'global': {
            'CertCA': {
                'FipsMode': False
            }
        },
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


class TestMapping:

    def test_class_mapping(self, config_class_extended_service, config_properties_extended_service):

        i = microesb.ClassMapper(
            class_references=config_class_extended_service['class_reference'],
            class_mappings=config_class_extended_service['class_mapping'],
            class_properties=config_properties_extended_service
        )

        cert_ca = getattr(i, 'CertCA')
        smartcard_ca = getattr(cert_ca, 'SmartcardCA')
        smartcard_container_ca = getattr(smartcard_ca, 'SmartcardContainer')
        smartcard_req = getattr(cert_ca, 'SmartcardREQ')
        smartcard_container_req = getattr(smartcard_req, 'SmartcardContainer')

        assert getattr(cert_ca, 'id') is None
        assert getattr(smartcard_ca, 'label') is None
        assert getattr(smartcard_req, 'label') is None
        assert getattr(smartcard_container_ca, 'label') is None
        assert getattr(smartcard_container_req, 'label') is None

    def test_service_mapping(
        self,
        config_service_extended_service,
        config_class_extended_service,
        config_properties_extended_service
    ):

        class_mapper = microesb.ClassMapper(
            class_references=config_class_extended_service['class_reference'],
            class_mappings=config_class_extended_service['class_mapping'],
            class_properties=config_properties_extended_service
        )

        s = microesb.ServiceExecuter().execute(
            class_mapper=class_mapper,
            service_data=config_service_extended_service
        )

        cert_ca = getattr(s[0]._class_mapper, 'CertCA')
        smartcard_ca = getattr(cert_ca, 'SmartcardCA')
        smartcard_container_ca = getattr(smartcard_ca, 'SmartcardContainer')
        smartcard_req = getattr(cert_ca, 'SmartcardREQ')
        smartcard_container_req = getattr(smartcard_req, 'SmartcardContainer')

        assert getattr(cert_ca, 'id') == 'testid1'
        assert getattr(smartcard_ca, 'label') == 'label1'
        assert getattr(smartcard_req, 'label') == 'label2'
        assert getattr(smartcard_container_ca, 'label') == 'container_label1'
        assert getattr(smartcard_container_req, 'label') == 'container_label2'

    def test_multi_item_object(
        self,
        config_service_multiobject,
        config_class_multiobject,
        config_properties_multiobject
    ):

        class_mapper = microesb.ClassMapper(
            class_references=config_class_multiobject['class_reference'],
            class_mappings=config_class_multiobject['class_mapping'],
            class_properties=config_properties_multiobject
        )

        s = microesb.ServiceExecuter().execute(
            class_mapper=class_mapper,
            service_data=config_service_multiobject
        )

        shipment = getattr(s[0]._class_mapper, 'Shipment')
        palette = getattr(shipment, 'Palette')

        p1 = palette._object_container[0]
        p2 = palette._object_container[1]

        assert getattr(p1, 'id') == 1
        assert getattr(p1, 'label') == 'label1'
        assert getattr(p2, 'id') == 2
        assert getattr(p2, 'label') == 'label2'

        shipment.json_transform()
        assert shipment.json_dict == {
            'id': 'testshipment1',
            'SYSServiceMethod': None,
            'Palette': [
                {'id': 1, 'label': 'label1'},
                {'id': 2, 'label': 'label2'}
            ]
        }

    def test_recursive_multi_item_object(self):
        """Test nested MultiClassHandler: Shipment -> Palette (multi) -> Box (multi)"""
        
        config_class = {
            'class_mapping': {
                'Shipment': 'Shipment',
                'Palette': 'Palette',
                'Box': 'Box',
            },
            'class_reference': {
                'Shipment': {
                    'property_ref': 'Shipment',
                    'children': {
                        'Palette': {
                            'property_ref': 'Palette',
                            'children': {
                                'Box': {
                                    'property_ref': 'Box',
                                }
                            }
                        }
                    }
                }
            }
        }
        
        config_properties = {
            'Shipment': {
                'properties': {
                    'id': {
                        'type': 'str',
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
                    'weight': {
                        'type': 'int',
                        'default': None,
                        'required': False,
                        'description': '',
                    }
                }
            },
            'Box': {
                'properties': {
                    'id': {
                        'type': 'str',
                        'default': None,
                        'required': True,
                        'description': '',
                    },
                    'contents': {
                        'type': 'str',
                        'default': None,
                        'required': False,
                        'description': '',
                    }
                }
            }
        }
        
        config_service = {
            'id': 'processShipment',
            'data': [
                {
                    'Shipment': {
                        'id': 'ship-001',
                        'Palette': [
                            {
                                'id': 'pal-001',
                                'weight': 100,
                                'Box': [
                                    {'id': 'box-001', 'contents': 'electronics'},
                                    {'id': 'box-002', 'contents': 'books'},
                                ]
                            },
                            {
                                'id': 'pal-002',
                                'weight': 150,
                                'Box': [
                                    {'id': 'box-003', 'contents': 'furniture'},
                                ]
                            }
                        ]
                    }
                }
            ]
        }
        
        class_mapper = microesb.ClassMapper(
            class_references=config_class['class_reference'],
            class_mappings=config_class['class_mapping'],
            class_properties=config_properties
        )
        
        s = microesb.ServiceExecuter().execute(
            class_mapper=class_mapper,
            service_data=config_service
        )
        
        shipment = getattr(s[0]._class_mapper, 'Shipment')
        palette = getattr(shipment, 'Palette')
        
        # Check first palette
        p1 = palette._object_container[0]
        assert getattr(p1, 'id') == 'pal-001'
        assert getattr(p1, 'weight') == 100
        
        # Check first palette's boxes
        p1_box = getattr(p1, 'Box')
        assert hasattr(p1_box, '_object_container')
        assert len(p1_box._object_container) == 2
        
        p1_b1 = p1_box._object_container[0]
        p1_b2 = p1_box._object_container[1]
        assert getattr(p1_b1, 'id') == 'box-001'
        assert getattr(p1_b1, 'contents') == 'electronics'
        assert getattr(p1_b2, 'id') == 'box-002'
        assert getattr(p1_b2, 'contents') == 'books'
        
        # Check second palette
        p2 = palette._object_container[1]
        assert getattr(p2, 'id') == 'pal-002'
        assert getattr(p2, 'weight') == 150
        
        # Check second palette's boxes
        p2_box = getattr(p2, 'Box')
        assert hasattr(p2_box, '_object_container')
        assert len(p2_box._object_container) == 1
        
        p2_b1 = p2_box._object_container[0]
        assert getattr(p2_b1, 'id') == 'box-003'
        assert getattr(p2_b1, 'contents') == 'furniture'
        
        # Test JSON transformation
        shipment.json_transform()
        assert shipment.json_dict == {
            'id': 'ship-001',
            'SYSServiceMethod': None,
            'Palette': [
                {
                    'id': 'pal-001',
                    'weight': 100,
                    'Box': [
                        {'id': 'box-001', 'contents': 'electronics'},
                        {'id': 'box-002', 'contents': 'books'}
                    ]
                },
                {
                    'id': 'pal-002',
                    'weight': 150,
                    'Box': [
                        {'id': 'box-003', 'contents': 'furniture'}
                    ]
                }
            ]
        }
