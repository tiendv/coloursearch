from django.core.management.base import BaseCommand, CommandError
from ...views.retrieve import evaluate_performance


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('database_name', type=str)
        parser.add_argument('query_path', type=str)
        parser.add_argument('extraction_id', type=float)
        parser.add_argument('k', type=int)

    def handle(self, *args, **options):
        status = evaluate_performance(options['database_name'],
                                      options['query_path'],
                                      options['extraction_id'], 
                                      options['k'])
        self.stdout.write(self.style.SUCCESS('Command done.'))
