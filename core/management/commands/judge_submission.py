from django.core.management.base import BaseCommand
from core import tasks


class Command(BaseCommand):
    help = 'Provisions an worker to judge a source file. DO NOT CALL MANUALLY!'

    def handle(self, *args, **options):
        tasks.judge_submission()
