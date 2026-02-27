from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Denumire')),
                ('category', models.CharField(choices=[('planuri', 'Planuri și strategii'), ('rapoarte', 'Rapoarte'), ('achizitii_planuri', 'Achiziții — Planuri'), ('achizitii_anunturi', 'Achiziții — Anunțuri'), ('achizitii_rapoarte', 'Achiziții — Rapoarte')], max_length=30, verbose_name='Categorie')),
                ('file', models.FileField(upload_to='documents/', verbose_name='Fișier')),
                ('order', models.IntegerField(default=0, verbose_name='Ordine')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data încărcării')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documente',
                'ordering': ['category', 'order', '-created_at'],
            },
        ),
    ]
