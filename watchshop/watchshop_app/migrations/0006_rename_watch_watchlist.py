# Generated by Django 5.1.2 on 2024-10-22 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchshop_app', '0005_rename_watchs_watch'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Watch',
            new_name='Watchlist',
        ),
    ]