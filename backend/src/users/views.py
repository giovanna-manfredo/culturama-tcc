from rest_framework.views import APIView, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from rest_framework.response import Response

from .serializers import RegisterUserSerializer, RegisterUserValidateSerializer
from drf_spectacular.utils import extend_schema

from services.email_client import EmailClient
from services.token_manager import TokenManager

from rest_framework import viewsets
from rest_framework.decorators import action

# class RegisterLoginUserView(APIView):
#     permission_classes = [AllowAny]

#     @extend_schema(
#     request=RegisterUserSerializer
#     ) 
#     def post(self, request):
#         serializer = RegisterUserSerializer(data=request.data)
#         if serializer.is_valid():
#             result = EmailClient.create_email_validation_code(request.data["email"])

#             token = TokenManager.generate_custom_token(serializer.data)

#             return Response({"data_token":token, "email":result}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class RegisterUser(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
    request=RegisterUserSerializer
    ) 
    @action(detail=False, methods=['post'], url_path='register-one')
    def register_get_info(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            result = EmailClient.create_email_validation_code(request.data["email"])

            data = {"user":serializer.data, "code":result}
            token = TokenManager.generate_custom_token(data)

            return Response({"data_token":token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
    request=RegisterUserValidateSerializer
    ) 
    @action(detail=False, methods=['post'], url_path='register-two')
    def register_validate(self, request):
        data = TokenManager.verify_custom_token(request.data["data_token"])
        if str(request.data["code"]) != data["data"]["code"]:
            return Response("Invalid code", status=status.HTTP_400_BAD_REQUEST)
        user_data = data["data"]["user"]
        serializer = RegisterUserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(data["data"]["user"], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    

        
