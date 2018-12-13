from django.shortcuts import render


from produto.models import Produto,Pessoal,Categoria

from produto.forms import EstoqueForm

def index(request):
    return render(request, 'index.html')

#páginas estáticas
def quem_somos(request):
    if request.method == "GET":
        return render(request,"quem_somos.html");

def produtos(request):
    vidros = Produto.objects.all()

    produtos_disponiveis = []
    for produto in vidros:
        produtos_disponiveis.append({'produto': produto,
                                 'form': EstoqueForm(initial={'estoque': 0})})

    print(vidros)
    return render(request,"produtos.html", {'vidros' : produtos_disponiveis});

def pessoal(request):
    pessoal = Pessoal.objects.all()
    return render(request,"pessoal.html",{'pessoal': pessoal});

def depoiomentos(request):
    return render(request, "depoimentos.html");

def paginaInicial (request):
    return render(request,"index.html");