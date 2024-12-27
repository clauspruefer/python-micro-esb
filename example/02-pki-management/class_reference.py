class_reference_ca = {
    'CertCA': {
        'property_ref': 'Cert',
        'children': {
            'Smartcard': {
                'property_ref': 'Smartcard',
                'children': {
                    'SmartcardContainer': {
                        'property_ref': 'SmartcardContainer'
                    }
                }
            }
        }
    }
}

class_reference_server = {
    'CertServer': {
        'property_ref': 'Cert',
        'children': {
            'Smartcard': {
                'property_ref': 'Smartcard',
                'children': {
                    'SmartcardContainer': {
                        'property_ref': 'SmartcardContainer'
                    }
                }
            },
            'CertCA': {
                'property_ref': 'Cert',
                'children': {
                    'Smartcard': {
                        'property_ref': 'Smartcard',
                        'children': {
                            'SmartcardContainer': {
                                'property_ref': 'SmartcardContainer'
                            }
                        }
                    }
                }
            }
        }
    }
}

class_reference_client = {
    'CertClient': {
        'property_ref': 'Cert',
        'children': {
            'Smartcard': {
                'property_ref': 'Smartcard',
                'children': {
                    'SmartcardContainer': {
                        'property_ref': 'SmartcardContainer'
                    }
                }
            },
            'CertCA': {
                'property_ref': 'Cert',
                'children': {
                    'Smartcard': {
                        'property_ref': 'Smartcard',
                        'children': {
                            'SmartcardContainer': {
                                'property_ref': 'SmartcardContainer'
                            }
                        }
                    }
                }
            },
            'CertServer': {
                'property_ref': 'Cert',
                'children': {
                    'Smartcard': {
                        'property_ref': 'Smartcard',
                        'children': {
                            'SmartcardContainer': {
                                'property_ref': 'SmartcardContainer'
                            }
                        }
                    }
                }
            }
        }
    }
}
