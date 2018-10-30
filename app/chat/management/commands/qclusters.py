from django.conf import settings
from django.core.management import BaseCommand
from django_q.brokers import get_broker
from django_q.cluster import Cluster


class Command(BaseCommand):
    def handle(self, *args, **options):
        for c in settings.DJANGO_Q_CLUSTERS:
            q = Cluster(get_broker(c))
            q.start()
