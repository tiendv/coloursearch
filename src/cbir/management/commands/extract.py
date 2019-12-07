from django.core.management.base import BaseCommand, CommandError
from ...views.extract_features import extract_features


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)
        parser.add_argument('method', type=str)
        parser.add_argument('-p1', '--param1', type=float, required=True)
        parser.add_argument('-p2', '--param2', type=float, required=False)
        parser.add_argument('-p3', '--param3', type=float, required=False)

    def handle(self, *args, **options):
        status = extract_features(options['path'], options['method'], options['param1'],
                                  options['param2'], options['param3'])
        self.stdout.write(self.style.SUCCESS('Command done.'))
