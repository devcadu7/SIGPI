"""
URL configuration for sigpi_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.page('login.html')),
    path('login/', views.page('login.html')),
    path('logout/', views.logout),
    path('api/data', views.api_data),
    path('api/auth/login', views.login),
    path('api/submit', views.submit_project),
    path('api/grade-update', views.grade_update),
    path('api/homologar', views.homologate_project),
    path('api/empresa-add', views.company_add),
    path('api/empresa-edit', views.company_edit),
    path('api/empresa-delete', views.company_delete),
    path('api/empresa-feedback', views.company_feedback),
    path('aluno/dashboard/', views.page('aluno/dashboard.html')),
    path('aluno/submissoes/', views.page('aluno/submissoes.html')),
    path('aluno/historico/', views.page('aluno/historico.html')),
    path('aluno/avaliacoes/', views.page('aluno/avaliacoes.html')),
    path('aluno/feedback-alternativa/', views.page('aluno/feedback_alternativa.html')),
    path('aluno/perfil-historico/', views.page('aluno/perfil_historico.html')),
    path('aluno/projeto-detail/', views.page('aluno/projeto_detail.html')),
    path('aluno/projetos/', views.page('aluno/projetos_list.html')),
    path('aluno/upload-entregavel/', views.page('aluno/upload_entregavel.html')),
    path('aluno/vincular-github/', views.page('aluno/vincular_github.html')),
    path('professor/dashboard/', views.page('professor/dashboard.html')),
    path('professor/turmas/', views.page('professor/turmas.html')),
    path('professor/notas/', views.page('professor/notas.html')),
    path('professor/orientandos/', views.page('professor/orientandos.html')),
    path('professor/avaliacoes-historico/', views.page('professor/avaliacoes_historico.html')),
    path('professor/projeto-avaliar/', views.page('professor/projeto_avaliar.html')),
    path('professor/projetos-filtrar/', views.page('professor/projetos_filtrar.html')),
    path('coordenacao/dashboard/', views.page('coordenacao/dashboard.html')),
    path('coordenacao/projetos/', views.page('coordenacao/projetos.html')),
    path('coordenacao/empresas/', views.page('coordenacao/empresas.html')),
    path('coordenacao/auditoria/', views.page('coordenacao/auditoria.html')),
    path('coordenacao/projetos-homologar/', views.page('coordenacao/projetos_homologar.html')),
    path('coordenacao/relatorios/', views.page('coordenacao/relatorios.html')),
    path('coordenacao/usuarios-criar-editar/', views.page('coordenacao/usuarios_criar_editar.html')),
    path('coordenacao/usuarios-gerenciar/', views.page('coordenacao/usuarios_gerenciar.html')),
    path('empresa/dashboard/', views.page('empresa/dashboard.html')),
    path('empresa/demandas/', views.page('empresa/demandas.html')),
    path('empresa/projetos/', views.page('empresa/projetos.html')),
    path('empresa/buscar-talentos/', views.page('empresa/buscar_talentos.html')),
    path('empresa/perfil-aluno/', views.page('empresa/perfil_aluno.html')),
    path('empresa/projeto-detalhe/', views.page('empresa/projeto_detalhe.html')),
    path('empresa/vitrine-projetos/', views.page('empresa/vitrine_projetos.html')),
]
