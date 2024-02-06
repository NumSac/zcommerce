# Generated by Django 5.0.1 on 2024-01-30 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_registration_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, help_text='The legal name of the company.', max_length=255, null=True)),
                ('vat_number', models.CharField(blank=True, help_text='The VAT number of the company.', max_length=50, null=True)),
                ('address', models.TextField(blank=True, help_text='The registered address of the company.', null=True)),
                ('contact_person_name', models.CharField(blank=True, help_text='The name of the primary contact person for the company.', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_description', models.CharField(blank=True, help_text="The description for the seller's page", max_length=255, null=True)),
                ('company_background_image', models.ImageField(blank=True, help_text="The background image for the store seller's page", null=True, upload_to='products/%Y/%m/%d')),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='contact_person_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='vat_number',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='accounts.company'),
        ),
        migrations.AddField(
            model_name='company',
            name='company_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='accounts.companyprofile'),
        ),
    ]
