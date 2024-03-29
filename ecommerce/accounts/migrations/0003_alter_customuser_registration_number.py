# Generated by Django 5.0.1 on 2024-01-28 16:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customuser_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='registration_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
