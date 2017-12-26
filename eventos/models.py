from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.forms.models import ModelForm

class Perfil(models.Model):
    user = models.ForeignKey(User)
    nomecracha = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    datanasci = models.CharField(max_length=10)
    sexo = models.CharField(max_length=50)
    cep = models.CharField(max_length=10,default="" )
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    endereco = models.CharField(max_length=500)
    bairro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, null=True, blank=True, default="")
    telefone = models.CharField(max_length=15, null=True, blank=True, default="")
    celular = models.CharField(max_length=15)
    rg = models.CharField(max_length=50)
    cpf = models.CharField(max_length=50)


    def nomecompleto(self):
        return self.user.get_full_name()

    def completado(self):
        tem = InscriUser.objects.filter(user=self.user)

        if len(tem) == 1:
            return True
        else:
            return False


class Questionario(models.Model):
    user = models.ForeignKey(User)
    academico = models.BooleanField()
    curso = models.CharField(max_length=255)
    profsaude = models.BooleanField()
    profissao = models.CharField(max_length=255)
    temposervico = models.CharField(max_length=20, null=True, blank=True, default="")
    raps = models.BooleanField()
    localtrabalho = models.CharField(max_length=255, null=True, blank=True,  default="")
    temprapsmental = models.CharField(max_length=30, null=True, blank=True,  default="")
    participaant = models.BooleanField()
    saudementalf  = models.BooleanField()
    importancia = models.BooleanField()
    justificativa = models.TextField(null=True, blank=True, default="")


    def nomecompleto(self):
        return self.user.get_full_name()


class InscriUser(models.Model):
    user = models.ForeignKey(User)
    etnia = models.CharField(max_length=255, default="")
    estadocivil = models.CharField(max_length=255, default="")
    escolaridade= models.CharField(max_length=255, default="")
    renda = models.CharField(max_length=255, default="")
    profissao = models.CharField(max_length=255, default="")
    academico = models.CharField(max_length=255, default="")
    instituicaodeensino = models.CharField(max_length=255, default="")
    alunotecnico = models.CharField(max_length=255, default="")
    profraps = models.CharField(max_length=255, default="")
    identpublico = models.CharField(max_length=255, default="")
    usuarioservico = models.CharField(max_length=255, default="")
    usuarioservicofamilia = models.CharField(max_length=255, default="")
    japarticipou = models.CharField(max_length=255, default="")
    abordcont = models.CharField(max_length=255, default="")
    partcurso = models.CharField(max_length=255, default="")
    jaauciliou = models.CharField(max_length=255, default="")
    jaaucilioudrogas = models.CharField(max_length=255, default="")
    opiniaodiscussao = models.CharField(max_length=255, default="")
    opiniaoevento = models.CharField(max_length=255, default="")


    def nomecompleto(self):
        return self.user.get_full_name()


    class Meta:
        ordering = ["user"]


class Evento(models.Model):
    nomeevento = models.CharField(max_length=255)
    abreviacao = models.CharField(max_length=50)
    inicio = models.DateField()
    fim = models.DateField()
    textoInicio = models.TextField(default="")
    taxainscricao = models.CharField(max_length=50)
    qtatividades = models.IntegerField() # quantas atividades o usuario pode


class Atividade(models.Model):
    evento = models.ForeignKey(Evento)
    descricao = models.CharField(max_length=50)
    oradorouprofessor = models.ForeignKey(User) # funcao pesquisar usuarios
    tipo = models.CharField(max_length=255) # palestra, curso, mesaredonda
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    turno = models.CharField(max_length=15)# Matutino, Vespertino e Noturno
    local = models.CharField(max_length=50)# sala, anfiteatro e outros

class InscricaoEv(models.Model):
    evento = models.ForeignKey(Evento)
    usuario = models.ForeignKey(User)

class InscricaoAtiv(models.Model):
    atividade = models.ForeignKey(Atividade)
    evento = models.ForeignKey(Evento)
    usuario = models.ForeignKey(User)
    concluiuativ = models.BooleanField() # sim/nao - sim gera cert e nao















