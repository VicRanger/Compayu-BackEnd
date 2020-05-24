from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

    
class Thought(models.Model):
    title = models.CharField(max_length=20)
    text = models.TextField()
    type_raw = models.CharField(max_length=20)
    type_ai = models.CharField(max_length=20, blank=True, null=True)
    type_human = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField(default=timezone.now)
    modified_time = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(default=0)
    # author = models.ForeignKey('User', related_name='thought_author', on_delete=models.CASCADE)
    # picture = models.ForeignKey('Media', related_name='thought_media', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.mood_type + ' - ' + self.text[:10] + ' : ' + str(self.mod_time)

    class Meta:
        app_label = 'compayu'
        db_table = 'compayu_thought'

    def get_dict(self):
        ret = {}
        ret['type_raw'] = self.type_raw
        ret['text'] = self.text
        ret['create_time'] = str(self.create_time)
        ret['id'] = self.id
        return ret
