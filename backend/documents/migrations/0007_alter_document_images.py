# Generated by Django 3.2 on 2023-08-29 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_alter_document_textfields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='images',
            field=models.ManyToManyField(blank=True, max_length=255, to='documents.Image', verbose_name='Элемент'),
        ),
    ]
