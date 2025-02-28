from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import date
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from validate_docbr import CPF


class CustomUserManager(BaseUserManager):
    def create_user(self, email:str, cpf:str, date_of_birth:date, password=None, **extra_fields):
        self.validation_email(email)
        self.validate_cpf(cpf)
        self.is_adult(date_of_birth)

        user = self.model(email=email, cpf=cpf, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)  
        return user

    def create_superuser(self, email, cpf, date_of_birth, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  

        return self.create_user(email, cpf, date_of_birth, password, **extra_fields)

    def validation_email(self, value):
        try:
            validate_email(value)
        except ValidationError as e:
             raise ValidationError("Email inválido.")

    def is_adult(self, value:date):
        today = date.today()
        if today.year - value.year <= 18:
            raise ValidationError("Idade inválida.")
        
    def validate_cpf(self, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise ValidationError("CPF inválido.")



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField(null=False, blank=False)
    # profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True) # future feature
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [ "cpf", "date_of_birth"]

    class Meta:
        db_table = "users" 
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

