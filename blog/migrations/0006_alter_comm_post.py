# Generated by Django 3.2.16 on 2022-10-28 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_comm_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comm',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='blog.post'),
        ),
    ]
