# Generated by Django 4.1.5 on 2023-01-26 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('servisas', '0011_alter_automobilis_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='UzsakymoApzvalga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('atsiliepimas', models.TextField(max_length=2000, verbose_name='Atsiliepimas')),
                ('klientas_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Vartotojas')),
                ('uzsakymas_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servisas.uzsakymas')),
            ],
            options={
                'verbose_name': 'Atsiliepimas',
                'verbose_name_plural': 'Atsiliepimai',
                'ordering': ['-date_created'],
            },
        ),
    ]
