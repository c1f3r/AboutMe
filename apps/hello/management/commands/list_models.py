import sys
from django.template.defaultfilters import pluralize
from django.core.management.base import NoArgsCommand
from django.db import models


class Command(NoArgsCommand):
    help = 'Print all models and count of objects in them'

    def handle(self, **options):
        for app in models.get_apps():
            for model in models.get_models(app):
                objects_quantity = model.objects.count()
                str_for_out = "Model {0} has {1} object{2}"
                print str_for_out.format(model.__name__, objects_quantity,
                                         pluralize(objects_quantity))
                str_for_err = "error: Model {0} has {1} object{2}\n"
                sys.stderr.write(str_for_err.format(model.__name__,
                                                    objects_quantity,
                                                    pluralize(objects_quantity)
                                                    )
                                 )
