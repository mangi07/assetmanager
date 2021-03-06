# Generated by Django 2.1.1 on 2019-04-21 23:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('original_cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assetmanager.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='ExtendedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=20)),
                ('user_type', models.CharField(choices=[('regular', 'Regular User'), ('manager', 'Manager')], max_length=7)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('create_manager', 'Can create a user that is a manager.'), ('create_regular_user', 'Can create a regular user.')),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('in_location', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='assetmanager.Location')),
            ],
        ),
        migrations.AddField(
            model_name='count',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assetmanager.Location'),
        ),
        migrations.AddField(
            model_name='asset',
            name='locations',
            field=models.ManyToManyField(through='assetmanager.Count', to='assetmanager.Location'),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('description', 'in_location')},
        ),
        migrations.AlterUniqueTogether(
            name='count',
            unique_together={('asset', 'location')},
        ),
    ]
