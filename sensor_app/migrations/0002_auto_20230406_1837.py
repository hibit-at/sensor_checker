# Generated by Django 2.2 on 2023-04-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='illuminancedata',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]