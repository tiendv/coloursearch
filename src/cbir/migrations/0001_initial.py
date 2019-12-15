# Generated by Django 2.2.6 on 2019-12-14 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Extraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directory_path', models.CharField(max_length=1000)),
                ('start_time', models.CharField(max_length=255, null=True)),
                ('end_time', models.CharField(max_length=255, null=True)),
                ('param1_name', models.CharField(max_length=255, null=True)),
                ('param1_value', models.FloatField(null=True)),
                ('param2_name', models.CharField(max_length=255, null=True)),
                ('param2_value', models.FloatField(null=True)),
                ('param3_name', models.CharField(max_length=255, null=True)),
                ('param3_value', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FuzzyColorHistogram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_extraction_id', models.IntegerField()),
                ('color_id', models.IntegerField()),
                ('value', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FuzzyColorHistogramColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_fine_colors', models.IntegerField()),
                ('number_of_coarse_colors', models.IntegerField()),
                ('ccomponent1', models.FloatField()),
                ('ccomponent2', models.FloatField()),
                ('ccomponent3', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('detail', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageExtraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=1000)),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbir.Extraction')),
            ],
        ),
        migrations.AddField(
            model_name='extraction',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbir.Method'),
        ),
        migrations.CreateModel(
            name='CumulativeColorHistogram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ccomponent1_min', models.IntegerField()),
                ('ccomponent1_max', models.IntegerField()),
                ('ccomponent2_min', models.IntegerField()),
                ('ccomponent2_max', models.IntegerField()),
                ('ccomponent3_min', models.IntegerField()),
                ('ccomponent3_max', models.IntegerField()),
                ('value', models.FloatField(default=0)),
                ('image_extraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbir.ImageExtraction')),
            ],
        ),
        migrations.CreateModel(
            name='ColorHistogram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ccomponent1_min', models.IntegerField()),
                ('ccomponent1_max', models.IntegerField()),
                ('ccomponent2_min', models.IntegerField()),
                ('ccomponent2_max', models.IntegerField()),
                ('ccomponent3_min', models.IntegerField()),
                ('ccomponent3_max', models.IntegerField()),
                ('value', models.FloatField(default=0)),
                ('image_extraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbir.ImageExtraction')),
            ],
        ),
        migrations.CreateModel(
            name='ColorCorrelogram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k', models.IntegerField()),
                ('ccomponent1_min', models.IntegerField()),
                ('ccomponent1_max', models.IntegerField()),
                ('ccomponent2_min', models.IntegerField()),
                ('ccomponent2_max', models.IntegerField()),
                ('ccomponent3_min', models.IntegerField()),
                ('ccomponent3_max', models.IntegerField()),
                ('value', models.FloatField(default=0)),
                ('image_extraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbir.ImageExtraction')),
            ],
        ),
        migrations.CreateModel(
            name='ColorCoherenceVector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ccomponent1', models.IntegerField()),
                ('ccomponent2', models.IntegerField()),
                ('ccomponent3', models.IntegerField()),
                ('alpha', models.IntegerField(default=0)),
                ('beta', models.IntegerField(default=0)),
                ('image_extraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbir.ImageExtraction')),
            ],
        ),
    ]
