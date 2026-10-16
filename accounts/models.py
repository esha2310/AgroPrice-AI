from django.conf import settings
from django.db import models
class WatchItem(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
 series_id=models.CharField(max_length=64)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:constraints=[models.UniqueConstraint(fields=['user','series_id'],name='unique_user_series')]
