# Generated by Django 5.0.3 on 2024-06-03 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0034_alter_allocationfamily_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='NutritionalLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='fyp/nutritional_label/')),
            ],
        ),
    ]
