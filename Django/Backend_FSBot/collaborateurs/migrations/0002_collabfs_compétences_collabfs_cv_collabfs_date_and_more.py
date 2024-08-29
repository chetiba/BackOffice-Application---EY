# Generated by Django 4.2.13 on 2024-07-08 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaborateurs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collabfs',
            name='Compétences',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collabfs',
            name='cv',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collabfs',
            name='date',
            field=models.CharField(default='data analysis', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collabfs',
            name='diplome_obtenu',
            field=models.CharField(db_column='diplome obtenu', default='data analysis', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collabfs',
            name='grade',
            field=models.CharField(default='data analysis', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collabfs',
            name='image',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collabfs',
            name='institution',
            field=models.CharField(default='data analysis', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collabfs',
            name='role',
            field=models.CharField(default='data analysis', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collabfs',
            name='departement',
            field=models.CharField(default='SSL FS TRANSFORMATION', max_length=100),
        ),
        migrations.AlterField(
            model_name='collabfs',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Personal Email'),
        ),
        migrations.AlterField(
            model_name='collabfs',
            name='poste',
            field=models.CharField(choices=[('Junior Consultant', 'Junior Consultant'), ('Senior Consultant', 'Senior Consultant'), ('Assistant Manager', 'Assistant Manager'), ('Manager', 'Manager'), ('Senior Manager', 'Senior Manager'), ('Partner', 'Partner')], max_length=100),
        ),
    ]
