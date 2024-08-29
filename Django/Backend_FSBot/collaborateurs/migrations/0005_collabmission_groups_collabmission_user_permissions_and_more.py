# Generated by Django 4.2.13 on 2024-08-14 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('collaborateurs', '0004_collabmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='collabmission',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='collabfs_groups', related_query_name='collabfs_group', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='collabmission',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='collabfs_user_permissions', related_query_name='collabfs_user_permission', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='collabfs',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='collabfs',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]