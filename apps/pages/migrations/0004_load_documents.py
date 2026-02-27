from django.db import migrations


def load_documents(apps, schema_editor):
    Document = apps.get_model('pages', 'Document')

    documents = [
        {
            'title': 'Declarația de răspundere managerială a I.P. CMDA pentru anul 2023',
            'category': 'rapoarte',
            'file': 'documents/declaratia-de-raspundere-manageriala-2023.pdf',
            'order': 1,
        },
        {
            'title': 'Declarația de răspundere managerială a I.P. CMDA pentru anul 2024',
            'category': 'rapoarte',
            'file': 'documents/declaratia-de-raspundere-manageriala-2024.pdf',
            'order': 2,
        },
        {
            'title': 'Declarația de control intern managerial a I.P. CMDA pentru anul 2025',
            'category': 'rapoarte',
            'file': 'documents/declaratia-control-intern-managerial-2025.pdf',
            'order': 3,
        },
        {
            'title': 'Planul anual de achiziții publice a I.P. CMDA pentru anul 2025',
            'category': 'achizitii_planuri',
            'file': 'documents/planul-de-achizitii-publice-cmda-2025.pdf',
            'order': 1,
        },
        {
            'title': 'Planul anual de achiziții publice provizoriu a I.P. CMDA pentru anul 2026',
            'category': 'achizitii_planuri',
            'file': 'documents/planul-de-achizitii-provizoriu-cmda-2026.pdf',
            'order': 2,
        },
    ]

    for doc_data in documents:
        Document.objects.create(**doc_data)


def remove_documents(apps, schema_editor):
    Document = apps.get_model('pages', 'Document')
    Document.objects.filter(file__startswith='documents/').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_document'),
    ]

    operations = [
        migrations.RunPython(load_documents, remove_documents),
    ]
