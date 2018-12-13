from django.db.models import Sum, F, FloatField
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from produto.forms import ProdutoForm, RemoveProdutoForm, AtualizaProdutoForm
from produto.models import Produto
def cadastra_produto(request):

    produto_id = request.POST.get('id')
    print(produto_id)
    form = ProdutoForm(request.POST)
    if request.method == "POST":
        if produto_id:
            produto = get_object_or_404(Produto, pk=produto_id)

            # Como se trata de uma alteração, o objeto ProdutoForm é instanciado utilizando
            # os dados provenientes do banco de dados (instance=produto) e, em seguida,
            # essas informações são atualizadas utilizando os dados submetidos pelo usuário (request.POST).
            form_produto = ProdutoForm(request.POST, instance=produto)
            if form_produto.is_valid():
            # O método save() de ModelForm salva o produto (inclui ou altera) no banco de dados e retorna
            # um objeto do tipo Produto.
                produto = form_produto.save()

            # Se a variável produto_id for diferente de None então trata-se de uma alteração
                messages.add_message(request, messages.INFO, 'Produto Alterado com sucesso.')


                return redirect('produto:cadastra_produto')

        else:
            form = ProdutoForm(request.POST)
            acao = 'inclusao'
            form_produto = ProdutoForm(request.POST)
            print("GRETCHEN")
            # A linha de código abaixo testa se os dados constantes do form estão corretos.
            # As regras de validação foram definidas no form (ProdutoForm). Os campos categoria, nome, preco e
            # data_cadastro são de preenchimento obrigatório (required=True). E o campo preco deve obedecer a
            # uma expressão regular (veja em ProdutoForm)

            # Observe que o comando if abaixo não possui o "else". Caso ocorra um erro de validação a página
            # cadastra_produto.html será exibida novamente juntamente com as mensagens de erro.
            if form_produto.is_valid():
            # O método save() de ModelForm salva o produto (inclui ou altera) no banco de dados e retorna
            # um objeto do tipo Produto.
                print("bpoquete")
                produto = form_produto.save()

            # Se a variável produto_id for diferente de None então trata-se de uma alteração
                messages.add_message(request, messages.INFO, 'Produto cadastrado com sucesso.')


                return redirect('produto:cadastra_produto')


    else:
        form = ProdutoForm()

    produtos = Produto.objects.all()

    lista_de_produtos = []
    valor_do_estoque = 0
    ids_dos_produtos = []
    for produto in produtos:
        valor_do_estoque = valor_do_estoque + produto.preco * produto.estoque
        ids_dos_produtos.append(produto.id)
        lista_de_produtos.append({'produto': produto,
                                  'form': AtualizaProdutoForm(initial={'estoque': produto.estoque})})

    return render(request, 'produto/cadastra_produto.html', {'form': form,
                                                             'lista_de_produtos': lista_de_produtos,
                                                             'ids_dos_produtos': ids_dos_produtos,
                                                             'valor_do_estoque': valor_do_estoque})


def remove_produto(request):
    print('Entrou em remove_produto')
    form = RemoveProdutoForm(request.POST)
    if form.is_valid():
        produto = get_object_or_404(Produto, pk=form.cleaned_data['produto_id'])
        print(produto)
        #if request.user == produto.user:
        produto.delete()

        resultado = Produto.objects.filter(disponivel=True).aggregate(valor_do_estoque=Sum(F('estoque')*F('preco'), output_field=FloatField()))

        if resultado['valor_do_estoque']:
            return render(request, 'produto/valor_do_estoque.html', {'valor_do_estoque': '{0:.2f}'.format(resultado['valor_do_estoque'])})
        else:
            return render(request, 'produto/valor_do_estoque.html', {'valor_do_estoque': '0,00'})
        # return HttpResponse("{0:.2f}".format(resultado['valor_do_estoque']).replace('.',','))
    else:
        raise ValueError('Ocorreu um erro inesperado ao tentar remover um produto!')


def atualiza_produto(request,id):
    produto = get_object_or_404(Produto, pk=id)

    # Aqui instanciamos o objeto remove_produto_form para que os botões de edição e de remoção sejam exibidos.
    atualiza_produto_form = ProdutoForm(instance=produto)
    print(produto)
    print(atualiza_produto_form)
    return render(request, 'produto/atualiza_produto.html', {'produto': produto,
                                                             'form' : atualiza_produto_form,
                                                             'acao' : 'alteracao',
                                                             'id' : id})

#def atualiza_produto(request):
#    form = AtualizaProdutoForm(request.POST)
#    if form.is_valid():
#        produto = get_object_or_404(Produto, pk=form.cleaned_data['produto_id'])
#        produto.estoque = form.cleaned_data['estoque']
#        produto.save()

#        resultado = produto.objects.filter(disponivel=True).aggregate(valor_do_estoque=Sum(F('estoque')*F('preco'), output_field=FloatField()))
#        return render(request, 'produto/valor_do_estoque.html', {'valor_do_estoque': "{0:.2f}".format(resultado['valor_do_estoque'])})
        # return HttpResponse("{0:.2f}".format(resultado['valor_do_estoque']).replace('.',','))
#    else:
#        print(form.errors)
#        raise ValueError('Ocorreu um erro inesperado ao tentar alterar um produto!')


