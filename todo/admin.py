from django.contrib import admin
from .models import Todo

# Create a read-only variable
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

# Register models here
admin.site.register(Todo, TodoAdmin)
