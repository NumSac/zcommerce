from django.contrib import admin

# Register your models here
from .models import Synchronization


class SynchronizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Synchronization)
