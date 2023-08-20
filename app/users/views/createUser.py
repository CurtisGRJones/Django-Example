from django.forms import ValidationError
from rest_framework.mixins import (
    CreateModelMixin
)
from rest_framework.viewsets import GenericViewSet

from ..utils.responses import success_response

from ..models import CustomUser
from ..serializers import CustomUserSerializer

from rest_framework import status
from rest_framework.response import Response

class CreateUserViewSet(
        GenericViewSet,  # generic view functionality
        CreateModelMixin # handles POSTs 
    ):  

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        queryset = CustomUser.objects.filter(email=serializer.validated_data['email'])
        if queryset.exists():
            raise ValidationError('A user with this email has already signed up', code="invalid")
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        user = CustomUser.objects.get(email=serializer.validated_data['email'])

        token = user.set_token()


        response = success_response({"token": token}, status=status.HTTP_201_CREATED, headers=headers)

        response = Response({
            'success': True,
            'data': {
                'token': token
            }
        }, status=status.HTTP_201_CREATED, headers=headers)

        response.set_cookie('auth_token', token)

        return response

