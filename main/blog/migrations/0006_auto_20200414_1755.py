# Generated by Django 3.0.2 on 2020-04-14 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200414_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduler',
            name='end_date',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='start_date',
            field=models.CharField(max_length=250),
        ),
    ]