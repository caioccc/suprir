# coding=utf-8
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import FormView, RedirectView

from app.forms import FormLogin, FormRegisterCliente, FormRegisterProfissional
from app.models import Cliente, Profissional, CategoriaDeProfissional, FormaPagamento, ComentarioServico, Servico, \
    FotoServico, CarrinhoDeServicos, ItemServico, ContratoDeServico
from app.views.StoreModule import CustomContextMixin


class LoginView(CustomContextMixin, FormView):
    """
    Displays the login form.
    """
    template_name = 'login.html'
    form_class = FormLogin
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(**data)
        print(user)
        try:
            profissional = user.profissional
            if not profissional.is_approved:
                messages.error(self.request, 'Usuário ainda não foi aprovado. Aguarde 24 horas!')
                return self.form_invalid(form)
        except (Exception,):
            pass

        if user is not None:
            login(self.request, user)
        else:
            messages.error(self.request, 'Nenhum usuário encontrado')
            return self.form_invalid(form)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        url = '/'
        profissional = None
        cliente = None
        try:
            user = self.request.user
        except (Exception,):
            user = None
        try:
            profissional = user.profissional
        except (Exception,):
            pass

        try:
            cliente = user.cliente
        except (Exception,):
            pass

        if user:
            if profissional:
                url = '/painel/'
                self.success_url = url
            elif cliente:
                url = '/'
                self.success_url = url
            elif user.is_superuser:
                url = '/admin/'
                self.success_url = url
            else:
                url = '/'
                self.success_url = url
        else:
            url = '/'
            self.success_url = url
        return url


class LogoutView(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegistroCliente(CustomContextMixin, FormView):
    template_name = 'register-client.html'
    form_class = FormRegisterCliente
    success_url = '/login/'

    def get(self, request, *args, **kwargs):
        return super(RegistroCliente, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('')
        return super(RegistroCliente, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        user_data = {}
        if len(data['telefone']) < 10:
            messages.error(self.request, 'Insira um Telefone valido')
            return self.form_invalid(form)
        if len(data['password']) < 5:
            messages.error(self.request, 'Insira uma senha maior que 5 caracteres')
            return self.form_invalid(form)
        user_data['username'] = data['telefone']
        user_data['first_name'] = data['nome']
        user_data['last_name'] = data['sobrenome']
        user_data['password'] = data['password']
        data_address_client = self.get_address_client(data)
        try:
            user = User.objects.create_user(**user_data)
            cliente = Cliente(
                telefone_1=data['telefone'],
                user=user,
                whatsapp=data['telefone'],
                **data_address_client
            )
            cliente.save()
        except (Exception,):
            messages.error(self.request, 'Ja existe uma conta com este numero')
            return self.form_invalid(form)
        messages.success(self.request, 'Registrado com Sucesso')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super(RegistroCliente, self).form_invalid(form)

    def get_address_client(self, data):
        data_pro = {}
        if 'cep' in data:
            data_pro['cep'] = data['cep']
        if 'bairro' in data:
            data_pro['bairro'] = data['bairro']
        if 'endereco' in data:
            data_pro['endereco'] = data['endereco']
        if 'numero' in data:
            data_pro['numero'] = data['numero']
        if 'cidade' in data:
            data_pro['cidade'] = data['cidade']
        if 'estado' in data:
            data_pro['estado'] = str(data['estado']).upper()
        return data_pro


class RegistroProfissional(CustomContextMixin, FormView):
    template_name = 'register-profissional.html'
    form_class = FormRegisterProfissional
    success_url = '/login/'

    def get(self, request, *args, **kwargs):
        return super(RegistroProfissional, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('')
        return super(RegistroProfissional, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        user_data = {}
        if len(data['telefone']) < 10:
            messages.error(self.request, 'Insira um Telefone valido')
            return self.form_invalid(form)
        if len(data['password']) < 5:
            messages.error(self.request, 'Insira uma senha maior que 5 caracteres')
            return self.form_invalid(form)
        user_data['username'] = data['telefone']
        user_data['first_name'] = data['nome']
        user_data['last_name'] = data['sobrenome']
        user_data['password'] = data['password']
        data_pro = self.get_profissional_data(data)
        try:
            user = User.objects.create_user(**user_data)
            profissional = Profissional(
                telefone_1=data['telefone'],
                user=user,
                **data_pro
            )
            profissional.save()
        except (Exception,):
            messages.error(self.request, 'Ja existe uma conta com este numero')
            return self.form_invalid(form)
        messages.success(self.request, 'Registrado com Sucesso. Aguarde 24 horas para ser aprovado!')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super(RegistroProfissional, self).form_invalid(form)

    def get_profissional_data(self, data):
        data_pro = {}
        if 'cpf' in data:
            data_pro['cpf'] = data['cpf']
        if 'cnpj' in data:
            data_pro['cnpj'] = data['cnpj']
        if 'cep' in data:
            data_pro['cep'] = data['cep']
        if 'bairro' in data:
            data_pro['bairro'] = data['bairro']
        if 'endereco' in data:
            data_pro['endereco'] = data['endereco']
        if 'numero' in data:
            data_pro['numero'] = data['numero']
        if 'cidade' in data:
            data_pro['cidade'] = data['cidade']
        if 'estado' in data:
            data_pro['estado'] = str(data['estado']).upper()
        if 'telefone_2' in data:
            data_pro['telefone_2'] = data['telefone_2']
            data_pro['whatsapp'] = data['telefone_2']
        if 'categoria' in data:
            data_pro['categoria'] = data['categoria']
        if 'link_facebook' in data:
            data_pro['link_facebook'] = data['link_facebook']
        if 'link_instagram' in data:
            data_pro['link_instagram'] = data['link_instagram']
        if 'url_site' in data:
            data_pro['url_site'] = data['url_site']
        return data_pro


cidades = [
    {'cidade': 'Campina Grande', 'estado': 'PB'},
    {'cidade': 'Guarabira', 'estado': 'PB'},
    {'cidade': 'Recife', 'estado': 'PE'},
    {'cidade': 'Caruaru', 'estado': 'PE'},
    {'cidade': 'Natal', 'estado': 'RN'},
]


class StartSystem(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        self.create_categories()
        self.create_payments_form()
        logout(self.request)
        return super(StartSystem, self).get(request, *args, **kwargs)

    def create_categories(self):
        for catego in CategoriaDeProfissional.objects.all():
            catego.delete()
        categories = [
            'Serviços de informática',
            'Serviços prestados mediante locação',
            'Serviços de saúde, assistência médica e congêneres',
            'Serviços de medicina e assistência veterinária',
            'Serviços de cuidados pessoais, estética e atividades físicas',
            'Serviços relativos a engenharia, arquitetura, geologia, urbanismo, construção civil',
            'Serviços relativos a manutenção, limpeza, meio ambiente, saneamento e congêneres',
            'Serviços de educação, ensino, orientação pedagógica e educacional, instrução, treinamento',
            'Serviços relativos a hospedagem, turismo, viagens e congêneres',
            'Serviços de intermediação e congêneres',
            'Serviços de guarda, estacionamento, armazenamento, vigilância e congêneres',
            'Serviços de diversões, lazer, entretenimento e congêneres',
            'Serviços relativos a fonografia, fotografia, cinematografia e reprografia',
            'Serviços relacionados ao setor bancário ou financeiro',
            'Serviços de transporte',
            'Serviços de apoio técnico, administrativo, jurídico, contábil, comercial',
            'Serviços de comunicação visual, desenho industrial',
            'Serviços funerários',
            'Serviços técnicos em edificações, eletrônica, eletrotécnica, mecânica, telecomunicações',
        ]
        for categorie in categories:
            cat = CategoriaDeProfissional(categoria=categorie)
            cat.save()
        return CategoriaDeProfissional.objects.all()

    def create_payments_form(self):
        for paym in FormaPagamento.objects.all():
            paym.delete()
        payments = ['BOLETO', 'CRÉDITO', 'DÉBITO', 'DINHEIRO', ]
        for pay in payments:
            pay = FormaPagamento(forma=pay)
            pay.save()


class StartTestSystem(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        self.create_categories()
        self.create_clients()
        self.create_profissionals()
        self.create_services()
        self.create_payments_form()
        self.create_carts()
        self.create_contracts()
        self.create_comments()
        logout(self.request)
        return super(StartTestSystem, self).get(request, *args, **kwargs)

    def create_user_default(self, number, name, id_custom="custom"):
        user = User.objects.create_user(number, '', '12345')
        user.first_name = str(name + str(id_custom))
        user.last_name = 'Test'
        user.save()
        return user

    def create_clients(self):
        for use in User.objects.all():
            if not use.is_superuser:
                use.delete()
        for i in range(10):
            number = '8399177303' + str(i)
            user = self.create_user_default(number=number, name='Cliente ', id_custom=i)
            sel_cidade = cidades[random.randrange(len(cidades))]
            client = Cliente(
                user=user,
                telefone_1=user.username,
                estado=sel_cidade['estado'],
                cidade=sel_cidade['cidade']
            )
            client.save()
        return Cliente.objects.all()

    def create_profissionals(self):
        for pro in Profissional.objects.all():
            pro.delete()
        for i in range(10):
            number = '8398669766' + str(i)
            user = self.create_user_default(number=number, name='Profissional ', id_custom=i)
            sel_cidade = cidades[random.randrange(len(cidades))]
            prof = Profissional(
                categoria=CategoriaDeProfissional.objects.all().order_by('?').first(),
                is_approved=True,
                user=user,
                telefone_1=user.username,
                estado=sel_cidade['estado'],
                cidade=sel_cidade['cidade']
            )
            prof.save()
        return Profissional.objects.all()

    def create_services(self):
        for serv in Servico.objects.all():
            serv.delete()
        valores = ['10.00', '50.00', '100.00', '30.00', '130.00', '150.00']
        for prof in Profissional.objects.all():
            for i in range(3):
                servico = Servico(
                    titulo=str('Serviço a prestar ' + str(i)),
                    descricao='Take it as demo specs, ipsum dolor sit amet, consectetuer adipiscing elit, Lorem ipsum dolor sit amet, consectetuer adipiscing elit, Ut wisi enim ad minim sint occaecat cupidatat non proident, sunt in culpa qui laborum....',
                    valor_base=valores[random.randrange(len(valores))],
                    profissional=prof,
                    is_approved=True
                )
                servico.save()
                foto = FotoServico(servico=servico)
                foto.save()
        return Servico.objects.all()

    def create_carts(self):
        for car in CarrinhoDeServicos.objects.all():
            car.delete()
        valores = ['10.00', '50.00', '100.00', '30.00', '130.00', '150.00']
        for client in Cliente.objects.all():
            for i in range(2):
                pro = Profissional.objects.all().order_by('?').first()
                cart = CarrinhoDeServicos(
                    cliente=client,
                    profissional=pro,
                    forma_pagamento=FormaPagamento.objects.all().order_by('?').first()
                )
                cart.save()
                itemservico = ItemServico(
                    carrinho=cart,
                    servico=Servico.objects.filter(profissional=pro).order_by('?').first(),
                    valor_total=valores[random.randrange(len(valores))]
                )
                itemservico.save()
                cart.save()
        return CarrinhoDeServicos.objects.all()

    def create_contracts(self):
        for contract in ContratoDeServico.objects.all():
            contract.delete()
        valores = ['10.00', '50.00', '100.00', '30.00', '130.00', '150.00']
        status = ['EM ANDAMENTO', 'REALIZADO', 'REJEITADO', ]
        for profi in Profissional.objects.all():
            for i in range(15):
                client = Cliente.objects.all().order_by('?').first()
                cart = CarrinhoDeServicos(
                    cliente=client,
                    profissional=profi,
                    forma_pagamento=FormaPagamento.objects.all().order_by('?').first(),
                    status=False
                )
                cart.save()
                itemservico = ItemServico(
                    carrinho=cart,
                    servico=Servico.objects.filter(profissional=profi).order_by('?').first(),
                    valor_total=valores[random.randrange(len(valores))]
                )
                itemservico.save()
                cart.save()
                contract = ContratoDeServico(
                    carrinho=cart,
                    status=status[random.randrange(len(status))],
                    cliente=client,
                    profissional=profi
                )
                contract.save()
        return ContratoDeServico.objects.all()

    def get_random_client(self):
        return Cliente.objects.all().order_by('?').first()

    def create_comments(self):
        for comment in ComentarioServico.objects.all():
            comment.delete()
        avaliacoes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        comentarios = [
            "Compensa pagar um pouco mais para ter mais conforto",
            "Excelente",
            "Bom Custo Benefício",
            "Soberbo",
            "Ótimo e barato",
            "Tudo perfeito",
            "Tem minha preferência",
        ]
        for servico in Servico.objects.all():
            for i in range(5):
                cliente = self.get_random_client()
                comm = ComentarioServico(servico=servico, cliente=cliente,
                                         comentario=comentarios[random.randrange(len(comentarios))],
                                         avaliacao=avaliacoes[random.randrange(len(avaliacoes))])
                comm.save()
        return ComentarioServico.objects.all()

    def create_categories(self):
        for catego in CategoriaDeProfissional.objects.all():
            catego.delete()
        categories = [
            {
                'categoria': 'Informática',
                'desc': 'Serviços de informática'
            },
            {
                'categoria': 'Locação',
                'desc': 'Serviços prestados mediante locação'
            },
            {
                'categoria': 'Saúde',
                'desc': 'Serviços de saúde, medicina, assistência médica, medicina veterinária e congêneres'
            },
            {
                'categoria': 'Cuidados Pessoais',
                'desc': 'Serviços de cuidados pessoais, estética, atividades físicas e congêneres'
            },
            {
                'categoria': 'Construção Civil',
                'desc': 'Serviços relativos a engenharia, arquitetura, geologia, urbanismo, construção civil'
            },
            {
                'categoria': 'Manutenção e Limpeza',
                'desc': 'Serviços relativos a manutenção, limpeza, meio ambiente, saneamento e congêneres'
            },
            {
                'categoria': 'Turismo',
                'desc': 'Serviços relativos a hospedagem, turismo, viagens e congêneres'
            },
            {
                'categoria': 'Educação',
                'desc': 'Serviços de educação, ensino, orientação pedagógica e educacional, instrução, treinamento'
            },
            {
                'categoria': 'Intermediação',
                'desc': 'Serviços de intermediação e congêneres'
            },
            {
                'categoria': 'Vigilância',
                'desc': 'Serviços de guarda, estacionamento, armazenamento, vigilância e congêneres'
            },
            {
                'categoria': 'Entretenimento',
                'desc': 'Serviços de diversões, lazer, entretenimento e congêneres'
            },
            {
                'categoria': 'Fotografia e Cinema',
                'desc': 'Serviços relativos a fonografia, fotografia, cinematografia e reprografia'
            },
            {
                'categoria': 'Financeiro',
                'desc': 'Serviços relacionados ao setor bancário ou financeiro'
            },
            {
                'categoria': 'Transporte',
                'desc': 'Serviços de transporte'
            },
            {
                'categoria': 'Jurídico',
                'desc': 'Serviços de apoio técnico, administrativo, jurídico, contábil, comercial'
            },
            {
                'categoria': 'Comunicação Visual',
                'desc': 'Serviços de comunicação visual, desenho industrial'
            },
            {
                'categoria': 'Funerário',
                'desc': 'Serviços funerários'
            },
            {
                'categoria': 'Técnico',
                'desc': 'Serviços técnicos em edificações, eletrônica, eletrotécnica, mecânica, telecomunicações'
            },
        ]
        for obj in categories:
            cat = CategoriaDeProfissional(categoria=obj['categoria'], descricao=obj['desc'])
            cat.save()
        return CategoriaDeProfissional.objects.all()

    def create_payments_form(self):
        for paym in FormaPagamento.objects.all():
            paym.delete()
        payments = ['BOLETO', 'CRÉDITO', 'DÉBITO', 'DINHEIRO', ]
        for pay in payments:
            pay = FormaPagamento(forma=pay)
            pay.save()
        return FormaPagamento.objects.all()
