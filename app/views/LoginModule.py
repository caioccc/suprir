# coding=utf-8
import datetime
import random
from base64 import b64encode

import pyimgur
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import FormView, RedirectView
from djmoney.money import Money

from app.forms import FormLogin, FormRegisterCliente, FormRegisterProfissional
from app.mixins.CustomMixins import CustomContextMixin
from app.models import Cliente, Profissional, CategoriaDeProfissional, FormaPagamento, ComentarioServico, Servico, \
    FotoServico, CarrinhoDeServicos, ItemServico, ContratoDeServico, Entrada, Saida, Interesse, Proposta, Processo, TelegramBot


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
                profissional.is_online = True
                profissional.save()
                url = '/painel/'
                self.success_url = url
            elif cliente:
                cliente.is_online = True
                cliente.save()
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
        customuser = None
        try:
            customuser = self.request.user.cliente
        except (Exception,):
            print('Nao eh cliente')
        try:
            customuser = self.request.user.profissional
        except (Exception,):
            print('Nao eh profissional')
        try:
            customuser.is_online = False
            customuser.save()
        except (Exception,):
            print('Erro ao setar online offline no logout')
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
        if 'email' in data:
            user_data['email'] = data['email']
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
        if 'cpf' in data:
            data_pro['cpf'] = data['cpf']
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
        if 'email' in data:
            data_pro['email'] = data['email']
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
        if 'email' in data:
            user_data['email'] = data['email']
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
        if 'email' in data:
            data_pro['email'] = data['email']
        try:
            CLIENT_ID = "cdadf801dc167ab"
            bencode = b64encode(self.request.FILES['file'].read())
            client = pyimgur.Imgur(CLIENT_ID)
            r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': bencode})
            file = r['link']
            data_pro['photo'] = file
        except (Exception,):
            pass
        return data_pro


cidades = [
    {'cidade': 'Campina Grande', 'estado': 'PB'},
    {'cidade': 'Guarabira', 'estado': 'PB'},
    {'cidade': 'Recife', 'estado': 'PE'},
    {'cidade': 'Caruaru', 'estado': 'PE'},
    {'cidade': 'Natal', 'estado': 'RN'},
]

names = [
    'Joao',
    'Caio',
    'Paulo',
    'Luiz',
    'Fernando',
    'Pedro',
    'Jose',
    'Francisco',
    'Marcos'
]

surnames = [
    'Sousa',
    'Silva',
    'Barbosa',
    'Oliveira',
    'Santos',
    'Rodrigues',
    'Ferreira',
    'Alves',
    'Pereira'
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
        payments = ['CRÉDITO', 'DÉBITO', 'DINHEIRO', ]
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
        self.create_entradas_e_saidas()
        self.create_interesses()
        self.create_propostas()
        self.create_processos()
        logout(self.request)
        return super(StartTestSystem, self).get(request, *args, **kwargs)

    def create_user_default(self, number, id_custom="custom"):
        user = User.objects.create_user(number, '', '12345')
        user.first_name = str(names[random.randrange(len(names))])
        user.last_name = str(surnames[random.randrange(len(surnames))])
        user.email = 'caiomarinho8@gmail.com'
        user.save()
        return user

    def create_clients(self):
        for use in User.objects.all():
            if not use.is_superuser:
                use.delete()
        for i in range(10):
            number = '8399177303' + str(i)
            user = self.create_user_default(number=number, id_custom=i)
            sel_cidade = cidades[random.randrange(len(cidades))]
            client = Cliente(
                user=user,
                telefone_1=user.username,
                estado=sel_cidade['estado'],
                cidade=sel_cidade['cidade'],
                email='caiomarinho8@gmail.com',
                endereco='Rua Claudio Bezerra de Lima',
                numero='694',
                bairro='Tres Irmas',
                cep='58423530',
                cpf='10698646410'
            )
            client.save()
        return Cliente.objects.all()

    def create_profissionals(self):
        for pro in Profissional.objects.all():
            pro.delete()
        for i in range(10):
            number = '8398669766' + str(i)
            user = self.create_user_default(number=number, id_custom=i)
            sel_cidade = cidades[random.randrange(len(cidades))]
            telegramBot = TelegramBot(
                first_name='Caio',
                chat_id='451429199',
                last_name='Marinho',
                username='caiomarin'
            )
            telegramBot.save()
            prof = Profissional(
                categoria=CategoriaDeProfissional.objects.all().order_by('?').first(),
                is_approved=True,
                user=user,
                email='caiomarinho8@gmail.com',
                telefone_1=user.username,
                estado=sel_cidade['estado'],
                cidade=sel_cidade['cidade'],
                endereco='Rua Claudio Bezerra de Lima',
                numero='694',
                bairro='Tres Irmas',
                cep='58423530',
                cpf='10698646410',
                cnpj='61.152.872/0001-60',
                telegram_bot=telegramBot
            )
            prof.save()
        return Profissional.objects.all()

    def create_services(self):
        for serv in Servico.objects.all():
            serv.delete()
        valores = [Money(10.00, 'BRL'), Money(20.00, 'BRL'), Money(50.00, 'BRL'), Money(100.00, 'BRL'),
                   Money(130.00, 'BRL'), Money(150.00, 'BRL')]
        for prof in Profissional.objects.all():
            for i in range(2):
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
        valores = [Money(10.00, 'BRL'), Money(20.00, 'BRL'), Money(50.00, 'BRL'), Money(100.00, 'BRL'),
                   Money(130.00, 'BRL'), Money(150.00, 'BRL')]
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
        valores = [Money(10.00, 'BRL'), Money(20.00, 'BRL'), Money(50.00, 'BRL'), Money(100.00, 'BRL'),
                   Money(130.00, 'BRL'), Money(150.00, 'BRL')]
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
        payments = ['CRÉDITO', 'DÉBITO', 'DINHEIRO', ]
        for pay in payments:
            pay = FormaPagamento(forma=pay)
            pay.save()
        return FormaPagamento.objects.all()

    def get_days_between_dates(self):
        start_date = datetime.date(2020, 1, 1)
        end_date = datetime.date(2020, 5, 29)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        return days_between_dates

    def get_date_random(self):
        start_date = datetime.date(2020, 1, 1)
        days_between_dates = self.get_days_between_dates()
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        return random_date

    def create_entradas_e_saidas(self):
        for entr in Entrada.objects.all():
            entr.delete()
        for sai in Saida.objects.all():
            sai.delete()
        for profi in Profissional.objects.all():
            for dia in range(self.get_days_between_dates()):
                entrada = Entrada(
                    profissional=profi,
                    valor=Money(random.randint(10, 300), 'BRL'),
                    descricao='',
                    tipo_pagamento='CHEQUE',
                    cliente=names[random.randrange(len(names))],
                    telefone=83986697661,
                    data=self.get_date_random()
                )
                entrada.save()
                saida = Saida(
                    profissional=profi,
                    valor=Money(random.randint(10, 300), 'BRL'),
                    descricao='',
                    cliente=names[random.randrange(len(names))],
                    tipo_pagamento='CHEQUE',
                    telefone=83986697661,
                    data=self.get_date_random()
                )
                saida.save()

    def create_interesses(self):
        for inte in Interesse.objects.all():
            inte.delete()
        for profi in Profissional.objects.all():
            inte = Interesse(
                profissional_dono=profi,
                titulo='Preciso de tal coisa e tal coisa',
                descricao=''
            )
            inte.save()

    def create_propostas(self):
        for prop in Proposta.objects.all():
            prop.delete()
        for inte in Interesse.objects.all():
            for prof in Profissional.objects.all():
                if prof.pk != inte.profissional_dono.pk:
                    prop = Proposta(
                        profissional_socio=prof,
                        interesse=inte,
                        titulo='Ofereco em troca tal e tal coisa',
                        descricao=''
                    )
                    prop.save()

    def create_processos(self):
        for pro in Processo.objects.all():
            pro.delete()
        status = [
            'AGUARDANDO PAGAMENTO',
            'ABERTO', 'EM ANDAMENTO', 'REJEITADO', 'REALIZADO'
        ]
        for prop in Proposta.objects.all():
            new_status = status[random.randrange(len(status))]
            if new_status in ['EM ANDAMENTO', 'REJEITADO', 'REALIZADO']:
                prop.status = 'ACEITO'
                prop.save()
                proc = Processo(
                    profissional_socio=prop.profissional_socio,
                    profissional_dono=prop.interesse.profissional_dono,
                    titulo=prop.interesse.titulo,
                    interesse=prop.interesse,
                    proposta=prop,
                    descricao='',
                    status=new_status
                )
                proc.save()
