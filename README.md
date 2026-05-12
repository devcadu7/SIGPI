# SIGPI - Sistema de Gestão de Projetos Integrados

## Descrição
📋 Sobre
O SIGPI é uma plataforma desenvolvida para substituir o fluxo informal de submissão de Projetos Integradores via e-mail e Microsoft Teams. O sistema centraliza todas as entregas, organiza informações por turma e aluno, e fornece ferramentas para:

✅ Submissão padronizada de entregáveis
✅ Avaliação estruturada com rubricas
✅ Geração de relatórios acadêmicos
✅ Rastreamento completo de alterações (auditoria)
✅ Vitrine de projetos para empresas parceiras
✅ Gestão centralizada de usuários

🎯 Objetivo
Eliminar gargalos administrativos, melhorar a rastreabilidade de projetos e promover maior transparência no acompanhamento acadêmico, alinhado aos preceitos da Melhoria de Processo de Software (MPS).

👥 Perfis de Usuários
A plataforma atende a 4 perfis distintos:
PerfilPrincipais Funções👨‍🎓 AlunoSubmeter entregáveis, acompanhar progresso, vincular repositório GitHub, visualizar feedbacks👨‍🏫 ProfessorAvaliar projetos com rubricas, registrar notas e feedback, filtrar entregas por turma🎛️ Coordenação/ADMGerenciar usuários, homologar projetos, gerar relatórios, administrar cronogramas🏢 Empresa ParceiraVisualizar vitrine de projetos, buscar talentos por competências, manifestar interesse

✨ Recursos Principais
🔐 Autenticação e Controle de Acesso

Login seguro com e-mail e senha
Controle de perfis personalizados
Logout seguro

📊 Dashboard de Progresso (Aluno)

Cronograma de entregas
Status de projetos
Progresso por Unidade Curricular
Histórico completo de notas e feedbacks

📁 Gerenciamento de Entregáveis

Upload de arquivos (PDF, DOCX, etc.)
Registro automático de data/hora
Vinculação de repositório GitHub
Controle de versões

📋 Avaliação Estruturada (Professor)

Interface de avaliação por rubricas
Filtros avançados por turma/semestre/aluno
Registro automático de auditorias
Histórico de alterações de notas

📈 Relatórios Gerenciais (Coordenação)

Status de entrega por turma
Estatísticas de desempenho acadêmico
Exportação de dados
Visualização de conformidade MPS

🏪 Vitrine de Projetos (Empresa)

Catálogo de projetos homologados
Filtros por tecnologia e competências
Perfil de alunos (com consentimento LGPD)
Canal de recrutamento


🛠️ Stack Tecnológico
Este projeto foi desenvolvido sem uso de frameworks, utilizando apenas as linguagens em sua forma pura:
TecnologiaVersãoFunçãoHTML5-Estrutura das páginasCSS3-Estilização e responsividadeJavaScript (Vanilla)ES6+Interações e validações no frontendPython3.9+Servidor backend e lógica de negócioJSON-Persistência de dados
Por que sem frameworks?
Este é um projeto acadêmico do 2º período do curso de ADS. A intenção é aprender os fundamentos puros das linguagens, sem abstrações de frameworks, para melhor compreensão dos conceitos básicos.

## Como Executar
1. Navegue até a pasta `backend`.
2. Execute `python server.py`.
3. Acesse `http://localhost:8000/frontend/login.html` em seu navegador.
