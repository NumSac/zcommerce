# Generated by Django 5.0.1 on 2024-01-30 19:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Synchronization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(blank=True, null=True)),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='synchronizations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name', 'created_at'),
            },
        ),
    ]