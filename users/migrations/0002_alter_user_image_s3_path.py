# Generated by Django 4.1.4 on 2022-12-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image_s3_path',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
