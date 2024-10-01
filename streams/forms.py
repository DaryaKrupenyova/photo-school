from django import forms


class StreamForm(forms.Form):
    first = forms.CharField(
        label='Ссылка вебинара', required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-sm-8',
                'id': 'firstval',
            }
        )
    )
    second = forms.CharField(
        label='Ссылка ютуба', required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-sm-8',
                'id': 'secondval',
            }
        )
    )
