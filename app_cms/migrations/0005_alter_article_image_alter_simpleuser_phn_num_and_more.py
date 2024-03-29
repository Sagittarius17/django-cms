# Generated by Django 4.1.1 on 2023-09-26 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cms', '0004_simpleuser_phn_num_alter_article_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='simpleuser',
            name='phn_num',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simpleuser',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
