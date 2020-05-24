from django.contrib import admin
from .models import Thought
# Register your models here.


class ThoughtAdmin(admin.ModelAdmin):
    fieldsets = (
        ['Main',{
            'fields':('name','face','nickname','text','img',),
        }]
    )
admin.site.register(Thought)