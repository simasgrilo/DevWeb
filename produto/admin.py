from django.contrib import admin
from .models import Categoria, Produto

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    search_fields = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}
admin.site.register(Categoria, CategoriaAdmin)

class ProdutoAdmin(admin.ModelAdmin):
    # fields = ('categoria', 'nome', 'slug', 'descricao', 'preco', 'estoque')
    list_display = ['nome', 'categoria', 'preco']
    search_fields = ('nome', 'categoria')
    list_filter = ['categoria']
    list_editable = ['preco']
admin.site.register(Produto, ProdutoAdmin)
