from django.urls import path
from . import views

app_name = 'produto'

from django.contrib.auth import views as auth_views
#from .autenticacao.forms import AutenticationFormCustomizado

#a partir de atualiza_produto, são páginas estáticas
urlpatterns = [
    path('cadastra_produto/', views.cadastra_produto, name='cadastra_produto'),
    path('remove_produto/', views.remove_produto, name='remove_produto'),
    path('atualiza_produto/<int:id>', views.atualiza_produto, name='atualiza_produto')

]
