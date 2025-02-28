from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone", "cpf", "first_name", "last_name", "date_of_birth"]
        read_only_fields = ["cpf"]

