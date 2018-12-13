from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render

from carrinho.carrinho import Carrinho
from carrinho.form import EstoqueForm, RemoveProdutoDoCarrinhoForm
from produto.models import Produto

def exibe_produtos_e_carrinho(request):
    return render(request, 'carrinho/vendas.html')


def exibe_produtos(request):

    produtos = Produto.objects.filter(disponivel=True)
    produtos_a_venda = []
    for produto in produtos:
        produtos_a_venda.append({'produto': produto,
                                 'form': EstoqueForm(initial={'estoque': 0})})

    return render(request, 'carrinho/produtos_a_venda.html',  {'produtos_a_venda': produtos_a_venda})


def exibe_carrinho(request):

    carrinho = Carrinho(request)

    lista_de_produtos_no_carrinho = carrinho.get_lista_de_produtos()
    produtos_no_carrinho = []
    valor_do_carrinho = 0
    for item in lista_de_produtos_no_carrinho:
        valor_do_carrinho = valor_do_carrinho + int(item['quantidade']) * Decimal(item['preco'])
        produtos_no_carrinho.append({'produto': item['produto'],
                                     'form': EstoqueForm(initial={'estoque': item['quantidade']})})

    return render(request, 'carrinho/produtos_no_carrinho.html',  {'produtos_no_carrinho': produtos_no_carrinho,
                                                                   'valor_do_carrinho': valor_do_carrinho})


def adicionar_ao_carrinho(request):
    form = EstoqueForm(request.POST)
    print("anus")
    if form.is_valid():
        estoque = form.cleaned_data['estoque']
        produto_id = form.cleaned_data['produto_id']

        carrinho = Carrinho(request)
        carrinho.adicionar(produto_id, estoque)

        messages.add_message(request, messages.INFO, 'Produto cadastrado com sucesso.')
        return render(request,"produtos.html")
        #return exibe_carrinho(request)
    else:
        raise ValueError('Ocorreu um erro inesperado ao adicionar um produto ao carrinho.')


def remove_produto_carrinho(request):
    form = RemoveProdutoDoCarrinhoForm(request.POST)
    if form.is_valid():
        carrinho = Carrinho(request)
        carrinho.remover(form.cleaned_data['produto_id'])

        return exibe_carrinho(request)
    else:
        #print(form.errors) p/ debug
        raise ValueError('Ocorreu um erro inesperado ao adicionar um produto ao carrinho.')


def atualiza_qtd_carrinho(request):
    form = EstoqueForm(request.POST)
    if form.is_valid():
        produto_id = form.cleaned_data['produto_id']
        estoque =  form.cleaned_data['estoque']

        carrinho = Carrinho(request)
        carrinho.alterar(produto_id, estoque)

        return exibe_carrinho(request)
    else:
        # print(form.errors) p/ debug
        raise ValueError('Ocorreu um erro inesperado ao adicionar um produto ao carrinho.')
