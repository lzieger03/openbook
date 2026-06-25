# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# OpenBook: Interactive Online Textbooks - Server

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_content', '0008_content_anonymous_view_permissions'),
        ('openbook_gamification', '0010_skillprogress_alter_skill_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='textbookpage',
            name='skills',
            field=models.ManyToManyField(blank=True, help_text='Skills trained by this page. Quiz points earned here advance these skills.', related_name='textbook_pages', to='openbook_gamification.skill', verbose_name='Skills'),
        ),
    ]
