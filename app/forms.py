# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, inlineformset_factory

from app.models import Profissional, CarrinhoDeServicos, ContratoDeServico, ItemServico, Servico, FotoServico


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


class FormCarrinho(ModelForm, BaseForm):
    class Meta:
        model = CarrinhoDeServicos
        fields = ['cliente', 'valor_total', 'forma_pagamento', ]

    def __init__(self, *args, **kwargs):
        super(FormCarrinho, self).__init__(*args, **kwargs)


class FormItemServico(ModelForm, BaseForm):
    class Meta:
        model = ItemServico
        fields = ['servico', 'observacoes', 'valor_total', ]

    def __init__(self, *args, **kwargs):
        super(FormItemServico, self).__init__(*args, **kwargs)


class FormContrato(ModelForm, BaseForm):
    class Meta:
        model = ContratoDeServico
        fields = ['status', ]

    def __init__(self, *args, **kwargs):
        super(FormContrato, self).__init__(*args, **kwargs)


ItemServicoFormSet = inlineformset_factory(CarrinhoDeServicos, ItemServico, form=FormItemServico, extra=1)


class FormServico(ModelForm, BaseForm):
    class Meta:
        model = Servico
        fields = ['titulo', 'descricao', 'valor_base', 'disponivel', 'profissional']

    def __init__(self, *args, **kwargs):
        super(FormServico, self).__init__(*args, **kwargs)
        self.fields['profissional'].label = ''
        self.fields['profissional'].widget.attrs['class'] = 'hidden'
        for field_name, field in self.fields.items():
            field.widget.attrs['required'] = True


class FormFotoServico(ModelForm, BaseForm):
    class Meta:
        model = FotoServico
        fields = ['file', 'url']

    def __init__(self, *args, **kwargs):
        super(FormFotoServico, self).__init__(*args, **kwargs)
        self.fields['file'].label = 'Arquivo'
        self.fields['url'].label = ''
        self.fields['url'].widget.attrs['class'] = 'hidden'


FotoServicoFormSet = inlineformset_factory(Servico, FotoServico, form=FormFotoServico, extra=1)


class FormProfissional(ModelForm, BaseForm):
    class Meta:
        model = Profissional
        fields = ['categoria', 'user', 'telefone_1', 'telefone_2', 'link_facebook',
                  'link_instagram', 'url_site', 'whatsapp', 'photo', 'file', 'cpf', 'cnpj', ]

    def __init__(self, *args, **kwargs):
        super(FormProfissional, self).__init__(*args, **kwargs)
        self.fields['user'].label = ''
        self.fields['user'].widget.attrs['class'] = 'hidden'
        self.fields['file'].label = 'Foto'
        self.fields['photo'].label = ''
        self.fields['photo'].widget.attrs['class'] = 'hidden'


class FormUser(ModelForm, BaseForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]

    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['username'].widget = forms.NumberInput()
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs['readonly'] = 'true'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].label = 'Nome'
        self.fields['last_name'].label = 'Sobrenome'

