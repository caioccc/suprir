from django.contrib import admin

# Register your models here.
from app.models import FotoServico, AdicionalDeServico, Servico, CarrinhoDeServicos, ItemServico, \
    AdicionalEscolhido, Cliente, CategoriaDeProfissional, Profissional, CategoriaDeServico, FormaPagamento, \
    ContratoDeServico, ComentarioServico, Mensagem, Cupom, ItemCupom, TelegramBot, RecycleTelegramItem, Entrada, Saida, Interesse, Proposta, Processo, EmailOuTelegramaAdmin
from app.views.TelegramAPI import get_chat_ids, send_mail_and_telegram


def approve_selected(modeladmin, request, queryset):
    queryset.update(is_approved=True)


def desapprove_selected(modeladmin, request, queryset):
    queryset.update(is_approved=False)


def abrir_processo_selected(modeladmin, request, queryset):
    print(queryset)
    send_mail_and_telegram(queryset.first().profissional_socio,
                           'A proposta depois de aceita, gerou um processo.\n Neste Processo, estamos aguardando o pagamento '
                           'das taxas para poder dar andamento ao processo e liberar o documento de contrato para ambos os profissionais. Por favor, acesse o sistema para realizar o pagamento, e '
                           'envie o comprovante para o administrador atraves do botao laranja AJUDA.',
                           'Processo em aberto aguardando pagamento.')
    queryset.update(status='ABERTO')


def dar_andamento_selected(modeladmin, request, queryset):
    proc = queryset.first()
    send_mail_and_telegram(proc.profissional_socio,
                           'Pagamento das taxas realizado com sucesso. O processo esta em andamento, e um documento de contrato foi gerado com sucesso. Por favor, acesso o sistema para verificar. Obrigado.',
                           'Processo em andamento.')
    send_mail_and_telegram(proc.profissional_dono,
                           'Pagamento das taxas realizado com sucesso. O processo esta em andamento, e um documento de contrato foi gerado com sucesso. Por favor, acesso o sistema para verificar. Obrigado.',
                           'Processo em andamento.')
    queryset.update(status='EM ANDAMENTO')


def get_new_itens(modeladmin, request, queryset):
    dic = get_chat_ids()
    if len(dic) > 0:
        for item in RecycleTelegramItem.objects.all():
            item.delete()
        for item in dic:
            rec = RecycleTelegramItem(chat_id=item['id'],
                                      first_name=item['first_name'],
                                      last_name=item['last_name'],
                                      username=item['username'])
            rec.save()


approve_selected.short_description = "Aprovar itens selecionados"
desapprove_selected.short_description = "Desaprovar itens selecionados"
get_new_itens.short_description = "Recuperar novos contatos"
dar_andamento_selected.short_description = "Dar Andamento aos itens selecionados"
abrir_processo_selected.short_description = "Abrir processos selecionados"


class FotoServicoInline(admin.TabularInline):
    model = FotoServico


class AdicionalDeServicoInline(admin.TabularInline):
    model = AdicionalDeServico


class ServicoInline(admin.TabularInline):
    model = Servico


class CarrinhoInline(admin.TabularInline):
    model = CarrinhoDeServicos


class ItemServicoInline(admin.TabularInline):
    model = ItemServico


class AdicionalEscolhidoInline(admin.TabularInline):
    model = AdicionalEscolhido


class ClienteAdmin(admin.ModelAdmin):
    list_filter = ('estado', 'cidade', 'is_online',)
    search_fields = (
        'user__first_name', 'cpf', 'cnpj',
    )
    inlines = [CarrinhoInline, ]
    list_display = (
        'id', 'user', 'nome_completo', 'estado', 'cidade', 'cpf', 'cnpj', 'telefone_1', 'whatsapp',
        'email', 'is_online',
        'created_at')

    def nome_completo(self, obj):
        return str(obj.user.first_name) + ' ' + str(obj.user.last_name)


class CategoriaDeProfissionalAdmin(admin.ModelAdmin):
    list_display = (
        'categoria', 'descricao', 'id', 'created_at',)


class ProfissionalAdmin(admin.ModelAdmin):
    list_filter = ('estado', 'cidade', 'categoria__categoria', 'is_approved')
    inlines = [
        ServicoInline,
    ]
    actions = [approve_selected, desapprove_selected]
    search_fields = (
        'user__first_name', 'cpf', 'cnpj',
    )
    list_display = (
        'user', 'id', 'nome_profissional', 'estado', 'cidade', 'categoria', 'telefone_1', 'cpf', 'cnpj',
        'is_approved', 'is_online', 'receber_pelo_sistema', 'email', 'telegram_bot', 'created_at',)

    def nome_profissional(self, obj):
        return obj.user.first_name


class CategoriaDeServicoAdmin(admin.ModelAdmin):
    list_filter = ('disponivel', 'is_approved',)
    actions = [approve_selected, desapprove_selected]
    search_fields = (
        'profissional__user__first_name', 'categoria', 'profissional__cpf', 'profissional__cnpj',
    )
    list_display = (
        'categoria', 'id', 'profissional', 'disponivel', 'is_approved', 'created_at',)


class ServicoAdmin(admin.ModelAdmin):
    list_filter = ('disponivel', 'is_approved',)
    inlines = [
        AdicionalDeServicoInline,
        FotoServicoInline
    ]
    actions = [approve_selected, desapprove_selected]
    search_fields = (
        'profissional__user__first_name', 'categoria__categoria',
    )
    list_display = (
        'titulo', 'id', 'categoria', 'valor_base', 'profissional', 'disponivel', 'is_approved', 'created_at')


class AdicionalDeServicoAdmin(admin.ModelAdmin):
    list_filter = ('disponivel', 'is_approved',)
    actions = [approve_selected, desapprove_selected]
    search_fields = (
        'servico__titulo',
    )
    list_display = ('titulo', 'id', 'servico', 'valor', 'disponivel', 'is_approved', 'created_at')


class FotoServicoAdmin(admin.ModelAdmin):
    list_filter = ('is_approved',)
    actions = [approve_selected, desapprove_selected]
    search_fields = (
        'servico__titulo',
    )
    list_display = ('servico', 'id', 'url', 'is_approved', 'created_at')


class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('forma', 'id', 'created_at')


class CarrinhoDeServicosAdmin(admin.ModelAdmin):
    list_filter = ('estado', 'cidade', 'forma_pagamento', 'status')
    inlines = [
        ItemServicoInline,
    ]
    search_fields = (
        'cliente__user__first_name', 'profissional__user__first_name', 'cliente__cpf', 'cliente__cnpj',
        'profissional__cpf', 'profissional__cnpj',
    )
    list_display = ('cliente', 'id', 'profissional', 'subtotal', 'cep', 'cidade', 'estado',
                    'valor_total', 'forma_pagamento', 'status', 'cupom', 'created_at')


class ItemServicoAdmin(admin.ModelAdmin):
    list_filter = ('servico__profissional__estado', 'servico__profissional__cidade', 'servico__disponivel')
    search_fields = (
        'servico__cliente__user__first_name', 'servico__profissional__user__first_name', 'servico__titulo',
        'servico__profissional__cpf', 'servico__profissional__cnpj',
    )
    inlines = [
        AdicionalEscolhidoInline,
    ]
    list_display = ('carrinho', 'id', 'servico', 'valor_total', 'created_at')


class AdicionalEscolhidoAdmin(admin.ModelAdmin):
    list_filter = (
        'item_servico__servico__profissional__estado', 'item_servico__servico__profissional__cidade',
        'item_servico__carrinho__forma_pagamento')
    search_fields = (
        'item_servico__servico__titulo', 'item_servico__servico__profissional__cpf',
        'item_servico__servico__profissional__cnpj',
    )
    list_display = ('adicional', 'id', 'item_servico', 'created_at')


class ContratoDeServicoAdmin(admin.ModelAdmin):
    list_filter = (
        'carrinho__profissional__estado', 'carrinho__profissional__cidade', 'carrinho__forma_pagamento',
        'is_avaliado')
    search_fields = (
        'carrinho__cliente__user__first_name', 'carrinho__profissional__user__first_name',
        'carrinho__profissional__cpf',
        'carrinho__profissional__cnpj', 'carrinho__cliente__cpf', 'carrinho__cliente__cnpj',
    )
    list_display = ('carrinho', 'id', 'status', 'motivo', 'is_avaliado', 'created_at')


class ComentarioServicoAdmin(admin.ModelAdmin):
    list_filter = (
        'cliente__estado', 'cliente__cidade',)
    search_fields = (
        'cliente__user__first_name', 'cliente__cpf',
        'cliente__cnpj',
    )
    list_display = ('servico', 'id', 'cliente', 'avaliacao', 'created_at')


class MensagemAdmin(admin.ModelAdmin):
    list_filter = ('categoria', 'resolvido',)
    search_fields = (
        'telefone', 'mensagem', 'nome',
    )
    list_display = ('categoria', 'titulo', 'mensagem', 'id', 'nome', 'email', 'telefone', 'resolvido', 'created_at')


class CupomAdmin(admin.ModelAdmin):
    list_filter = ('is_approved',)
    search_fields = (
        'codigo', 'valor_de_desconto',
    )
    list_display = ('codigo', 'profissional', 'valor_de_desconto', 'id', 'created_at')


class ItemCupomAdmin(admin.ModelAdmin):
    list_display = ('cupom', 'created_at')


class TelegramBotAdmin(admin.ModelAdmin):
    list_filter = ('is_approved',)
    search_fields = (
        'chat_id', 'first_name',
    )
    list_display = ('chat_id', 'id', 'first_name', 'last_name', 'username', 'is_approved', 'created_at')


class RecycleTelegramItemAdmin(admin.ModelAdmin):
    search_fields = (
        'chat_id', 'first_name',
    )
    list_display = ('chat_id', 'id', 'first_name', 'last_name', 'username', 'created_at')
    actions = [get_new_itens, ]


class EntradaAdmin(admin.ModelAdmin):
    list_filter = ('profissional', 'tipo_pagamento')
    search_fields = (
        'cliente',
    )
    list_display = ('profissional', 'id', 'valor', 'descricao', 'cliente', 'telefone', 'data', 'tipo_pagamento',
                    'created_at')


class SaidaAdmin(admin.ModelAdmin):
    list_filter = ('profissional', 'tipo_pagamento')
    search_fields = (
        'cliente',
    )
    list_display = ('profissional', 'id', 'valor', 'descricao', 'cliente', 'telefone', 'data', 'tipo_pagamento',
                    'created_at')


class InteresseAdmin(admin.ModelAdmin):
    search_fields = (
        'titulo',
    )
    list_display = ('profissional_dono', 'id', 'titulo', 'descricao', 'status', 'created_at')


class PropostaAdmin(admin.ModelAdmin):
    search_fields = (
        'titulo',
    )
    list_display = ('profissional_socio', 'id', 'titulo', 'interesse', 'descricao', 'status', 'created_at')


class ProcessoAdmin(admin.ModelAdmin):
    search_fields = (
        'titulo',
    )
    actions = [dar_andamento_selected, abrir_processo_selected]
    list_display = ('profissional_dono', 'profissional_socio', 'id', 'titulo',
                    'interesse', 'proposta', 'descricao', 'status', 'motivo', 'created_at')


class MensagemAdminAdmin(admin.ModelAdmin):
    search_fields = (
        'user__first_name',
    )
    list_display = ('user', 'message', 'id', 'title', 'enviado', 'created_at')


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Profissional, ProfissionalAdmin)
admin.site.register(CategoriaDeProfissional, CategoriaDeProfissionalAdmin)
admin.site.register(CategoriaDeServico, CategoriaDeServicoAdmin)
admin.site.register(Servico, ServicoAdmin)
admin.site.register(AdicionalDeServico, AdicionalDeServicoAdmin)
admin.site.register(FotoServico, FotoServicoAdmin)
admin.site.register(FormaPagamento, FormaPagamentoAdmin)
admin.site.register(CarrinhoDeServicos, CarrinhoDeServicosAdmin)
admin.site.register(ItemServico, ItemServicoAdmin)
admin.site.register(AdicionalEscolhido, AdicionalEscolhidoAdmin)
admin.site.register(ContratoDeServico, ContratoDeServicoAdmin)
admin.site.register(ComentarioServico, ComentarioServicoAdmin)
admin.site.register(Mensagem, MensagemAdmin)
admin.site.register(Cupom, CupomAdmin)
admin.site.register(ItemCupom, ItemCupomAdmin)
admin.site.register(TelegramBot, TelegramBotAdmin)
admin.site.register(RecycleTelegramItem, RecycleTelegramItemAdmin)
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(Saida, SaidaAdmin)
admin.site.register(Interesse, InteresseAdmin)
admin.site.register(Proposta, PropostaAdmin)
admin.site.register(Processo, ProcessoAdmin)
admin.site.register(EmailOuTelegramaAdmin, MensagemAdminAdmin)
