# Generated by Django 3.0.3 on 2020-11-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0002_auto_20201110_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='file_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]