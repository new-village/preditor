# Generated by Django 2.0.4 on 2018-04-13 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('race_id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('race_dt', models.DateField(db_index=True, null=True)),
                ('place_id', models.CharField(max_length=2)),
                ('place_name', models.CharField(max_length=8)),
                ('days', models.IntegerField(null=True)),
                ('times', models.IntegerField(null=True)),
                ('round', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=80)),
                ('grade', models.CharField(max_length=2, null=True)),
                ('type', models.CharField(max_length=16)),
                ('length', models.IntegerField(null=True)),
                ('weather', models.CharField(max_length=16)),
                ('condition', models.CharField(max_length=16)),
                ('head_count', models.IntegerField(null=True)),
                ('max_prize', models.FloatField(null=True)),
                ('odds_stdev', models.FloatField(null=True)),
                ('result_flg', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'レース',
                'verbose_name_plural': 'レース',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('key', models.CharField(max_length=34, primary_key=True, serialize=False)),
                ('rank', models.IntegerField(null=True)),
                ('bracket', models.IntegerField(null=True)),
                ('horse_num', models.IntegerField(null=True)),
                ('horse_id', models.CharField(db_index=True, max_length=12)),
                ('sex', models.CharField(max_length=4)),
                ('age', models.IntegerField(null=True)),
                ('burden', models.FloatField(null=True)),
                ('jockey_id', models.CharField(max_length=10)),
                ('finish_time', models.FloatField(null=True)),
                ('last3f_time', models.FloatField(null=True)),
                ('odds', models.FloatField(null=True)),
                ('odor', models.IntegerField(null=True)),
                ('weight', models.IntegerField(null=True)),
                ('weight_diff', models.IntegerField(null=True)),
                ('trainer_id', models.CharField(max_length=10)),
                ('owner_id', models.CharField(max_length=12)),
                ('prize', models.FloatField(null=True)),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='umap.Race')),
            ],
            options={
                'verbose_name': '出走情報',
                'verbose_name_plural': '出走情報',
            },
        ),
        migrations.AlterModelOptions(
            name='race',
            options={},
        ),
        migrations.AddIndex(
            model_name='race',
            index=models.Index(fields=['race_dt'], name='umap_race_race_dt_f5c7cc_idx'),
        ),
        migrations.AddIndex(
            model_name='result',
            index=models.Index(fields=['horse_id'], name='umap_result_horse_i_bb6b70_idx'),
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('label', models.CharField(max_length=80, primary_key=True, serialize=False)),
                ('bin', models.BinaryField()),
                ('type', models.CharField(max_length=80)),
                ('recall', models.FloatField()),
                ('precision', models.FloatField()),
                ('note', models.TextField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '予測モデル',
                'verbose_name_plural': '予測モデル',
            },
        ),
        migrations.AlterModelOptions(
            name='result',
            options={},
        ),
        migrations.AddIndex(
            model_name='result',
            index=models.Index(fields=['jockey_id'], name='umap_result_jockey__b6d539_idx'),
        ),
        migrations.AddField(
            model_name='result',
            name='roi',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='run_cnt',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='t3r_horse',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='t3r_jockey',
            field=models.FloatField(null=True),
        ),
        migrations.AlterModelOptions(
            name='race',
            options={'verbose_name': 'レース', 'verbose_name_plural': 'レース'},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'verbose_name': '出走情報', 'verbose_name_plural': '出走情報'},
        ),
        migrations.AddField(
            model_name='result',
            name='clf_result',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='result',
            name='reg_result',
            field=models.FloatField(null=True),
        ),
    ]
