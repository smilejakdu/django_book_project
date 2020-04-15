# Generated by Django 3.0.2 on 2020-04-14 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_memo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, verbose_name='start_date')),
                ('end_date', models.DateTimeField(null=True, verbose_name='end_date')),
                ('text', models.CharField(max_length=250, null=True)),
            ],
            options={
                'db_table': 'schedulers',
            },
        ),
    ]
