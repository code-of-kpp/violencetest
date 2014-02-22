import logging

from django.conf import settings

from cqlengine import Model  # lint:ok

from cqlwrapper import default_cassandra_alias

from cqlwrapper.cqlmodels import columns  # lint:ok
from cqlwrapper.cqlmodels.columns import *


logger = logging.getLogger(__name__)


from cqlengine.connection import setup

try:
    setup(**settings.CASSANDRA[default_cassandra_alias])
except Exception as exc:
    logger.error('Cannot setup connection to cassandra: %r', exc)
