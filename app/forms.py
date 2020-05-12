# coding=utf-8
from django import forms


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone'
            if field_name == 'numero' or field_name == 'number':
                field.widget.attrs['class'] = 'form-control numero'


class FormUploadCsv(BaseForm):
    file = forms.FileField(widget=forms.TextInput(attrs={'required': True,
                                                         'placeholder': 'Arquivo CSV'
                                                         }))


class FormBaseAddress(BaseForm):
    cep = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'required': True,
                                                                       'maxlength': 200,
                                                                       'placeholder': 'CEP'
                                                                       }))
    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    bairro = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                           'maxlength': 200,
                                                                           'placeholder': 'Bairro'
                                                                           }))
    cidade = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                           'maxlength': 200,
                                                                           'placeholder': 'Cidade'
                                                                           }))
    estado = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                           'maxlength': 200,
                                                                           'placeholder': 'Estado'
                                                                           }))
    complemento = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'required': True,
                                                                                'maxlength': 300,
                                                                                'placeholder': 'Complemento'
                                                                                }))


class FormLogin(BaseForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))
