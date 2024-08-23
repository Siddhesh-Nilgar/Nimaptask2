from django.contrib import admin
from core.models import Client, Project

admin.site.register(Client)
admin.site.register(Project)
from django.contrib.auth.models import User

# Create a superuser
user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
