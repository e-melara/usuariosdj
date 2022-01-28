from django.views.generic import View
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from .models import User
from .functions import code_generator
from .forms import (
    UserRegisterForm, UserFormLogin, UpdatePasswordForm, VerificateForm
)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('users_app:login')
        )


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('register-user')

    def form_valid(self, form):
        # Generamos codigo
        codigo = code_generator()
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro=codigo
        )
        asunto = 'Confirmacion de email'
        mensaje = 'Codigo de confirmacion: ' + codigo
        email_remitente = 'melara0606@gmail.com'

        send_mail(asunto, message=mensaje, from_email=email_remitente, recipient_list=[
            form.cleaned_data['email']
        ])
        return HttpResponseRedirect(
            reverse(
                'users_app:verificated',
                kwargs={
                    'pk': usuario.id
                }
            )
        )


class LoginUser(FormView):
    form_class = UserFormLogin
    template_name = 'users/login.html'
    success_url = reverse_lazy('home_app:home')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )

        login(self.request, user)

        return super(LoginUser, self).form_valid(form)


class UpdatePasswordView(LoginRequiredMixin, FormView):
    form_class = UpdatePasswordForm
    login_url = reverse_lazy('users_app:login')
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_app:login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(username=usuario.username,
                            password=form.cleaned_data['password']
                            )
        if user:
            new_password = form.cleaned_data['re_password']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class CodeVerificationView(FormView):
    form_class = VerificateForm
    template_name = 'users/verification.html'
    success_url = reverse_lazy('users_app:login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })

        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        return super(CodeVerificationView, self).form_valid(form)
