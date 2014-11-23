import sys

from django.core.management.base import NoArgsCommand
from django.db import models


class Command(NoArgsCommand):
    help = 'Print all models and count of objects in them'

    def handle(self, **options):
        for app in models.get_apps():
            for model in models.get_models(app):
                objects_quantity = model.objects.count()
                print "Model {0} has {1} objects".format(model.__name__, objects_quantity)
                sys.stderr.write('error: Model {0} has {1} objects\n'.format(model.__name__, objects_quantity))
