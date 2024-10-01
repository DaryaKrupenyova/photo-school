from django import forms
import re


class PasswordStrength:
    def validate(self, password, user=None):
        pattern_password = re.compile(r'(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z@$!%*#?&()|]{8,}$')
        if not pattern_password.match(password):
            raise forms.ValidationError('Пароль не соответствует требованиям')

    def get_help_text(self):
        print('Пароль не соответствует требованиям')
