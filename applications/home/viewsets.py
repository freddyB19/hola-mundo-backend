from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from . import serializers, models

class PersonViewset(viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    #pagination_class = serializers.PersonPagination
    queryset = models.Person.objects.all()

    permission_classes = (IsAuthenticated,)

