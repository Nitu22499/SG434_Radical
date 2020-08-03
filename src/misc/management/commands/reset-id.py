from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.management.color import no_style
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write('Reset AutoFields ...')
        APPS = apps.get_app_configs()

        # APPS = [apps.get_app_config(app) for app in APPS]
        models = []
        for app in APPS:
            models.extend(list(app.get_models()))

        sequence_sql = connection.ops.sequence_reset_sql(no_style(), models)
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                self.stdout.write(sql)
                cursor.execute(sql)
        self.stdout.write(self.style.SUCCESS('Reset AutoField complete.'))