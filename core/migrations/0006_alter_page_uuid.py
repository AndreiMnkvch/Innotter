# Generated by Django 4.1.5 on 2023-02-03 07:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_page_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('575981fc-ab19-498b-94c2-f55019224cba'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
