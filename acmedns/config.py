# -*- encoding: utf-8 -*-
#
# Copyright (c) 2016 Wayoos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

try:
    from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
except ImportError:  # pragma: no cover
    # Python 3
    from configparser import RawConfigParser, NoSectionError, NoOptionError

"""

.. code:: ini

    [default]
    ; general configuration: default endpoint
    url=https://acme-v01.api.letsencrypt.org

    [adapter-ovh]
    endpoint=ovh-eu
    application_key=my_app_key
    application_secret=my_application_secret
    consumer_key=my_consumer_key

"""

#: Locations where to look for configuration file by *increasing* priority
CONFIG_PATH = [
    '/etc/acmedns.conf',
    os.path.expanduser('~/.acmedns.conf'),
    os.path.realpath('./acmedns.conf'),
]

class ConfigurationManager(object):
    '''
    Application wide configuration manager
    '''
    def __init__(self, config=CONFIG_PATH):
        '''
        Create a config parser and load config from environment.
        '''
        # create config parser
        self.config = RawConfigParser()
        self.config.read(config)

    @classmethod
    def fromfilename(cls, name):
        return cls([name])

    def get(self, section, name):
        '''
        Load parameter ``name`` from configuration, respecting priority order.
        Most of the time, ``section`` will correspond to the current api
        ``endpoint``. ``default`` section only contains ``endpoint`` and general
        configuration.
        :param str section: configuration section or region name. Ignored when
            looking in environment
        :param str name: configuration parameter to lookup
        '''
        # 1/ try env
        try:
            return os.environ['ACMEDNS_'+name.upper()]
        except KeyError:
            pass

        # 2/ try from specified section/endpoint
        try:
            return self.config.get(section, name)
        except (NoSectionError, NoOptionError):
            pass

        # not found, sorry
        return None