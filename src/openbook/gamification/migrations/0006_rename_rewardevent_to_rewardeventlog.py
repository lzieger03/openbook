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

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_gamification', '0005_alter_reward_value'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RewardEvent',
            new_name='RewardEventLog',
        ),
        migrations.AlterModelTable(
            name='rewardeventlog',
            table='openbook_gamification_reward_event_log',
        ),
        migrations.AlterModelOptions(
            name='rewardeventlog',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Reward Event Log',
                'verbose_name_plural': 'Reward Event Log',
            },
        ),
        migrations.AlterField(
            model_name='rewardeventlog',
            name='account',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='reward_event_logs',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Account',
            ),
        ),
    ]
