from django.core.management.base import BaseCommand, CommandError
from ...views.annotate import annotate


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str)

    def handle(self, *args, **options):
        status = annotate(options['directory_path'])
        self.stdout.write(self.style.SUCCESS('Command done.'))
