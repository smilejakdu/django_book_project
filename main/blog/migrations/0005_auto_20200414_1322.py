# Generated by Django 3.0.2 on 2020-04-14 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_scheduler'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduler',
            name='text',
            field=models.CharField(max_length=250),
        ),
    ]