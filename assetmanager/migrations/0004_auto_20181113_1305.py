# Generated by Django 2.1.1 on 2018-11-13 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assetmanager', '0003_auto_20181106_1132'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='count',
            unique_together={('asset', 'location')},
        ),
    ]
