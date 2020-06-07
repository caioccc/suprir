# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, inlineformset_factory

from app.models import Profissional, CarrinhoDeServicos, ContratoDeServico, ItemServico, Servico, FotoServico, Mensagem, \
    Cliente, Cupom, Entrada, Saida, ComentarioServico, Interesse, Proposta, Processo


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
    cpf = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                        'maxlength': 100}))
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(FormRegisterCliente, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['required'] = 'True'
        self.fields['email'].widget.attrs['required'] = False
        self.fields['email'].required = False


class FormRegisterProfissional(ModelForm, FormRegisterCliente):
    class Meta:
        model = Profissional
        fields = ['categoria', 'file', 'email', 'telefone_2', 'link_facebook', 'link_instagram', 'url_site', 'cpf', 'cnpj']

    def __init__(self, *args, **kwargs):
        super(FormRegisterProfissional, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['required'] = False
        self.fields['file'].label = 'Foto (logotipo)'
        self.fields['link_facebook'].widget.attrs['required'] = False
        self.fields['link_instagram'].widget.attrs['required'] = False
        self.fields['url_site'].widget.attrs['required'] = False
        self.fields['telefone_2'].widget.attrs['required'] = False
        self.fields['cpf'].widget.attrs['required'] = False
        self.fields['cpf'].required = False
        self.fields['email'].widget.attrs['required'] = False
        self.fields['email'].required = False
        self.fields['cnpj'].widget.attrs['required'] = False


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

ItemServicoViewFormSet = inlineformset_factory(CarrinhoDeServicos, ItemServico,
                                               form=FormItemServico, extra=0)


class FormServico(ModelForm, BaseForm):
    class Meta:
        model = Servico
        fields = ['titulo', 'descricao', 'valor_base', 'disponivel', 'profissional']

    def __init__(self, *args, **kwargs):
        super(FormServico, self).__init__(*args, **kwargs)
        self.fields['valor_base'].label = 'Preço'
        self.fields['profissional'].label = ''
        self.fields['profissional'].widget.attrs['class'] = 'hidden'
        for field_name, field in self.fields.items():
            field.widget.attrs['required'] = True
        self.fields['disponivel'].widget.attrs['required'] = False


class FormFotoServico(ModelForm, BaseForm):
    class Meta:
        model = FotoServico
        fields = ['file', 'url']

    def __init__(self, *args, **kwargs):
        super(FormFotoServico, self).__init__(*args, **kwargs)
        self.fields['file'].label = 'Arquivo'
        self.fields['url'].label = ''
        self.fields['url'].widget.attrs['class'] = 'hidden'


FotoServicoFormSet = inlineformset_factory(Servico, FotoServico, form=FormFotoServico,
                                           extra=1, min_num=1, max_num=5)

FotoServicoViewFormSet = inlineformset_factory(Servico, FotoServico, form=FormFotoServico, extra=0,
                                               min_num=1, max_num=5)


class FormProfissional(ModelForm, BaseForm):
    class Meta:
        model = Profissional
        fields = ['categoria', 'user', 'telefone_1', 'telefone_2', 'link_facebook',
                  'link_instagram', 'url_site', 'whatsapp', 'photo', 'file', 'cpf', 'cnpj',
                  'cep', 'endereco', 'numero', 'cidade', 'estado', 'email']

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
        fields = ['username', 'first_name', 'last_name', ]

    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['username'].widget = forms.NumberInput()
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs['readonly'] = 'true'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].label = 'Nome'
        self.fields['last_name'].label = 'Sobrenome'


class ServicoSearchForm(BaseForm):
    query = forms.CharField(
        required=False,
        label='Busque por titulo ou categoria!',
        widget=forms.TextInput(attrs={'placeholder': 'Digite algum termo ...'})
    )
    CHOICES_ESTADO = [(state, state) for state in
                      Profissional.objects.order_by('estado').values_list('estado', flat=True).exclude(
                          estado=None).distinct()]
    CHOICES_ESTADO.append(('', 'Todos'))
    CHOICES_CIDADE = [(city, city) for city in
                      Profissional.objects.order_by('cidade').values_list('cidade', flat=True).exclude(
                          cidade=None).distinct()]
    CHOICES_CIDADE.append(('', 'Todos'))
    estado = forms.CharField(
        required=False,
        widget=forms.Select(choices=CHOICES_ESTADO)
    )
    cidade = forms.CharField(
        required=False,
        widget=forms.Select(choices=CHOICES_CIDADE)
    )
    preco_min = forms.IntegerField(
        required=False,
        label='Min',
        widget=forms.NumberInput(attrs={'placeholder': 'R$ 0'})
    )
    preco_max = forms.IntegerField(
        required=False,
        label='Max',
        widget=forms.NumberInput(attrs={'placeholder': 'R$ 1000'})
    )
    ordering = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(attrs={'class': 'hidden', })
    )


class ProfissionalSearchForm(BaseForm):
    query_p = forms.CharField(
        required=False,
        label='Busque por telefone',
        widget=forms.TextInput(attrs={'placeholder': 'Digite algum numero ...'})
    )
    CHOICES_ESTADO = [(state, state) for state in
                      Profissional.objects.order_by('estado').values_list('estado', flat=True).exclude(
                          estado=None).distinct()]
    CHOICES_ESTADO.append(('', 'Todos'))
    CHOICES_CIDADE = [(city, city) for city in
                      Profissional.objects.order_by('cidade').values_list('cidade', flat=True).exclude(
                          cidade=None).distinct()]
    CHOICES_CIDADE.append(('', 'Todos'))
    estado = forms.CharField(
        required=False,
        widget=forms.Select(choices=CHOICES_ESTADO)
    )
    cidade = forms.CharField(
        required=False,
        widget=forms.Select(choices=CHOICES_CIDADE)
    )
    ordering = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(attrs={'class': 'hidden', })
    )


class FormMensagem(ModelForm, BaseForm):
    class Meta:
        model = Mensagem
        fields = ['categoria', 'titulo', 'mensagem', 'nome', 'email',
                  'telefone', ]

    def __init__(self, *args, **kwargs):
        super(FormMensagem, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['required'] = 'True'
        self.fields['telefone'].widget.attrs['required'] = False


class FormRejeiteContrato(ModelForm, BaseForm):
    class Meta:
        model = ContratoDeServico
        fields = ['motivo', 'status', ]

    def __init__(self, *args, **kwargs):
        super(FormRejeiteContrato, self).__init__(*args, **kwargs)
        self.fields['status'].label = ''
        self.fields['status'].widget.attrs['class'] = 'hidden'


class FormEditCliente(ModelForm, BaseForm):
    class Meta:
        model = Cliente
        fields = ['telefone_1', 'email', 'whatsapp', 'photo', 'file', 'cpf', 'cep', 'endereco', 'numero', 'bairro', 'cidade',
                  'estado', ]

    def __init__(self, *args, **kwargs):
        super(FormEditCliente, self).__init__(*args, **kwargs)
        self.fields['file'].label = 'Arquivo de Foto'
        self.fields['photo'].label = ''
        self.fields['telefone_1'].label = 'Telefone Celular'
        self.fields['photo'].widget.attrs['class'] = 'hidden'


class FormCreateCupom(ModelForm, BaseForm):
    class Meta:
        model = Cupom
        fields = ['profissional', 'codigo', 'valor_de_desconto', ]

    def __init__(self, *args, **kwargs):
        super(FormCreateCupom, self).__init__(*args, **kwargs)
        self.fields['profissional'].widget.attrs['class'] = 'hidden'
        self.fields['profissional'].label = ''


class FormEditCupom(ModelForm, BaseForm):
    class Meta:
        model = Cupom
        fields = ['profissional', 'codigo', 'valor_de_desconto', 'is_approved', ]

    def __init__(self, *args, **kwargs):
        super(FormEditCupom, self).__init__(*args, **kwargs)
        self.fields['profissional'].widget.attrs['class'] = 'hidden'
        self.fields['profissional'].label = ''
        self.fields['is_approved'].label = 'Disponivel'
        self.fields['is_approved'].widget.attrs['class'] = ''


class FormEntrada(ModelForm, BaseForm):
    class Meta:
        model = Entrada
        fields = ['profissional', 'cliente', 'telefone', 'descricao', 'valor', 'tipo_pagamento', 'data', ]

    def __init__(self, *args, **kwargs):
        super(FormEntrada, self).__init__(*args, **kwargs)
        self.fields['telefone'].label = 'Telefone do Cliente'
        self.fields['profissional'].label = ''
        self.fields['profissional'].widget.attrs['class'] = 'hidden'
        self.fields['data'].widget.attrs['class'] = 'datepicker'


class FormSaida(ModelForm, BaseForm):
    class Meta:
        model = Saida
        fields = ['profissional', 'cliente', 'telefone', 'descricao', 'valor', 'tipo_pagamento', 'data', ]

    def __init__(self, *args, **kwargs):
        super(FormSaida, self).__init__(*args, **kwargs)
        self.fields['telefone'].label = 'Telefone do Cliente'
        self.fields['profissional'].label = ''
        self.fields['profissional'].widget.attrs['class'] = 'hidden'
        self.fields['data'].widget.attrs['class'] = 'datepicker'


class FormComentario(ModelForm, BaseForm):
    class Meta:
        model = ComentarioServico
        fields = ['servico', 'cliente', 'avaliacao', 'comentario', ]

    def __init__(self, *args, **kwargs):
        super(FormComentario, self).__init__(*args, **kwargs)
        self.fields['servico'].label = ''
        self.fields['servico'].widget.attrs['class'] = 'hidden'
        self.fields['cliente'].label = ''
        self.fields['cliente'].widget.attrs['class'] = 'hidden'


class FormContratoAvaliacao(ModelForm, BaseForm):
    class Meta:
        model = ContratoDeServico
        fields = ['is_avaliado', ]


class FormInteresse(ModelForm, BaseForm):
    class Meta:
        model = Interesse
        fields = ['profissional_dono', 'titulo']

    def __init__(self, *args, **kwargs):
        super(FormInteresse, self).__init__(*args, **kwargs)
        self.fields['titulo'].label = 'Informe seu interesse'
        self.fields['titulo'].widget.attrs['required'] = True
        self.fields['profissional_dono'].label = ''
        self.fields['profissional_dono'].widget.attrs['class'] = 'hidden'


class FormProposta(ModelForm, BaseForm):
    class Meta:
        model = Proposta
        fields = ['profissional_socio', 'titulo', 'interesse']

    def __init__(self, *args, **kwargs):
        super(FormProposta, self).__init__(*args, **kwargs)
        self.fields['titulo'].label = 'Informe sua proposta'
        self.fields['titulo'].widget.attrs['required'] = True
        self.fields['profissional_socio'].label = ''
        self.fields['profissional_socio'].widget.attrs['class'] = 'hidden'
        self.fields['interesse'].label = ''
        self.fields['interesse'].widget.attrs['class'] = 'hidden'


class FormProcesso(ModelForm, BaseForm):
    class Meta:
        model = Processo
        fields = ['profissional_socio', 'profissional_dono', 'interesse', 'proposta', 'titulo', ]

    def __init__(self, *args, **kwargs):
        super(FormProcesso, self).__init__(*args, **kwargs)
        self.fields['profissional_socio'].label = 'Profissional Socio'
        self.fields['profissional_dono'].label = 'Profissional de Abertura'
        self.fields['interesse'].label = ''
        self.fields['interesse'].widget.attrs['class'] = 'hidden'
        self.fields['proposta'].label = ''
        self.fields['proposta'].widget.attrs['class'] = 'hidden'
