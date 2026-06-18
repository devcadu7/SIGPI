from .models import Company, CurrentUser, MentoredGroup, Project, Student, Submission


PROJECTS = [
    {
        'title': 'Sistema ERP Escolar',
        'description': 'Controle de vendas, estoque perecível e gestão de caixa para comércios locais de panificação.',
        'is_homologated': True,
        'grade': '9.5',
        'feedback': 'O projeto demonstra excelente maturidade arquitetural e usabilidade intuitiva para pequenos comércios de panificação e panificados.',
        'evaluation_date': '12 de Outubro, 2026',
        'leader_name': 'Lucas Silva',
        'company_demand_assigned': 'Automação de Controle de Validade em Panificados (Padaria Alfa)',
        'deadline': '30 de Junho, 2026',
        'progress': 88,
    },
    {
        'title': 'App de Saúde Mental',
        'description': 'Aplicação multiplataforma para monitoramento de rotinas diárias e meditação guiada.',
        'is_homologated': False,
        'grade': '8.8',
        'feedback': 'A metodologia de micro-hábitos está muito bem consolidada, porém necessita detalhar melhor a LGPD nos termos de uso.',
        'evaluation_date': '01 de Junho, 2026',
        'leader_name': 'Mariana Costa',
        'company_demand_assigned': 'Gestão Emocional nos Postos de saúde',
        'deadline': '15 de Julho, 2026',
        'progress': 72,
    },
    {
        'title': 'Rede Social Acadêmica',
        'description': 'Encontros de mentoria e compartilhamento de materiais de pesquisa acadêmica entre pós-graduandos.',
        'is_homologated': True,
        'grade': '7.6',
        'feedback': 'Escopo excelente, mas os índices de performance de rede nos testes de carga necessitam otimização de queries de persistência.',
        'evaluation_date': '20 de Maio, 2026',
        'leader_name': 'Rodrigo Alencar',
        'company_demand_assigned': None,
        'deadline': '05 de Agosto, 2026',
        'progress': 54,
    },
]

SUBMISSIONS = [
    {
        'project': 'Sistema ERP Escolar',
        'date': '12 de Outubro, 2026',
        'version': 2,
        'status': 'Aprovado',
        'description': 'Ajuste na modelagem de estoque de perecíveis de panificação.',
    },
    {
        'project': 'App de Saúde Mental',
        'date': '01 de Junho, 2026',
        'version': 1,
        'status': 'Pendente',
        'description': 'Envio de diagramas UML de caso de uso e termos de consinto da LGPD.',
    },
]

STUDENTS = [
    {'ra': '20240192', 'name': 'Lucas Silva', 'active_project': 'Sistema ERP Escolar', 'm1': 9.0, 'm2': 9.5, 'm3': 10.0},
    {'ra': '20240311', 'name': 'Mariana Costa', 'active_project': 'App de Saúde Mental', 'm1': 8.5, 'm2': 8.0, 'm3': 9.0},
    {'ra': '20240409', 'name': 'Rodrigo Alencar', 'active_project': 'Rede Social Acadêmica', 'm1': 7.0, 'm2': 7.5, 'm3': 8.0},
]

COMPANIES = [
    {
        'name': 'Padaria Alfa Ltda',
        'cnpj': '12.333.444/0001-90',
        'contact_email': 'tecnologia@padariaalfa.com',
        'proposal_demand': 'Automação de Controle de Validade em Panificados - sistema que evite o desperdício de lotes frescos de pães.',
        'is_convenio_active': True,
    },
    {
        'name': 'Frigorífico Beta S/A',
        'cnpj': '42.111.222/0001-11',
        'contact_email': 'projetos@frigorificobeta.com.br',
        'proposal_demand': 'Monitoramento de temperatura estática de câmaras de congelamento em tempo real por IoT.',
        'is_convenio_active': True,
    },
]

MENTORED_GROUPS = [
    {
        'code': 'PI-01',
        'group_name': 'Alpha Engineers',
        'project_name': 'Sistema ERP Escolar',
        'leader': 'Lucas Silva',
        'members_count': 4,
        'status': 'Em Progresso',
        'next_meeting': '14 Jun 2026 às 14:00',
    },
    {
        'code': 'PI-02',
        'group_name': 'Heal Minds',
        'project_name': 'App de Saúde Mental',
        'leader': 'Mariana Costa',
        'members_count': 3,
        'status': 'Em Progresso',
        'next_meeting': '16 Jun 2026 às 09:00',
    },
]


def seed_initial_data():
    CurrentUser.objects.get_or_create(
        id=1,
        defaults={
            'role': 'aluno',
            'name': 'Lucas Silva',
            'email': 'lucas.aluno@sigpi.com',
        },
    )

    for project in PROJECTS:
        Project.objects.get_or_create(title=project['title'], defaults=project)

    for submission in SUBMISSIONS:
        Submission.objects.get_or_create(
            project=submission['project'],
            version=submission['version'],
            defaults=submission,
        )

    for student in STUDENTS:
        Student.objects.get_or_create(ra=student['ra'], defaults=student)

    for company in COMPANIES:
        Company.objects.get_or_create(cnpj=company['cnpj'], defaults=company)

    for group in MENTORED_GROUPS:
        MentoredGroup.objects.get_or_create(code=group['code'], defaults=group)
