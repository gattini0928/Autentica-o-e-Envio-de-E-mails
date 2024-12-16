from django.urls import path
from .views import HomepageView
from django.contrib.auth import views as auth_views # Importando views de autenticação
from .views import UserCreateView, CustomLoginView, PerfilView, fazer_logout, ativar_email, email_ativado
from .forms import UserLoginForm
from django.urls import reverse_lazy

urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('criarconta/', UserCreateView.as_view(), name='criar_conta'),
    path('logout/', fazer_logout, name='logout'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('ativaremail/<str:uid>/<str:token>/', ativar_email, name='ativar_email'),
    path('emailativado/', email_ativado, name='email_ativado'),
    path("password_change/", auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('login')), name="password_change"),
    path("password_change/done/", 
     auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
     name="password_change_done"),
     
    path("password_reset/", 
     auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), 
     name="password_reset"),
     
    path("password_reset/done/", 
     auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
     name="password_reset_done"),
     
    path("reset/<uidb64>/<token>/", 
     auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
     name="password_reset_confirm"),
     
    path("reset/done/", 
     auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
     name="password_reset_complete"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
