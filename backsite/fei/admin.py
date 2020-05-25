from django.contrib import admin
from django.utils.translation import gettext_lazy
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile, Thought, Media
# Register your models here.

class UserProfileAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'phonenum', 'email', 'last_login')
    fieldsets = (
        (None,{'fields':('username','password','email')}),

        (gettext_lazy('User Information'),{'fields':('nickname','phonenum','signature','wxopenid')}),

        (gettext_lazy('Sign'), {'fields': ('signup_type','is_signup','signup_time',
                                                  'date_joined', 'last_login')}),

        # (gettext_lazy('Permissions'), {'fields': ('groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser')}),#这块就不显示了
    )
    

class ThoughtAdmin(admin.ModelAdmin):
    list_display = ('thought_id', 'title', 'type_raw', 'create_time', 'views', 'username')

    def username(self, obj): #返回外键的username
        return '%s'%obj.author.username

    # def link(self, obj): #返回外键的link
    #     return '%s'%obj.author.picture.link

class MediaAdmin(admin.ModelAdmin):
    list_display = ('media_id', 'link', 'media_type')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Thought, ThoughtAdmin)
admin.site.register(Media, MediaAdmin)

