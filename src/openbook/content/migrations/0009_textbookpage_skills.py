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
