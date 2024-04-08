# Generated by Django 5.0.3 on 2024-04-08 10:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("media", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mediafile",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="mediafile",
            name="file_size",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="mediafile",
            name="file_type",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
