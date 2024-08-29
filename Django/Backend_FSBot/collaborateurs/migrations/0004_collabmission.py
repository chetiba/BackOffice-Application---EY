# Generated by Django 4.2.13 on 2024-08-14 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0002_mission_client_alter_mission_code_projet_and_more'),
        ('collaborateurs', '0003_remove_collabfs_grade_collabfs_missions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollabMission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_sur_mission', models.CharField(choices=[('Junior Consultant', 'Junior Consultant'), ('Senior Consultant', 'Senior Consultant'), ('Assistant Manager', 'Assistant Manager'), ('Manager', 'Manager'), ('Senior Manager', 'Senior Manager'), ('Partner', 'Partner')], max_length=100)),
                ('collab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='missions.mission')),
            ],
        ),
    ]