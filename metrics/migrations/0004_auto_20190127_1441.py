# Generated by Django 2.1.5 on 2019-01-27 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0003_auto_20190127_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blockchain',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='blockchain',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='name'),
        ),
    ]
