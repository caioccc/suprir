# coding=utf-8
from django import forms
from django.forms import ModelForm

from app.models import Profissional


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
                                                                       'maxlength': 200
                                                                       }))
    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200
                                                                         }))
    bairro = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                           'maxlength': 200
                                                                           }))
    cidade = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                           'maxlength': 200
                                                                           }))
    estado = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                           'maxlength': 200
                                                                           }))


class FormBaseAddressNotRequired(BaseForm):
    cep = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'required': False,
                                                                                       'maxlength': 200
                                                                                       }))
    endereco = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'required': False,
                                                                                             'maxlength': 200
                                                                                             }))
    numero = forms.CharField(max_length=6, required=False, widget=forms.TextInput(attrs={'required': False,
                                                                                         'maxlength': 200
                                                                                         }))
    bairro = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'required': False,
                                                                                           'maxlength': 200
                                                                                           }))
    cidade = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'required': False,
                                                                                           'maxlength': 200
                                                                                           }))
    estado = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'required': False,
                                                                                           'maxlength': 200
                                                                                           }))


class FormLogin(BaseForm):
    username = forms.CharField(widget=forms.NumberInput(attrs={'required': True,
                                                               'placeholder': 'Telefone Celular'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))


class FormRegisterCliente(FormBaseAddressNotRequired):
    nome = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                         'maxlength': 100}))
    sobrenome = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                              'maxlength': 100}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True}))
    telefone = forms.CharField(widget=forms.NumberInput(attrs={'required': True}))


class FormRegisterProfissional(ModelForm, FormRegisterCliente):
    class Meta:
        model = Profissional
        fields = ['categoria', 'telefone_2', 'link_facebook', 'link_instagram', 'url_site', 'cpf', 'cnpj']

    def __init__(self, *args, **kwargs):
        super(FormRegisterProfissional, self).__init__(*args, **kwargs)
        # self.fields['categoria'].required = False
        # self.fields['categoria'].widget.attrs['required'] = 'False'
        # self.fields['telefone_2'].required = False
        # self.fields['telefone_2'].widget.attrs['required'] = 'False'
        # self.fields['link_facebook'].required = False
        # self.fields['link_facebook'].widget.attrs['required'] = 'False'
        # self.fields['link_instagram'].required = False
        # self.fields['link_instagram'].widget.attrs['required'] = 'False'
        # self.fields['url_site'].required = False
        # self.fields['url_site'].widget.attrs['required'] = 'False'
