from rest_framework import serializers
from .models import User
from validate_docbr import CPF
from datetime import date


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone", "cpf", "first_name", "last_name", "date_of_birth"]
    
    def validate_date_of_birth(self, value:date):
        today = date.today()
        if today.year - value.year <= 18:
            raise serializers.ValidationError("Invalid age. User must be at least 18 years old.")
        return value
        
    def validate_cpf(self, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError("Invalid CPF. Enter a valid CPF.")
        return value

class RegisterUserValidateSerializer(serializers.Serializer):
    data_token = serializers.CharField(max_length=225)
    code = serializers.IntegerField()
    