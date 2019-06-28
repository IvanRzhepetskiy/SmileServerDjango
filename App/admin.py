from django.contrib import admin

# Register your models here.
from App.models import Profile, Recognition

admin.site.register(Profile)
admin.site.register(Recognition)
