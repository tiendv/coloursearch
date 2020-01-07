from django.core.management.base import BaseCommand, CommandError
from ...views.evaluate import evaluate


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('database_name', type=str)
        parser.add_argument('query_path', type=str)
        parser.add_argument('extraction_id', type=int)
        parser.add_argument('k', type=int)
        parser.add_argument('type', type=str)

    def handle(self, *args, **options):
        status = evaluate(options['database_name'],
                          options['query_path'],
                          options['extraction_id'],
                          options['k'],
                          options['type'])
        self.stdout.write(self.style.SUCCESS('Command done.'))
