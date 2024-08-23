import os
import sys
import django

# Add the parent directory of the project to sys.path
sys.path.append('E:/Nimap/project_manager')  # Adjust this path if needed

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')

# Initialize Django
django.setup()

# Now you can import Django and DRF modules
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import Client, Project
from core.serializers import ClientSerializer, ProjectSerializer

# Your viewsets
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, client_id=None):
        client = Client.objects.get(pk=client_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(client=client, created_by=request.user)
            project.users.set(request.data.get('users'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        user = request.user
        queryset = user.projects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
