from django.contrib import admin

# Importing database models:
from .models import ExternalDatabase

# Adding The ExternalDatabase Model to the Admin Dashboard:
class ExternalDatabaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExternalDatabase, ExternalDatabaseAdmin)
