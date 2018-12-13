from django.conf import settings
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nome

class Produto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='operacoes_do_usuario',
                             on_delete=models.DO_NOTHING,
                             null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=120)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    disponivel = models.BooleanField(default=True)
    data_de_cadastro = models.DateField(null=True)
    tooltip = models.CharField(max_length=1000)
    foto = models.CharField(max_length=1000)

    class Meta:
        db_table = 'produto'

    def __str__(self):
        return self.nome

    def data_cadastro_masc(self):
        return self.data_de_cadastro.strftime("%d/%m/%Y")

class Pessoal(models.Model):
    nome = models.CharField(max_length=120)
    foto = models.CharField(max_length=400)
    descricao = models.CharField(max_length=1000)

    class Meta:
        db_table = 'pessoal'

    def __str__(self):
        return self.nome


