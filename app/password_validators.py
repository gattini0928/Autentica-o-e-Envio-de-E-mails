import string
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def __init__(self):
        self.min_length = 8
        self.requirements = {
            'uppercase': True,
            'lowercase': True,
            'digits': True,
            'special': True,
        }

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Sua senha deve conter no mínimo %(min_length)d caracteres."),
                code="password_too_short",
                params={"min_length": self.min_length},
            )
        
        if self.requirements['uppercase'] and not any(c.isupper() for c in password):
            raise ValidationError(
                _("Sua senha deve ter pelo menos uma letra maíscula."),
                code="password_no_uppercase",
            )
        
        if self.requirements['lowercase'] and not any(c.islower() for c in password):
            raise ValidationError(
                _("Sua senha deve ter pelo menos uma letra minúscula."),
                code="password_no_lowercase",
            )
        
        if self.requirements['digits'] and not any(c.isdigit() for c in password):
            raise ValidationError(
                _("Sua senha deve ter pelo menos um dígito."),
                code="password_no_digit",
            )
        
        if self.requirements['special'] and not any(c in string.punctuation for c in password):
            raise ValidationError(
                _("Sua senha deve ter pelo menos um caractere especial"),
                code="password_no_special",
            )

    def get_help_text(self):
        requirements = []
        if self.requirements['uppercase']:
            requirements.append(_('Pelo menos uma maíscula'))
        if self.requirements['lowercase']:
            requirements.append(_('Pelo menos uma minúscula'))
        if self.requirements['digits']:
            requirements.append(_("Pelo menos um digito"))
        if self.requirements['special']:
            requirements.append(_("Pelo menos um caractere especial"))
        
        return _("Senha precisa ter os seguintes requisitos: ") + ", ".join(requirements)