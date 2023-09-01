# Generated by Django 3.2 on 2023-08-29 19:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20230822_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('font_family', models.CharField(max_length=55, verbose_name='Название шрифта')),
                ('font_style', models.CharField(max_length=55, verbose_name='Начертание шрифта')),
                ('font_weight', models.CharField(max_length=55, verbose_name='Насыщенность шрифта')),
                ('url', models.CharField(max_length=55)),
            ],
            options={
                'verbose_name': 'Шрифт',
                'verbose_name_plural': 'Шрифты',
                'ordering': ('-id',),
                'unique_together': {('font_style', 'font_weight')},
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinate_y', models.IntegerField(verbose_name='Координата Y')),
                ('coordinate_x', models.IntegerField(verbose_name='Координата X')),
                ('url', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Элемент',
                'verbose_name_plural': 'Элементы',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='TemplateColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hex', models.CharField(help_text='Введите цвет фона', max_length=7, verbose_name='Цвет фона')),
                ('slug', models.SlugField(blank=True, help_text='Введите уникальный префикс', max_length=55, unique=True, verbose_name='Уникальный префикс')),
            ],
            options={
                'verbose_name': 'Цвет фона',
                'verbose_name_plural': 'Цвета фона',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='TextField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст поля')),
                ('coordinate_y', models.IntegerField(verbose_name='Координата Y')),
                ('coordinate_x', models.IntegerField(verbose_name='Координата X')),
                ('font_size', models.PositiveSmallIntegerField(default=14, help_text='Введите размер шрифта', validators=[django.core.validators.MinValueValidator(8, message='Введите число начиная от 8')], verbose_name='Размер шрифта')),
                ('font_color', models.CharField(max_length=7, verbose_name='Цвет шрифта')),
                ('text_decoration', models.CharField(max_length=20, verbose_name='Подчёркивание шрифта')),
                ('fonts', models.ManyToManyField(help_text='Введите название шрифта', max_length=50, to='documents.Font', verbose_name='Название шрифта')),
            ],
            options={
                'verbose_name': 'Поле',
                'verbose_name_plural': 'Поля',
                'ordering': ('-id',),
            },
        ),
        migrations.RemoveField(
            model_name='stamp',
            name='document_id',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='preview',
            new_name='thumbnail',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='document',
            name='background_image',
        ),
        migrations.RemoveField(
            model_name='document',
            name='category_id',
        ),
        migrations.AddField(
            model_name='document',
            name='category',
            field=models.ForeignKey(blank=True, max_length=15, null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.category'),
        ),
        migrations.AddField(
            model_name='document',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('diplomas', 'Дипломы'), ('certificates', 'Сертификаты'), ('appreciations', 'Благодарности'), ('awards', 'Грамоты')], db_index=True, help_text='Введите категорию документа', max_length=55, verbose_name='Категория'),
        ),
        migrations.DeleteModel(
            name='Field',
        ),
        migrations.DeleteModel(
            name='Stamp',
        ),
        migrations.AddField(
            model_name='document',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.templatecolor'),
        ),
        migrations.AddField(
            model_name='document',
            name='images',
            field=models.ManyToManyField(blank=True, max_length=255, to='documents.Image', verbose_name='Фон'),
        ),
        migrations.AddField(
            model_name='document',
            name='textFields',
            field=models.ManyToManyField(to='documents.TextField'),
        ),
    ]
