# Generated by Django 3.2.16 on 2022-11-09 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comm_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comm',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]