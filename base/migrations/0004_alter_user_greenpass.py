# Generated by Django 4.0 on 2022-01-04 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_user_greenpass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='greenpass',
            field=models.ImageField(default='green_pass.jpg', null=True, upload_to=''),
        ),
    ]
