from decimal import Decimal
from django.conf import settings

from produto.models import Produto

class Carrinho(object):

    def __init__(self, request):
        """ Initializa o carrinho de compras. """

        #deixa pública a sessão da request que criou o carrinho
        self.session = request.session

        # recupera o carrinho da sessão e o salva na variável de instância carrinho
        self.carrinho = self.session.get(settings.CARRINHO_SESSION_ID)

        # Se a sessão não tiver um carrinho
        if not self.carrinho:
            # cria um carrinho vazio e o salva na sessão, e na variável de instância carrinho.
            # carrinho é um dicionário que irá conter pares de chave e valor. A chave será o id de um produto
            # e o valor será um dicionário contendo o id do produto, a quantidade e o preço.
            self.carrinho = self.session[settings.CARRINHO_SESSION_ID] = {}

        # Observação:
        # -----------
        # Nosso dicionário para o carrinho deve utilizar ids dos produtos como chaves e um dicionário com o id do produto,
        # a quantidade e o preço, como valor. Fazendo isso, podemos garantir que um produto não é adicionado mais de
        # uma vez no carrinho.
        #
        # print(carrinho)  # {1: {'id': 1, 'quantidade': 10, 'preco': '100'}}

    def __len__(self):
        """ Conta todos os itens no carrinho. """
        return sum(item['quantidade'] for item in self.carrinho.values())

    def get_lista_de_produtos(self):

        lista = []
        for item in self.carrinho.values():
            produto = Produto.objects.get(id=item['id'])#adiciono no carrinho o objeto com o id correspondente.
            #assim como Produto.objects.all(), get é um metodo da classe MOdels que recupera o item de acordo com algum atributo
            lista.append({'produto': produto,
                          'preco': item['preco'],
                          'quantidade': item['quantidade']})

        return lista



    def adicionar(self, id, quantidade):
        """ Adiciona um produto ao carrinho ou atualiza suas quantidades. """

        produto = Produto.objects.get(id=id)
        produto_id = str(id)

        if produto_id not in self.carrinho:
            #coloco item no carrinho
            self.carrinho[produto_id] = {'id': produto_id, 'preco': str(produto.preco), 'quantidade': quantidade}
        else:
            #se já tiver lá só modifico a quantidade com o selecionado
            self.carrinho[produto_id]['quantidade'] += quantidade

        print("Passou 6")
        self.salvar()


    def alterar(self, id, quantidade):
        """ Adiciona um produto ao carrinho ou atualiza suas quantidades. """
        produto_id = str(id)

        if produto_id in self.carrinho:
            self.carrinho[produto_id]['quantidade'] = quantidade
            self.salvar()  # O método salvar é chamado para que o carrinho
                           # seja salvo na sessão.
        else:
            print("Passou 3")
            self.adicionar(id, quantidade)

        print("Passou 8")


    def remover(self, id):
        """ Remove a produto from the carrinho. """
        print("remover id = ", id)
        produto_id = str(id)

        print("remover self.carrinho = ", self.carrinho)
        if produto_id in self.carrinho:
            del self.carrinho[produto_id] #retiro o objeto do dicionário que é o carrinho
            self.salvar()  #atualizo a modificação no objeto sessão
        print("remover self.carrinho = ", self.carrinho)


    def salvar(self):
        # atualiza o carrinho na sessão
        self.session[settings.CARRINHO_SESSION_ID] = self.carrinho

    def limpar(self):
        # Esvazia o carrinho
        self.session[settings.CARRINHO_SESSION_ID] = {}
        # self.session.modified = True

    def get_preco_total(self):
        return sum(Decimal(item['preco']) * item['quantidade'] for item in self.carrinho.values())
