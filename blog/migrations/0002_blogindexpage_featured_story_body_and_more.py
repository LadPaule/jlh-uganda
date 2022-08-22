# Generated by Django 4.0.6 on 2022-08-16 07:02

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogindexpage',
            name='featured_story_body',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogindexpage',
            name='featured_story_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='blogindexpage',
            name='featured_story_title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
