# Generated by Django 2.2.3 on 2019-08-02 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_fileupload_ethnicity_select'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='academic_score_select',
            field=models.BooleanField(default=False),
        ),
    ]
