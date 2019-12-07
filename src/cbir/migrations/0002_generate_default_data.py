from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cbir', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL('''
        INSERT INTO cbir_method(name, detail) VALUES ('color_histogram', 'Color Histogram');
        INSERT INTO cbir_method(name, detail) VALUES ('fuzzy_color_histogram', 'Fuzzy Color Histogram');
        INSERT INTO cbir_method(name, detail) VALUES ('cumulative_color_histogram', 'Cumulative Color Histogram');
        INSERT INTO cbir_method(name, detail) VALUES ('color_coherence_vector', 'Color Coherence Vector');
        INSERT INTO cbir_method(name, detail) VALUES ('color_correlogram', 'Color Correlogram');
        ''')
    ]

