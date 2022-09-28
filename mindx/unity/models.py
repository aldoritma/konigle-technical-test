from sqlite3 import Timestamp
import uuid
from django.db import models
from datetime import datetime
from django.utils import timezone
class Subscriber(models.Model):
    status = (
        ('UNSUBSCRIBED', 'unsubscribed'),
        ('SUBSCRIBED', 'subscribed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, choices=status, default='SUBSCRIBED')
    

    @property
    def timestamp_string(self):
        now = datetime.now(timezone.utc)
        then = self.timestamp
        diff = now - then
        if diff.seconds < 60:
            return f'{diff.seconds} seconds ago'
        elif diff.seconds < 3600:
            return f'{diff.seconds // 60} minutes ago'
        elif diff.seconds < 86400:
            return f'{diff.seconds // 3600} hour(s) ago'
        
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
    
    def total_emails(self):
        return Subscriber.objects.count()

    def total_subscribers(self):
        return Subscriber.objects.filter(status='SUBSCRIBED').count()
    
    def total_unsubscribers(self):
        return Subscriber.objects.filter(status='UNSUBSCRIBED').count()
    
    def total_emails_this_month(self):
        return Subscriber.objects.filter(timestamp__month=datetime.now().month).count()