# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_gamification', '0002_alter_reward_value'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccountPoints',
            new_name='AccountProgress',
        ),
        migrations.AddField(
            model_name='accountprogress',
            name='level',
            field=models.PositiveIntegerField(default=0, verbose_name='Level'),
        ),
        migrations.AlterModelOptions(
            name='accountprogress',
            options={
                'ordering': ['account'],
                'verbose_name': 'Account Progress',
                'verbose_name_plural': 'Account Progress',
            },
        ),
    ]
