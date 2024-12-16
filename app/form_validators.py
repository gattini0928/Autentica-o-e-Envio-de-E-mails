from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
from django.contrib.auth.models import User

def validate_email(email):
    """
    Validador customizado para verificar e-mails duplicados e domínios permitidos.
    """
    # Valida o formato do e-mail usando o validador padrão do Django
    try:
        django_validate_email(email)
    except ValidationError:
        raise ValidationError('O e-mail fornecido não é válido.')

    # Verifica se o domínio está na lista permitida
    dominios_permitidos = ['gmail.com', 'icloud.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
    dominio = email.split('@')[-1].lower()  # Extrai o domínio e padroniza para minúsculas
    if dominio not in dominios_permitidos:
        raise ValidationError('Digite um e-mail com domínio permitido (ex: gmail.com, outlook.com).')

    # Verifica se o e-mail já está em uso
    if User.objects.filter(email=email).exists():
        raise ValidationError('Este e-mail já está em uso.')
    return email