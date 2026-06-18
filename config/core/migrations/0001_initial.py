from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220)),
                ('cnpj', models.CharField(max_length=32, unique=True)),
                ('contact_email', models.EmailField(max_length=254)),
                ('proposal_demand', models.TextField()),
                ('is_convenio_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='aluno', max_length=32)),
                ('name', models.CharField(max_length=160)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='MentoredGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, unique=True)),
                ('group_name', models.CharField(max_length=160)),
                ('project_name', models.CharField(max_length=220)),
                ('leader', models.CharField(max_length=160)),
                ('members_count', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(max_length=80)),
                ('next_meeting', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=220, unique=True)),
                ('description', models.TextField()),
                ('is_homologated', models.BooleanField(default=False)),
                ('grade', models.CharField(blank=True, max_length=16, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('evaluation_date', models.CharField(blank=True, max_length=80, null=True)),
                ('leader_name', models.CharField(default='Lucas Silva', max_length=160)),
                ('company_demand_assigned', models.TextField(blank=True, null=True)),
                ('deadline', models.CharField(default='30 de Junho, 2026', max_length=80)),
                ('progress', models.PositiveSmallIntegerField(default=65)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ra', models.CharField(max_length=32, unique=True)),
                ('name', models.CharField(max_length=160)),
                ('active_project', models.CharField(max_length=220)),
                ('m1', models.DecimalField(decimal_places=1, default=0, max_digits=4)),
                ('m2', models.DecimalField(decimal_places=1, default=0, max_digits=4)),
                ('m3', models.DecimalField(decimal_places=1, default=0, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=220)),
                ('date', models.CharField(max_length=80)),
                ('version', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(default='Pendente', max_length=80)),
                ('description', models.TextField()),
                ('title', models.CharField(blank=True, default='', max_length=220)),
                ('linkedin', models.URLField(blank=True, default='')),
                ('github', models.URLField(blank=True, default='')),
                ('file_name', models.CharField(blank=True, default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
