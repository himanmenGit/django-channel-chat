from django.core.management import BaseCommand
from django_q.brokers import get_broker
from django_q.cluster import Cluster


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--worker_name', '-wn', type=str)

    def handle(self, *args, **options):
        q = Cluster(get_broker(options['worker_name']))
        q.start()
