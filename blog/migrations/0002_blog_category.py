# Generated by Django 3.2.5 on 2021-09-06 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
