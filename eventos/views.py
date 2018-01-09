# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import http.client, urllib.parse

from django.shortcuts import render

import requests

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from eventos.models import *


from django.contrib.auth.decorators import login_required

from django.core import serializers
from django.core.mail import EmailMessage

from datetime import date

@login_required
def alllusers(request):
    data = serializers.serialize("json", User.objects.all(), fields=('username', 'first_name', 'last_name', 'pk'))

    return HttpResponse(data)


def criarusuario(request):
    if request.method == "POST":
        response = {}
        nomecompleto = request.POST['nomecompleto']
        username = request.POST['username']
        email = request.POST['email']
        senha = request.POST['senha']
        cfsenha = request.POST['cfsenha']
        captcha = request.POST['g-recaptcha-response']

        try:

            # Verifica se o captcha esta OK
            url = "https://www.google.com/recaptcha/api/siteverify"
            params = {'secret': '6LeUhSMTAAAAAAIPG3Zyi0Usf9yfIbjhQP9fbgGC', 'response': captcha }
            verify_rs = requests.get(url, params=params)

            print("Url: ", verify_rs.url)
            verify_rs = verify_rs.json()

            response["status"] = verify_rs.get("success", False)

            print("Captcha: ", captcha, "\n")
            print("Resposta: ", response["status"])
            resp = response["status"]
        except:
            print("erro Captcha")
            return HttpResponse(-1)

        try:
            # Verifica se o usuario ja esta cadastrado
            userl = len(User.objects.filter(username=username))

            if senha != cfsenha:
                return HttpResponse(0)
            elif userl != 0:
                return HttpResponse(1)
            elif resp!= True:
                return HttpResponse(2)

            user = User.objects.create_user(username, email, senha)

            # gera o primeiro e o ultimo nome do usuario
            nomel = nomecompleto.split(' ') # todos os nomes devem ter espaço
            lastname = nomel[len(nomel)-1]
            ind = nomel.index(lastname)
            del nomel[ind]
            firstname = " ".join(nomel)

            user.first_name = firstname
            user.last_name = lastname
            user.save()

            # Autentica


            password = senha

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)


            # TODO Enviar um e-mail com o login, e-mail e senha
            # A coisa toda funcionou
            return HttpResponse(3) #blz
        except:
            return HttpResponse(666) # sei la, alguma merda aconteceu


def logUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/')
            else:
                return HttpResponse(1)  # Usuario nao presente
        else:
            return HttpResponse(1) # Usuario nao presente


@login_required
def logoff(request):
    logout(request)

    return HttpResponseRedirect('/')


@login_required
def changePass(request):
    if request.method == "POST":
        user = request.user
        oldpass = request.POST['oldpass']
        newpass = request.POST['newpass']
        newpassr = request.POST['newpassr']

        print("User: ", user)
        print("User: ", oldpass)

        usr = authenticate(username=user, password=oldpass)
        if usr is not None:
            # Verifica se as senhas sao iguais
            if newpass == newpassr:
                usr.set_password(newpass)
                usr.save()
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("-1") # certo
        else:
            return HttpResponse('2') # senha errada
    else:
        return HttpResponse('1')



# Estes arquivos precisam pegar a requisicao CSRFTOKEN
def renderContato(request):
    context = {}
    return render(request, 'contato.htm', context)


def renderInscricao(request):

    user = request.user
    try:
        usrObj = User.objects.get(username=user)
    except:
        # Nao tem ninguem autenticado
        context = {}
        return render(request, 'inscricao.htm', context)


    # tem profile?
    perfiluser = Perfil.objects.filter(user=usrObj)

    tam = len(perfiluser)

    if tam == 0:
        # Deve cadastrar o profile
        context = {}

        pf = Perfil()
        pf.nomecracha = usrObj.get_full_name()
        pf.email = usrObj.email
        pf.cidade = "Barra do Garças"
        pf.estado="MT"
        pf.cep = "78600-000"

        context['mensagem'] = "Preencha os dados do perfil antes de efetuar a inscrição"

        context['pf'] = pf
        context['estados'] = getEstados()

        return render(request, 'profile.html', context)

    else: # aqui e igual a 1
        context = {}

        context['pf'] = perfiluser[0]
        context['estados'] = getEstados()
        print(context['estados'])

        return render(request, 'profile.html', context)

def getEstados():
    estados = {}
    estados["AC"] = "Acre	"
    estados["AL"] = "Alagoas	"
    estados["AP"] = "Amapá"
    estados["AM"] = "Amazonas	"
    estados["BA"] = "Bahia	"
    estados["CE"] = "Ceará	"
    estados["DF"] = "Distrito Federal	"
    estados["ES"] = "Espírito Santo	"
    estados["GO"] = "Goiás	"
    estados["MA"] = "Maranhão	"
    estados["MT"] = "Mato Grosso	"
    estados["MS"] = "Mato Grosso do Sul	"
    estados["MG"] = "Minas Gerais	"
    estados["PA"] = "Pará;	"
    estados["PB"] = "Paraíba	"
    estados["PR"] = "Paraná	"
    estados["PE"] = "Pernambuco	"
    estados["PI"] = "Piauí	"
    estados["RJ"] = "Rio de Janeiro	"
    estados["RN"] = "Rio Grande do Norte	"
    estados["RS"] = "Rio Grande do Sul	"
    estados["RO"] = "Rondônia	"
    estados["RR"] = "Roraima	"
    estados["SC"] = "Santa Catarina	"
    estados["SP"] = "São Paulo	"
    estados["SE"] = "Sergipe	"
    estados["TO"] = "Tocantins	"


    return estados

@login_required
def cadPerfil(request):
    if request.method == "POST":
        try:
            # falta criar os formularios para verificar se os dados recebidos são válidos
            usrObj = User.objects.get(username=request.user)
            nomecracha = request.POST['nomecracha']
            email = request.POST['email']
            datanasci = request.POST['dtnasci'] # esta diferente
            sexo = request.POST['sexo']
            cep = request.POST['cep']
            estado = request.POST['Estado']
            cidade = request.POST['cidade']
            endereco = request.POST['endereco']
            bairro = request.POST['bairro']
            complemento = request.POST['complemento']
            telefone = request.POST['telefone']
            celular = request.POST['celular']
            rg = request.POST['rg']
            cpf = request.POST['cpf']

            # tenta encontrar
            try:
                perf = Perfil.objects.get(user=usrObj)
            except:
                perf = Perfil()
                perf.user = usrObj

            perf.nomecracha = nomecracha
            perf.email = email
            perf.datanasci = datanasci
            perf.sexo = sexo
            perf.cep = cep
            perf.estado = estado
            perf.cidade = cidade
            perf.endereco = endereco
            perf.bairro = bairro
            perf.complemento = complemento
            perf.telefone = telefone
            perf.celular = celular
            perf.rg = rg
            perf.cpf = cpf
            perf.save()
        except:
            print("Cara deu erro louco aqui que eu não sei dizer qual é")
            pass

        # Redireciona para a página de matricula

        return HttpResponseRedirect('/')
@login_required
def questionario(request):

    context = {}
    context['main'] = True
    return render(request, "questinscricaoevento.html", context)


@login_required
def enviarquestionario(request):
    if request.method == "POST":
        quest = Questionario()
        quest.user = request.user
        quest.academico = request.POST['academico']
        quest.curso = request.POST['curso']
        quest.profsaude = request.POST['profsaude']
        quest.profissao = request.POST['academico']
        quest.temposervico = request.POST['temposervico']
        quest.raps = request.POST['raps']
        quest.localtrabalho = request.POST['localtrabalho']
        quest.temprapsmental = request.POST['temprapsmental']
        quest.participaant = request.POST['participaant']
        quest.saudementalf = request.POST['saudementalf']
        quest.importancia = request.POST['importancia']
        quest.justificativa = request.POST['justificativa']

        try:
            quest.save()

            return HttpResponse(1) # sucesso
        except:
            return HttpResponse(-1)

def sendmail(request):

    res = 0

    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        telefone = request.POST['telefone']
        assunto  = request.POST['assunto']
        mensagem = request.POST['mensagem']

        msgt = "<b>Nome: </b> " + nome.upper()
        msgt = msgt + "<br /><b>Email: </b>" + email
        msgt = msgt + "<br /><b>Telefone: </b>" + telefone +" <br /> <br /> <b>Mensagem</b><br />"

        try:
            msg = EmailMessage(assunto, (msgt+mensagem), 'geekaia@gmail.com', [email, 'alisseia@hotmail.com', 'marcosvenf@gmail.com', 'tayla-queren@live.com', 'adaene_moura@hotmail.com'])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            res = 1
        except:
            res = 0

    return HttpResponse(res) # 1 ok e -1 erro


def forminscr(request):


    try:
        user = User.objects.get(pk=request.user.id)
        fichauser = InscriUser.objects.get(user=user)
    except:
        fichauser = InscriUser()

    context = {}
    context['ficha'] = fichauser

    return render(request, "formulariomultiplesteps.html", context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def matriculaaluno(request):

    temcad = 0
    teminscri = ""
    usr = User.objects.get(pk=request.user.id)
    print("Executei a função")
    print("Usuario: "+usr.get_full_name())

    prazo = 0
    if request.method == "POST":
        print("E um post")
        try:
            # Se já estive
            teminscri = InscriUser.objects.filter(user=usr)
            if len(teminscri)==1:
                print("Tem cadastro -- neste caso é só cadastrar")
                temcad=1
            # Verifica a quantidade de usuarios
            alli = InscriUser.objects.all()
            tam = len(alli)

            # Não é permitido o cadastro de mais de 290 estudantes
            if tam >= 300:
                print("Tamanho excedido!!!")
                return HttpResponse("-1 - Atenção, já não há mais vagas no evento!!!")

            # Verificar se as inscrições estão dentro do prazo
            atual = date.today()
            inicio = date(2016,8, 29) # Inicio do prazo da inscrição
            fim = date(2016, 9, 23) # Fim do prazo da inscrição

            # Para esta vez iremos estpular somente o perído fim das inscrições
            #if atual >= inicio and atual <= fim:
            if atual <= fim: # so para testes
                print("Ta tranquilo ta favoravel ")
            else:
                print("Fora do prazo")
                return HttpResponse("-2 - Atenção, inscrição fora do prazo!!!")
        except:
            # Não tem nada para este usuario
            print("Deu erro 2")
            pass

        #a = InscriUser()
        #a.user = usr
        inscri = InscriUser()

        if temcad == 1:
            # Aqui faz o update
            inscri = teminscri[0]
            print("Já tem cadastro, então pegar o dado recuperado")


        inscri.user = usr
        inscri.etnia = request.POST['etnia']
        inscri.estadocivil = request.POST['estadocivil']
        inscri.escolaridade= request.POST['escolaridade']
        inscri.renda = request.POST['renda']
        inscri.profissao = request.POST['profissao']
        inscri.academico = request.POST['academico']
        inscri.instituicaodeensino = request.POST['instituicaodeensino']
        inscri.alunotecnico= request.POST['alunotecnico']
        inscri.profraps = request.POST['profraps']
        inscri.identpublico= request.POST['identpublico']
        inscri.usuarioservico = request.POST['usuarioservico']
        inscri.usuarioservicofamilia = request.POST['usuarioservicofamilia']
        inscri.japarticipou = request.POST['japarticipou']
        inscri.abordcont = request.POST['abordcont']
        inscri.partcurso = request.POST['partcurso']
        inscri.jaauciliou= request.POST['jaauciliou']
        inscri.jaaucilioudrogas= request.POST['jaaucilioudrogas']
        inscri.opiniaodiscussao= request.POST['opiniaodiscussao']
        inscri.opiniaoevento= request.POST['opiniaoevento']

        #tudo Ok



        try:
            inscri.save()
            print("Dados salvos com sucesso!!!!")
            print()
        except:
            print("Erro ao salvar")


    return HttpResponseRedirect("/")

def areaadmin(request):
    return render(request, "adminint.html")


@login_required
def gerarcsv(request):

    user = request.user.get_username()

    if user != "adm":
        return HttpResponse("Usuário sem permissão!!!")

    # Fazer a checagem do admin
    allinscri = InscriUser.objects.all()

    l=[]

    for p in allinscri:
        l.append(p.user.get_full_name().upper())

    sorted(l)

    t = len(l)

    lf = []
    for i in range(0, t):
        t = teste()
        t.id = i
        t.nome = l[i]
        lf.append(t)


    context ={}
    context['inscritos'] = lf



    return render(request, "listainscritos.html", context)





class teste():
    id = 0
    nome = ''

class teste2():
    nome = ''
    email=''



@login_required
def gerarcsvemail(request):

    user = request.user.get_username()

    if user != "adm":
        return HttpResponse("Usuário sem permissão!!!")

    # Fazer a checagem do admin
    allinscri = InscriUser.objects.all()

    l=[]

    for p in allinscri:
        t = teste2()
        t.nome = p.user.get_full_name().upper()
        t.email = p.user.email
        l.append(t)

    #sorted(l)

    context ={}
    context['inscritos'] = l



    return render(request, "listainscritosemail.html", context)






@login_required
def areainscrito(request):

    # Para que seja considerado inscrito deve-se preencher o questionario e o perfil


    # Aqui será colocado o certificado do usuário
    return render(request, "areainscrito.html")

def renderEvento(request):
    context = {}
    #fevt = FormEvento()
    #context['formEvento'] = fevt
    return render(request, 'evento/cadevento.html', context)


def getEventos(request):
    data = serializers.serialize("json", Evento.objects.all())
    return HttpResponse(data)

@login_required
def renderMudarsenha(request):
    context = {}
    return render(request, 'mudarsenha.html', context)

def renderCadUser(request):
    context = {}
    return render(request, 'novousuario.html', context)

def renderIndex(request):

    # testa se o usuario esta autenticado
    # se tiver ele e passado uma variavel para o javascript que ira redirecionar para o cadastro

    user = ""

    # index 0 - não autenticado, index 1 - auth sem perfil, index 2 - auth sem
    # esta cadastrado?
    usr = ""
    index=0
    try:
        user = request.user
        usr = User.objects.get(username=user.username)
        index=1
    except:
        pass # pode ir para o index

    if index ==1:
        try:
            perf = Perfil.objects.get(user=usr)
            index = 2
            # tem perfil e pode ir para o proximo -- que e o questionario
        except:
            pass

        if index == 2:
            try:
                insc = InscriUser.objects.get(user=usr)
                index = 3
                # tem perfil e pode ir para o proximo -- que e o questionario
            except:
                pass

    if index==0:
        print("Lets auth boy")
    elif index==1:
        print("Vamos para o perf")
    elif index==2:
        print("Vamos para o questionario")
    elif index==3:
        print("Passo final - INSCRIÇÃO !!!!!!!!!!")

    context = {}
    context['index'] = index

    return render(request, "index.htm", context)


def pesqnomes(request):

    return render(request, "pesquisanomes.html")

def renderProfile(request):
    user = request.user
    context = {}
    # se não tiver profile data erro
    usrObj = User.objects.get(username=request.user)
    
    try:
        perfil = Perfil.objects.get(user=usrObj)
    except:
        perfil = Perfil()

    context['pf'] = perfil
    context['estados'] = getEstados()

    return render(request, 'profile.html', context)

def renderQuestinscricaoevento(request):
    context = {}

    return render(request, 'questinscricaoevento.htm', context)

