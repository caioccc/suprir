from django.contrib import admin


# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    search_fields = (
        'user__first_name',
    )
    list_display = (
        'id', 'user', 'nome_completo', 'estado', 'cidade', 'cpf', 'cnpj', 'telefone_1', 'whatsapp', 'is_online',
        'created_at')

    def nome_completo(self, obj):
        return str(obj.user.first_name) + ' ' + str(obj.user.last_name)


class CategoriaDeProfissionalAdmin(admin.ModelAdmin):
    list_display = (
        'categoria', 'id', 'created_at')


class ProfissionalAdmin(admin.ModelAdmin):
    list_filter = ('estado', 'cidade', 'categoria__categoria')
    search_fields = (
        'user__first_name', 'cpf'
    )
    list_display = (
        'user', 'id', 'nome_profissional', 'estado', 'cidade', 'categoria', 'telefone_1', 'whatsapp', 'cpf', 'cnpj',
        'is_approved', 'is_online', 'created_at')

    def nome_profissional(self, obj):
        return obj.user.first_name


class CategoriaDeServicoAdmin(admin.ModelAdmin):
    list_filter = ('disponivel')
    search_fields = (
        'profissional__user__first_name', 'categoria'
    )
    list_display = (
        'categoria', 'id', 'profissional', 'disponivel', 'created_at')


class ServicoAdmin(admin.ModelAdmin):
    list_filter = ('disponivel')
    search_fields = (
        'profissional__user__first_name', 'categoria__categoria'
    )
    list_display = ('titulo', 'id', 'categoria', 'valor_base', 'profissional', 'disponivel', 'created_at')


class AdicionalDeServicoAdmin(admin.ModelAdmin):
    list_filter = ('disponivel')
    search_fields = (
        'servico__titulo'
    )
    list_display = ('titulo', 'id', 'servico', 'valor', 'disponivel', 'created_at')


class FotoServicoAdmin(admin.ModelAdmin):
    search_fields = (
        'servico__titulo'
    )
    list_display = ('servico', 'id', 'url', 'created_at')


class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('forma', 'id', 'created_at')
