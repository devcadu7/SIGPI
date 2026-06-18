import json
from datetime import date

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import Company, CurrentUser, MentoredGroup, Project, Student, Submission


ROLE_DESTINATIONS = {
    'aluno': '/aluno/dashboard/',
    'professor': '/professor/dashboard/',
    'coordenacao': '/coordenacao/dashboard/',
    'empresa': '/empresa/dashboard/',
}

ROLE_NAMES = {
    'aluno': 'Lucas Silva',
    'professor': 'Prof. Dr. Carlos Silva',
    'coordenacao': 'Coord. Dr. Ricardo Oliveira',
    'empresa': 'Padaria Alfa Ltda',
}


def page(template_name):
    def view(request):
        return render(request, template_name)

    return view


def logout(request):
    CurrentUser.objects.update_or_create(
        id=1,
        defaults={
            'role': 'aluno',
            'name': 'Lucas Silva',
            'email': 'lucas.aluno@sigpi.com',
        },
    )
    return redirect('/')


def api_data(request):
    current_user = get_current_user()
    student = Student.objects.order_by('id').first()

    return JsonResponse(
        {
            'projects': [serialize_project(project) for project in Project.objects.order_by('id')],
            'submissions': [
                serialize_submission(submission)
                for submission in Submission.objects.order_by('-created_at', '-id')
            ],
            'students': [serialize_student(student) for student in Student.objects.order_by('id')],
            'companies': [serialize_company(company) for company in Company.objects.order_by('id')],
            'mentoredGroups': [
                serialize_group(group) for group in MentoredGroup.objects.order_by('id')
            ],
            'currentUser': serialize_current_user(current_user),
            'users': {
                'student': {
                    'name': student.name if student else current_user.name,
                    'email': current_user.email,
                }
            },
        }
    )


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Metodo nao permitido.'}, status=405)

    body = parse_json(request)
    role = body.get('role') or 'aluno'
    email = body.get('email') or ''
    name = ROLE_NAMES.get(role, 'Lucas Silva')

    CurrentUser.objects.update_or_create(
        id=1,
        defaults={
            'role': role,
            'name': name,
            'email': email,
        },
    )

    return JsonResponse({'success': True, 'redirectUrl': ROLE_DESTINATIONS.get(role, '/aluno/dashboard/')})


@csrf_exempt
def submit_project(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Metodo nao permitido.'}, status=405)

    body = parse_json(request)
    project_title = body.get('project') or ''
    title = body.get('title') or ''
    description = body.get('desc') or ''
    file_name = body.get('fileName') or 'projeto_entrega.pdf'
    current_user = get_current_user()

    next_version = (
        Submission.objects.filter(project=project_title).count() + 1
    )
    Submission.objects.create(
        project=project_title,
        title=title,
        description=description,
        linkedin=body.get('linkedin') or '',
        github=body.get('github') or '',
        file_name=file_name,
        version=next_version,
        status='Pendente',
        date=format_pt_date(date.today()),
    )

    project = Project.objects.filter(title=project_title).first()
    feedback = f'Envio de Trabalho de entrega realizado: "{title}". Justificativa de submissão: "{description}".'
    if project:
        project.is_homologated = False
        project.feedback = feedback
        project.save(update_fields=['is_homologated', 'feedback'])
    else:
        Project.objects.create(
            title=project_title,
            description=description,
            is_homologated=False,
            feedback='Aguardando avaliação do orientador clínico.',
            leader_name=current_user.name,
            progress=25,
        )

    return JsonResponse({'success': True})


@csrf_exempt
def grade_update(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Metodo nao permitido.'}, status=405)

    body = parse_json(request)
    student = Student.objects.filter(ra=body.get('ra')).first()
    if not student:
        return JsonResponse({'success': False, 'message': 'Student selection failed'}, status=404)

    student.m1 = parse_grade(body.get('m1'))
    student.m2 = parse_grade(body.get('m2'))
    student.m3 = parse_grade(body.get('m3'))
    student.save(update_fields=['m1', 'm2', 'm3'])

    project = Project.objects.filter(title=student.active_project).first()
    if project:
        project.grade = f'{weighted_average(student):.1f}'
        project.save(update_fields=['grade'])

    return JsonResponse({'success': True})


@csrf_exempt
def homologate_project(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Metodo nao permitido.'}, status=405)

    body = parse_json(request)
    project = Project.objects.filter(title=body.get('title')).first()
    if not project:
        return JsonResponse({'success': False, 'message': 'Project not found'}, status=404)

    project.is_homologated = bool(body.get('status'))
    project.save(update_fields=['is_homologated'])
    return JsonResponse({'success': True})


@csrf_exempt
def company_add(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Metodo nao permitido.'}, status=405)

    body = parse_json(request)
    cnpj = body.get('cnpj') or ''
    if Company.objects.filter(cnpj=cnpj).exists():
        return JsonResponse({'success': False, 'message': 'Empresa ja cadastrada.'}, status=409)

    Company.objects.create(
        name=body.get('name') or '',
        cnpj=cnpj,
        contact_email=body.get('contactEmail') or '',
        proposal_demand=body.get('proposalDemand') or '',
        is_convenio_active=True,
    )
    return JsonResponse({'success': True})


@csrf_exempt
def company_edit(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Metodo nao permitido.'}, status=405)

    body = parse_json(request)
    company = Company.objects.filter(cnpj=body.get('originalCnpj')).first()
    if not company:
        return JsonResponse({'success': False, 'message': 'Empresa não encontrada.'}, status=404)

    company.name = body.get('name') or ''
    company.cnpj = body.get('cnpj') or ''
    company.contact_email = body.get('contactEmail') or ''
    company.proposal_demand = body.get('proposalDemand') or ''
    company.save()
    return JsonResponse({'success': True})


@csrf_exempt
def company_delete(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Metodo nao permitido.'}, status=405)

    body = parse_json(request)
    deleted, _ = Company.objects.filter(cnpj=body.get('cnpj')).delete()
    if not deleted:
        return JsonResponse({'success': False, 'message': 'Empresa não encontrada.'}, status=404)

    return JsonResponse({'success': True})


@csrf_exempt
def company_feedback(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Metodo nao permitido.'}, status=405)

    body = parse_json(request)
    project = Project.objects.filter(title=body.get('title')).first()
    if not project:
        return JsonResponse({'success': False}, status=404)

    project.grade = body.get('grade') or ''
    project.feedback = body.get('feedback') or ''
    project.evaluation_date = format_pt_date(date.today())
    project.save(update_fields=['grade', 'feedback', 'evaluation_date'])
    return JsonResponse({'success': True})


def parse_json(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return {}


def get_current_user():
    user, _ = CurrentUser.objects.get_or_create(
        id=1,
        defaults={
            'role': 'aluno',
            'name': 'Lucas Silva',
            'email': 'lucas.aluno@sigpi.com',
        },
    )
    return user


def serialize_project(project):
    status = 'APROVADO' if project.is_homologated else 'EM_ANALISE'
    return {
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'desc': project.description,
        'isHomologated': project.is_homologated,
        'status': status,
        'grade': project.grade,
        'feedback': project.feedback,
        'evaluationDate': project.evaluation_date,
        'leaderName': project.leader_name,
        'companyDemandAssigned': project.company_demand_assigned,
        'deadline': project.deadline,
        'progress': project.progress,
    }


def serialize_submission(submission):
    return {
        'id': submission.id,
        'project': submission.project,
        'date': submission.date,
        'version': submission.version,
        'status': submission.status,
        'description': submission.description,
        'title': submission.title,
        'linkedin': submission.linkedin,
        'github': submission.github,
        'fileName': submission.file_name,
    }


def serialize_student(student):
    return {
        'ra': student.ra,
        'name': student.name,
        'activeProject': student.active_project,
        'grades': {
            'm1': float(student.m1),
            'm2': float(student.m2),
            'm3': float(student.m3),
        },
    }


def serialize_company(company):
    return {
        'name': company.name,
        'cnpj': company.cnpj,
        'contactEmail': company.contact_email,
        'proposalDemand': company.proposal_demand,
        'isConvenioActive': company.is_convenio_active,
    }


def serialize_group(group):
    return {
        'code': group.code,
        'groupName': group.group_name,
        'projectName': group.project_name,
        'leader': group.leader,
        'membersCount': group.members_count,
        'status': group.status,
        'nextMeeting': group.next_meeting,
    }


def serialize_current_user(user):
    return {
        'role': user.role,
        'name': user.name,
        'email': user.email,
    }


def parse_grade(value):
    try:
        return round(float(value), 1)
    except (TypeError, ValueError):
        return 0


def weighted_average(student):
    return (float(student.m1) * 0.3) + (float(student.m2) * 0.3) + (float(student.m3) * 0.4)


def format_pt_date(value):
    months = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro',
    ]
    return f'{value.day:02d} de {months[value.month - 1]}, {value.year}'
