from django.contrib.auth.password_validation import MinimumLengthValidator, validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import auth

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegistrationSerializer


class CustomPasswordValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        super(CustomPasswordValidator, self).validate(password, user)

        has_digits, has_alphas = False, False
        for char in password:
            if char.isdigit():
                has_digits = True
            if char.isalpha():
                has_alphas = True
            if has_digits & has_alphas:
                return

        raise ValidationError('Bad password. Password must contain at least one number and letter')


# /registration
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            username = serializer['username'].value
            password = serializer['password'].value

            try:
                validate_email(username)
            except ValidationError as error:
                data['username'] = error
                return Response(data)

            try:
                validate_password(password, password_validators=[CustomPasswordValidator()])
            except ValidationError as error:
                data['password'] = error
                return Response(data)

            serializer.save()
            data['response'] = True

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            return Response(data, status=status.HTTP_200_OK)

        else:
            data = serializer.errors
            return Response(data)
