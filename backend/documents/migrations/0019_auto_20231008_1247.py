# Generated by Django 3.2 on 2023-10-08 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0018_alter_font_options_remove_textfield_is_bold_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='templatecolor',
            name='blue',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='templatecolor',
            name='green',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='templatecolor',
            name='red',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='DocumentColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='documents.templatecolor')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document')),
            ],
        ),
    ]
