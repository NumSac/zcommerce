from django.contrib import admin

from .models import DynamoDbTable


# Register your models here.
class DynamoDbTableAdmin(admin.ModelAdmin):
    pass


admin.site.register(DynamoDbTable, DynamoDbTableAdmin)
