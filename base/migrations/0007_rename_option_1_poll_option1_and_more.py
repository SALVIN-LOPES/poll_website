# Generated by Django 4.0.6 on 2022-07-07 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_rename_option_four_poll_option_1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='option_1',
            new_name='option1',
        ),
        migrations.RenameField(
            model_name='poll',
            old_name='option_2',
            new_name='option2',
        ),
        migrations.RenameField(
            model_name='poll',
            old_name='option_3',
            new_name='option3',
        ),
        migrations.RenameField(
            model_name='poll',
            old_name='option_4',
            new_name='option4',
        ),
    ]
