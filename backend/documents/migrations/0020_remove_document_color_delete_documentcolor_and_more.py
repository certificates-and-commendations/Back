# Generated by Django 4.2.4 on 2023-10-10 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0019_documentcolor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='color',
        ),
        migrations.DeleteModel(
            name='DocumentColor',
        ),
        migrations.AddField(
            model_name='document',
            name='color',
            field=models.ManyToManyField(related_name='colors', to='documents.templatecolor'),
        ),
    ]