from django.core.management.base import BaseCommand
from schoolinfo.models import SchoolProfile
from django.core.cache import cache
from misc.utilities import academic_year
from django.utils import timezone

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        if cache.get('last_synced'):
            last_synced_time = timezone.now()
            obj = SchoolProfile.objects.filter(sp_school = cache.get('school_admin')).update(
                sp_last_synced = last_synced_time
            )