# Generated by Django 3.0.5 on 2020-04-04 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenames', '0024_auto_20200404_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winning_team',
            field=models.CharField(blank=True, choices=[('red', 'red'), ('blue', 'blue')], max_length=50, null=True),
        ),
    ]
