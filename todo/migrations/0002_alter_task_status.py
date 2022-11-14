# Generated by Django 4.1.3 on 2022-11-14 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[("Done", "Done"), ("Not done", "Not done")],
                default="Not done",
                max_length=63,
            ),
        ),
    ]
