from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.validators import validate_email


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

        raise ValidationError('Bad password')


def registration(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html', {
            'form': AuthenticationForm()
        })

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            validate_email(username)
            validate_password(password, password_validators=[CustomPasswordValidator()])
        except ValidationError as error:
            error = 'Некорректный email' if ('email' in str(error)) else 'Неподходящий пароль. ' \
                                                                    'Пароль должен быть не ' \
                                                                    'короче 8 символов и содержать ' \
                                                                    'хотя бы одну цифру и букву любого регистра'

            return render(request, 'registration/registration.html', {
                'form': AuthenticationForm(),
                'error_msg': error
            })

        try:
            User.objects.get(username=username)

            return render(request, 'registration/registration.html', {
                'form': AuthenticationForm(),
                'error_msg': 'Пользователь с таким email уже существует'
            })
        except User.DoesNotExist:
            User.objects.create_user(username=username, password=password).save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

        return redirect('index')


def logout(request):
    auth.logout(request)

    return redirect('login')
