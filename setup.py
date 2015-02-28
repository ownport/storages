import storages

setup_args = {
    'name': 'storages',
    'version': storages.__version__,
    'url': 'https://github.com/ownport/storages',
    'description': 'The collection of simple storages',
    'author': storages.__author__,
    'author_email': 'ownport@gmail.com',
    'maintainer': storages.__author__,
    'maintainer_email': 'ownport@gmail.com',
    'license': 'Apache 2.0',
    'packages': ['storages', ],
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Topic :: Database',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
}
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(**setup_args)