# Generated by Django 2.2.3 on 2019-08-02 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_fileupload_gender_select'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='ethnicity_select',
            field=models.BooleanField(default=False),
        ),
    ]
