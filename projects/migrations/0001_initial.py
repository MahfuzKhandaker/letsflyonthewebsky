# Generated by Django 3.1 on 2021-02-05 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('technology', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
            ],
            options={
                'verbose_name_plural': 'Projects',
            },
        ),
    ]
