from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        validators = []

    def save(self, *args, **kwargs):
        user = User(username=self.validated_data['username'])
        password = self.validated_data['password']

        user.set_password(password)
        user.save()

        return user
