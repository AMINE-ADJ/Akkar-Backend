from rest_framework import serializers
from api.models import Superuser
class SuperuserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Superuser
        fields= "__all__"