from setuptools import setup

setup(

    name = 'python-micro-esb',
    version = '0.01alpha',
    author = 'Claus Prüfer',
    author_email = 'pruefer@webcodex.de',
    maintainer = 'Claus Prüfer',
    description = 'A small OOP based Enterprise Service Bus implementation.',
    homepage = 'http://micro-esb.python.webcodex.de',
    license = 'GPLv3',
    long_description = open('./README.rst').read(),

    packages = [
        'micro-esb'
    ],

    package_dir = {
        'micro-esb': 'src/'
    },

    zip_safe = True

)
