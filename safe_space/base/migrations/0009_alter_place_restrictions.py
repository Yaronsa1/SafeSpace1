# Generated by Django 3.2.9 on 2021-12-20 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_place_restrictions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='restrictions',
            field=models.ManyToManyField(to='base.Restrictions'),
        ),
    ]
