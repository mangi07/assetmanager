# Generated by Django 2.1.1 on 2019-04-16 23:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assetmanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=20)),
                ('user_type', models.CharField(choices=[('regular', 'Regular User'), ('manager', 'Manager')], max_length=7)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='manageruser',
            name='user',
        ),
        migrations.DeleteModel(
            name='ManagerUser',
        ),
    ]
