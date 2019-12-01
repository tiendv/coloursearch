from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cbir', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL('''
        INSERT INTO cbir_method(name) VALUES ('fuzzy_color_histogram');
        INSERT INTO cbir_method(name) VALUES ('color_histogram');
        INSERT INTO cbir_method(name) VALUES ('color_coherence_vector');
        INSERT INTO cbir_method(name) VALUES ('color_correlogram');
        
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 1, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 2, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 3, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 4, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 5, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 6, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 7, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 8, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 9, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 10, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 11, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 12, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 13, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 14, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 15, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 16, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 17, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 18, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 19, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 20, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 21, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 22, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 23, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 24, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 25, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 26, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 27, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 28, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 29, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 30, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 31, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 32, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 33, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 34, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 35, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 36, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 37, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 38, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 39, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 40, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 41, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 42, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 43, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 44, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 45, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 46, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 47, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 48, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 49, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 50, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 51, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 52, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 53, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 54, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 55, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 56, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 57, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 58, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 59, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 60, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 61, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 62, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 63, '');
        INSERT INTO cbir_valuetype(method_id, method_index, description) VALUES (1, 64, '');
        ''')
    ]

