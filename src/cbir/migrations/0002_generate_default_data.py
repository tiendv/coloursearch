from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cbir', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL('''
        INSERT INTO cbir_method(name) VALUES ('color_histogram');
        INSERT INTO cbir_method(name) VALUES ('fuzzy_color_histogram');
        INSERT INTO cbir_method(name) VALUES ('cumulative_color_histogram');
        INSERT INTO cbir_method(name) VALUES ('color_coherence_vector');
        INSERT INTO cbir_method(name) VALUES ('color_correlogram');
        ''')
    ]

