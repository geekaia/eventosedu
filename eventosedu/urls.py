"""eventosedu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from eventos.views import *
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    url(r'^$',renderIndex),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^criarusuario', criarusuario),
    url(r'^loguser', logUser),
    url(r'^logoff', logoff),
    url(r'^changePass', changePass),
    url(r'^cadPerfil', cadPerfil),
    url(r'^questinscricaoevento.html', forminscr),
    url(r'^questionario.html', questionario),
    url(r'^enviarquestionario', enviarquestionario),
    #scial auth
    url(r'^renderEvento', renderEvento),
    url(r'^alllusers', alllusers),
    url(r'^getEventos', getEventos),

    url(r'^sendmail', sendmail),

    url(r'^pesqnomes', pesqnomes),
    url(r'^matricular', matriculaaluno),
    url(r'^areainscrito.html', areainscrito),
    url(r'^gerarcsv', gerarcsv),
    url(r'^relatorioemail', gerarcsvemail),


    url(r'^areaadmin.html', areaadmin),




    #url(r'^rendermatricula', rendermatricula),


    url(r'^accounts/', include('allauth.urls')),
    url(r'i18n/', include('django.conf.urls.i18n')),

    # Forms AngularJS
    url(r'^contato.htm', renderContato),
    url(r'^inscricao.htm', renderInscricao),
    url(r'^mudarsenha.html', renderMudarsenha),
    url(r'^novousuario.html', renderCadUser),
    url(r'^profile.html', renderProfile),
    url(r'^questinscricaoevento.html', renderQuestinscricaoevento),
    url(r'^index.htm', renderIndex),

]


