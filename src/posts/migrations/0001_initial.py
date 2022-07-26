# Generated by Django 4.0.6 on 2022-07-26 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('img_url', models.URLField()),
                ('top', models.CharField(max_length=200)),
                ('pants', models.CharField(max_length=200)),
                ('shoes', models.CharField(max_length=200)),
                ('tips', models.CharField(max_length=300)),
                ('writer', models.ForeignKey(db_column='writer_id', on_delete=django.db.models.deletion.CASCADE, related_name='writer', to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Whether',
            fields=[
                ('post', models.OneToOneField(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='post', serialize=False, to='posts.post')),
                ('temperature_max', models.FloatField(blank=True, null=True)),
                ('temperature_min', models.FloatField(blank=True, null=True)),
                ('temperature_avg', models.FloatField(blank=True, null=True)),
                ('precipitation_avg', models.FloatField(blank=True, null=True)),
                ('wind_speed_avg', models.FloatField(blank=True, null=True)),
                ('humidity_avg', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
