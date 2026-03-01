"""
Import news from Facebook page photos.
Creates News entries with optimized images from /tmp/cmda_fb_news/optimized/
"""
import os
from datetime import date

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.pages.models import News, NewsImage

EVENTS = [
    {
        'title': 'Ceremonia de înmânare a certificatelor de grant – Programul STARTUP pentru TINERI și MIGRANȚI',
        'excerpt': 'CMDA a organizat ceremonia de înmânare a certificatelor de grant în cadrul Programului municipal STARTUP pentru TINERI și MIGRANȚI. Beneficiarii au primit granturi nerambursabile de până la 250.000 MDL pentru lansarea și dezvoltarea afacerilor.',
        'content': '''<p>Centrul Municipal pentru Dezvoltarea Antreprenoriatului (CMDA) a organizat ceremonia oficială de înmânare a certificatelor de grant în cadrul <strong>Programului municipal STARTUP pentru TINERI și MIGRANȚI</strong>, oferit de Primăria Municipiului Chișinău.</p>

<p>În cadrul evenimentului, beneficiarii programului au primit certificate de grant nerambursabil de până la <strong>250.000 MDL</strong> pentru lansarea și dezvoltarea afacerilor în diverse domenii de activitate.</p>

<p>Printre companiile beneficiare se numără:</p>
<ul>
    <li><strong>S.R.L. "FLEX WOOD"</strong> – grant de 250.000 MDL pentru prelucrarea articolelor din lemn</li>
    <li><strong>S.R.L. "M&A GROUP"</strong> – grant de 250.000 MDL</li>
    <li><strong>S.R.L. "AMPERION LABS"</strong> – grant de 249.998 MDL pentru educație și instruiri în domeniul inteligenței artificiale</li>
</ul>

<p>Programul STARTUP pentru TINERI și MIGRANȚI oferă:</p>
<ul>
    <li>Granturi nerambursabile pentru lansarea afacerilor</li>
    <li>Consultanță și asistență antreprenorială</li>
    <li>Cursuri gratuite de instruire</li>
</ul>

<p>Evenimentul a reunit antreprenori, reprezentanți ai Primăriei Municipiului Chișinău și echipa CMDA, subliniind angajamentul municipalității față de dezvoltarea ecosistemului antreprenorial din Chișinău.</p>

<p>Mai multe detalii despre program sunt disponibile pe platforma <a href="https://startup.chisinau.md" target="_blank">startup.chisinau.md</a>.</p>''',
        'published_date': date(2025, 1, 28),
        'source_url': 'https://www.facebook.com/photo/?fbid=766709916490148&set=a.648028491691625',
        'image_file': 'grant_1.jpg',
        'gallery_images': [f'grant_{i}.jpg' for i in range(1, 9)],
    },
    {
        'title': 'Lansarea proiectului EUroBRIDGE_UA_MD – Cooperare transfrontalieră pentru antreprenoriat',
        'excerpt': 'CMDA a găzduit evenimentul de lansare a proiectului european EUroBRIDGE_UA_MD, dedicat cooperării transfrontaliere pentru dezvoltarea antreprenoriatului între Republica Moldova și Ucraina.',
        'content': '''<p>Centrul Municipal pentru Dezvoltarea Antreprenoriatului (CMDA) a organizat <strong>evenimentul de lansare a proiectului EUroBRIDGE_UA_MD</strong> – un proiect european dedicat cooperării transfrontaliere pentru dezvoltarea antreprenoriatului.</p>

<p>Proiectul EUroBRIDGE_UA_MD vizează consolidarea legăturilor antreprenoriale între Republica Moldova și Ucraina, facilitând schimbul de experiență, bune practici și oportunități de business între cele două țări.</p>

<p><strong>Obiectivele proiectului:</strong></p>
<ul>
    <li>Dezvoltarea cooperării transfrontaliere în domeniul antreprenoriatului</li>
    <li>Crearea de punți de legătură între ecosistemele de business din Moldova și Ucraina</li>
    <li>Facilitarea accesului la piețe și oportunități de finanțare europeană</li>
    <li>Transferul de bune practici și know-how antreprenorial</li>
</ul>

<p>Evenimentul a reunit peste 70 de participanți – antreprenori, reprezentanți ai instituțiilor publice, organizații internaționale și parteneri de proiect – care au discutat despre oportunitățile de colaborare și dezvoltare comună.</p>

<p>Proiectul este implementat cu sprijinul <strong>Uniunii Europene</strong> și face parte din portofoliul de proiecte europene ale CMDA, care include și SOCIALCAP, DIGICROSS, CEDDI, GrowthUP Chișinău și altele.</p>''',
        'published_date': date(2025, 11, 8),
        'source_url': 'https://www.facebook.com/media/set/?set=a.705744499253357&type=3',
        'image_file': 'euro_1.jpg',
        'gallery_images': [f'euro_{i}.jpg' for i in range(1, 9)],
    },
    {
        'title': 'Incubatorul Municipal de Afaceri – platformă de creștere pentru antreprenori',
        'excerpt': 'Incubatorul Municipal de Afaceri, creat de Primăria Municipiului Chișinău și gestionat de CMDA, oferă sprijin intensiv pentru dezvoltarea afacerilor din sectoarele creative, culturale și IT.',
        'content': '''<p><strong>Incubatorul Municipal de Afaceri (IMA)</strong>, creat de Primăria Municipiului Chișinău și gestionat de CMDA, este un instrument real de accelerare pentru antreprenori.</p>

<p>Rezidenții incubatorului beneficiază de:</p>
<ul>
    <li>Spații modulare de lucru și utilități incluse</li>
    <li>Consultanță de inovare, consultanță tehnologică și sprijin managerial</li>
    <li>Mentorat și instruiri specializate</li>
    <li>Oportunități de networking și dezvoltare profesională</li>
    <li>Perioadă de incubare de până la 24 de luni</li>
</ul>

<p>Printre rezidenții de succes se numără compania <strong>EnergIQ</strong>, al cărei administrator, Vladislav, a pornit cu o idee clară: sisteme electroenergetice sigure, conforme standardelor europene. Prin Incubatorul Municipal de Afaceri, a avut acces la mentorat, instruiri și networking. Rezultatul? Extinderea echipei și creșterea veniturilor.</p>

<p>Cifra de afaceri a rezidenților incubatorului a crescut de la <strong>247.896 lei la 1.863.878 lei</strong>, demonstrând impactul real al programului de incubare.</p>

<p>Dacă ai un business și vrei să îl crești corect, aplică pe <a href="https://startup.chisinau.md/incubator/" target="_blank">startup.chisinau.md/incubator</a>.</p>''',
        'published_date': date(2025, 2, 22),
        'source_url': 'https://www.facebook.com/people/Centrul-Municipal-pentru-Dezvoltarea-Antreprenoriatului/100094534392601/',
        'image_file': 'grant_event_hall.jpg',
        'gallery_images': ['grant_event_hall.jpg'],
    },
]

IMAGE_DIR = '/tmp/cmda_fb_news/optimized'


class Command(BaseCommand):
    help = 'Import news from Facebook page photos with gallery images'

    def add_arguments(self, parser):
        parser.add_argument('--force-gallery', action='store_true',
                            help='Re-import gallery images for existing articles')

    def handle(self, *args, **options):
        created = 0
        gallery_added = 0
        force_gallery = options.get('force_gallery', False)

        for event in EVENTS:
            slug = slugify(event['title'])[:500]
            existing = News.objects.filter(slug=slug).first()

            if existing and not force_gallery:
                if not existing.images.exists():
                    self._add_gallery(existing, event)
                    gallery_added += 1
                else:
                    self.stdout.write(f'Already exists with gallery: {event["title"][:60]}')
                continue

            if existing and force_gallery:
                existing.images.all().delete()
                self._add_gallery(existing, event)
                gallery_added += 1
                self.stdout.write(self.style.SUCCESS(f'Gallery updated: {event["title"][:60]}'))
                continue

            news = News(
                title=event['title'],
                slug=slug,
                excerpt=event['excerpt'],
                content=event['content'],
                published_date=event['published_date'],
                source_url=event['source_url'],
            )

            img_path = os.path.join(IMAGE_DIR, event['image_file'])
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    news.image.save(event['image_file'], ContentFile(f.read()), save=False)
                self.stdout.write(f'  Cover image: {event["image_file"]}')

            news.save()
            self._add_gallery(news, event)
            created += 1
            self.stdout.write(self.style.SUCCESS(f'Created: {event["title"][:60]}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {created} articles, added gallery to {gallery_added} existing.'))

    def _add_gallery(self, news, event):
        for i, img_name in enumerate(event.get('gallery_images', [])):
            img_path = os.path.join(IMAGE_DIR, img_name)
            if os.path.exists(img_path):
                ni = NewsImage(news=news, order=i)
                with open(img_path, 'rb') as f:
                    ni.image.save(img_name, ContentFile(f.read()), save=False)
                ni.save()
                self.stdout.write(f'  Gallery [{i+1}]: {img_name}')
            else:
                self.stdout.write(self.style.WARNING(f'  Not found: {img_path}'))
