# Generated by Django 2.0.5 on 2018-11-04 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('umap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('result', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='umap.Result')),
                ('hrs_prz_max', models.FloatField(null=True)),
                ('hrs_prz_avg', models.FloatField(null=True)),
                ('jky_prz_max', models.FloatField(null=True)),
                ('jky_prz_avg', models.FloatField(null=True)),
            ],
            options={
                'verbose_name': '加工変数',
                'verbose_name_plural': '加工変数',
            },
        ),
    ]
