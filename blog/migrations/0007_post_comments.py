# Generated by Django 2.2.16 on 2020-12-04 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201203_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.CharField(default=0, max_length=700),
            preserve_default=False,
        ),
    ]
