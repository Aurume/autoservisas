# Generated by Django 4.1.5 on 2023-01-25 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servisas', '0008_uzsakymas_due_back_uzsakymas_vartotojas_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uzsakymas',
            name='due_back',
        ),
        migrations.AddField(
            model_name='uzsakymas',
            name='terminas',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Grąžinti iki'),
        ),
        migrations.AlterField(
            model_name='uzsakymas',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
