# Generated by Django 3.0.2 on 2020-04-15 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200414_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduler',
            name='date_id',
            field=models.IntegerField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
