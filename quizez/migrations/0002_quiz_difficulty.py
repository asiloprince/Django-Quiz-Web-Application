# Generated by Django 3.2 on 2021-06-14 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizez', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='difficulty',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Select', max_length=6),
        ),
    ]
