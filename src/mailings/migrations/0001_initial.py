# Generated by Django 4.1.6 on 2023-02-19 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonMailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email подписчика')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.case', verbose_name='Дело')),
            ],
            options={
                'db_table': 'case_mailing_list',
            },
        ),
    ]
