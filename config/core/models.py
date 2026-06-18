from django.db import models


class CurrentUser(models.Model):
    role = models.CharField(max_length=32, default='aluno')
    name = models.CharField(max_length=160)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name} ({self.role})'


class Project(models.Model):
    title = models.CharField(max_length=220, unique=True)
    description = models.TextField()
    is_homologated = models.BooleanField(default=False)
    grade = models.CharField(max_length=16, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    evaluation_date = models.CharField(max_length=80, blank=True, null=True)
    leader_name = models.CharField(max_length=160, default='Lucas Silva')
    company_demand_assigned = models.TextField(blank=True, null=True)
    deadline = models.CharField(max_length=80, default='30 de Junho, 2026')
    progress = models.PositiveSmallIntegerField(default=65)

    def __str__(self):
        return self.title


class Submission(models.Model):
    project = models.CharField(max_length=220)
    date = models.CharField(max_length=80)
    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=80, default='Pendente')
    description = models.TextField()
    title = models.CharField(max_length=220, blank=True, default='')
    linkedin = models.URLField(blank=True, default='')
    github = models.URLField(blank=True, default='')
    file_name = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.project} v{self.version}'


class Student(models.Model):
    ra = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=160)
    active_project = models.CharField(max_length=220)
    m1 = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    m2 = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    m3 = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    def __str__(self):
        return f'{self.ra} - {self.name}'


class Company(models.Model):
    name = models.CharField(max_length=220)
    cnpj = models.CharField(max_length=32, unique=True)
    contact_email = models.EmailField()
    proposal_demand = models.TextField()
    is_convenio_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MentoredGroup(models.Model):
    code = models.CharField(max_length=32, unique=True)
    group_name = models.CharField(max_length=160)
    project_name = models.CharField(max_length=220)
    leader = models.CharField(max_length=160)
    members_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=80)
    next_meeting = models.CharField(max_length=120)

    def __str__(self):
        return self.group_name
