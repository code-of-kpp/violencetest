from __future__ import print_function

from optparse import make_option
from itertools import chain

import six

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.utils.importlib import import_module

from cqlengine.management import sync_table
from cqlengine.models import BaseModel

from cqlwrapper import models_model_name
from cqlwrapper.cqlmodels import *  # setup connections


class Command(NoArgsCommand):

    option_list = NoArgsCommand.option_list + (
        make_option('--create-keyspaces',
                    action='store_true',
                    dest='create_keyspaces',
                    default=False,
                    help='Also create keyspace if not exists'),
        make_option('--noinput',
                    action='store_true',
                    dest='noinput',
                    default=False,
                    help='Do not interact with user'),
    )

    def handle_noargs(self, **options):

        verbosity = int(options.get('verbosity'))
        create_ks = (options.get('create_keyspaces'))

        modules = set()

        for app_name in settings.INSTALLED_APPS:
            if verbosity >= 3:
                print('Loading app %s' % app_name)
            try:
                modules.add(import_module(models_model_name, app_name))
            except ImportError as exc:
                msg = exc.args[0]
                modname = models_model_name[1:]
                if not msg.startswith('No module named') \
                   or modname not in msg:
                    raise
            else:
                if verbosity >= 2:
                    print('Loaded app %s' % app_name)

        models = frozenset(chain.from_iterable(
            (
                (obj for obj in six.itervalues(module.__dict__)
                 if isinstance(obj, six.class_types) and
                    issubclass(obj, BaseModel))
                for module in modules
            )
        ))

        for model in models:
            if model.__abstract__:
                continue
            if verbosity >= 1:
                print('Creating table %s' %
                      (model.__table_name__ or model.__name__))
            sync_table(model, create_ks)
