from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True) 
    nome = models.CharField(max_length=255, null=False, blank=False)
    telefone = models.CharField(max_length=20, null=True)
    matricula = models.CharField(max_length=255, null=False, blank=False)
    senha = models.CharField(max_length=255, null=False, blank=False, default='Aluno@ifpi')
    tipo = models.CharField(max_length=255, null=False, blank=False, default='aluno')

    def __str__(self):
        return self.nome

class Cosultas(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    numeroConsulta = models.IntegerField(null=False)
    horario = models.IntegerField(null=False)
    data = models.DateField(null=False)
    pendente = models.BooleanField(null=False, default=True)
    estevePresente = models.BooleanField(null=False, default=False)
    descricao = models.TextField(null=True)

    def __str__(self):
        firstName = self.usuario.nome.split()[0]
        return f'{firstName}: {self.data}'

class Sessao(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=15, null=False, blank=False)
    dataCriacao = models.DateField(null=False, blank=False)
    dataExpiracao = models.DateField(null=False, blank=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        firstName = self.usuario.nome.split()[0]
        return f'{firstName}: {self.dataCriacao}'