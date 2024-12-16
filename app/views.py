from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView
from django.urls import reverse_lazy
from .forms import UserCreateForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import os
from dotenv import load_dotenv

load_dotenv()

class HomepageView(TemplateView):
    template_name = 'app/homepage.html'

class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'app/criar_conta.html'
    success_url = reverse_lazy('login')

    def form_valid(self,form):
        user = form.save()
        self.enviar_email_confirmacao(user)
        messages.success(self.request, f'Conta {user.username} criada com sucesso! Faça login para continuar.')
        return self.render_to_response(self.get_context_date(form=form, redirect_to='home'))
    
    def form_invalid(self, form):
        messages.error(self.request,'Ocorreu um erro ao criar a conta. Por favor, tente novamente.')
        return self.render_to_response(self.get_context_data(form=form, redirect_to='criar_conta'))

    def enviar_email_confirmacao(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(self.request).domain

        print(f"UID: {uid}, Token: {token}, Domain: {domain}")

        subject = 'Confirmação de E-mail'
        message = render_to_string('app/email/email_confirmacao.html',
            {'user':user,
            'uid':uid,
            'token':token,
            'domain':domain})
        user.email_user(subject, message)
        messages.success(self.request, "Um e-mail de confirmação foi enviado.")
        return redirect('homepage') 

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    def dispatch(self, request, *args, **kwargs):
        if not User.objects.exists():
            messages.error(request,'Nenhum usuário registrado, Por favor, crie um primeiro.')
            return reverse_lazy('criar_conta')
        return super().dispatch(request, *args, **kwargs)
    
    def form_invalid(self,form):
        messages.error(self.request, "Username ou senha inválidos, digite novamente.")
        return super().form_invalid(form)
    
    def form_valid(self,form):
        messages.success(self.request, 'Login realizado com sucesso')
        return super().form_valid(form)

class PerfilView(LoginRequiredMixin,DetailView):
    template_name = 'app/perfil.html'
    model = User

    def get_object(self, queryset=None):
        return self.request.user

def ativar_email(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        perfil = user.perfil
        perfil.email_confirmado = True
        perfil.save()
        messages.success(request, 'Seu e-mail foi confirmado com sucesso')
        return redirect('email_ativado')
    else:
        return render('app/email/email_expirado.html', {'message':'Link de ativação expirado '})

def email_ativado(request):
    return render(request,'app/email_ativado.html' ,{'message':'Seu e-mail foi confirmado com sucesso'})

@login_required
def fazer_logout(request):
    logout(request)
    return redirect('login')


