# Generated by Django 4.1.5 on 2023-03-18 21:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_alter_post_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="published_date",
            field=models.DateTimeField(null=True),
        ),
    ]
