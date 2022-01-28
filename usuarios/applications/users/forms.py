from django import forms
from django.contrib.auth import authenticate

from .models import User


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    re_password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir contraseña'
            }
        )
    )


class UserFormLogin(forms.Form):
    username = forms.CharField(
        label='username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'placeholder': 'Username',
                'style': '{ margin: 10px }'
            }
        )
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'style': '{ margin: 10px }'
            }
        )
    )

    def clean(self):
        cleaned_data = super(UserFormLogin, self).clean()

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError(
                'Los datos del usuario no son correctos')

        return self.cleaned_data


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    re_password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir contraseña'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero'
        )

    def clean_re_password(self):
        if self.cleaned_data['re_password'] != self.cleaned_data['password']:
            self.add_error('re_password', 'Las contraseñas no son iguales')

        if len(self.cleaned_data['password']) < 5:
            self.add_error(
                'password', 'La contraseña no debe ser menor a 5 caracteres'
            )


class VerificateForm(forms.Form):
    codregistro = forms.CharField(required=True)

    def __init__(self, pk, *args, **kwargs):
        self.user_id = pk
        super(VerificateForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            # verificar si el codigo y usuario son validos
            activo = User.objects.cod_validation(
                self.user_id,
                codigo
            )

            if not activo:
                raise forms.ValidationError('El codigo es incorrecto')

        else:
            raise forms.ValidationError('El codigo es incorrecto')
