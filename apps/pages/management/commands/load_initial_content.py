"""
Management command to load all hardcoded content into the database.

Usage:
    python manage.py load_initial_content

This command is idempotent - it uses get_or_create so it can be run
multiple times without creating duplicates. Images are copied from
static/img/ to the media/ directory.
"""

import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.pages.models import (
    EUProject,
    GalleryPhoto,
    Partner,
    Statistic,
    SuccessStory,
)


class Command(BaseCommand):
    help = 'Load initial hardcoded content into the database'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_img = os.path.join(settings.BASE_DIR, 'static', 'img')
        self.media_root = settings.MEDIA_ROOT

    def handle(self, *args, **options):
        self.stdout.write('Loading initial content...\n')
        self.load_success_stories()
        self.load_partners()
        self.load_eu_projects()
        self.load_gallery_photos()
        self.load_statistics()
        self.stdout.write(self.style.SUCCESS('All initial content loaded successfully.'))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _copy_image(self, src_relative, dest_subfolder, dest_filename=None):
        """
        Copy an image from static/img/<src_relative> to media/<dest_subfolder>/<dest_filename>.
        Returns the relative path suitable for an ImageField value (e.g. 'stories/story1.webp').
        If the source file does not exist, prints a warning and returns the path anyway.
        """
        if dest_filename is None:
            dest_filename = os.path.basename(src_relative)

        src_path = os.path.join(self.static_img, src_relative)
        dest_dir = os.path.join(self.media_root, dest_subfolder)
        dest_path = os.path.join(dest_dir, dest_filename)
        relative_path = os.path.join(dest_subfolder, dest_filename)

        if not os.path.exists(src_path):
            self.stdout.write(self.style.WARNING(
                f'  Source image not found: {src_path}'
            ))
            return relative_path

        os.makedirs(dest_dir, exist_ok=True)

        if not os.path.exists(dest_path):
            shutil.copy2(src_path, dest_path)
            self.stdout.write(f'  Copied {src_relative} -> media/{relative_path}')
        else:
            self.stdout.write(f'  Image already exists: media/{relative_path}')

        return relative_path

    # ------------------------------------------------------------------
    # Success Stories
    # ------------------------------------------------------------------

    def load_success_stories(self):
        self.stdout.write('\n--- Success Stories ---')

        # Stories that appear on the homepage (index.html success-preview)
        homepage_companies = {'Analytics SOL SRL', "Corina's Desserts", 'FIN-TAXY', 'NAKA BOO'}

        stories_data = [
            {
                'company_name': 'Analytics SOL SRL',
                'title': 'O companie ce dezvolta solutii software pentru automatizarea procesului de colectare si analiza a datelor',
                'category': 'IT & AI',
                'short_description': (
                    'Solutii software pentru automatizarea colectarii si analizei datelor cu inteligenta '
                    'artificiala. Contracte internationale in primul an.'
                ),
                'content': (
                    '<p>Cu o licenta si un masterat obtinute in Danemarca, in domeniul Informaticii si Ingineriei, '
                    'Cristian a decis sa-si puna cunostintele si experienta in beneficiul Republicii Moldova. '
                    'A fondat Analytics SOL SRL, o companie ce dezvolta solutii software pentru automatizarea '
                    'procesului de colectare si analiza a datelor, folosind inteligenta artificiala (IA). '
                    'Cristian este rezident in cadrul IMA si beneficiar al Programului Municipal pilot '
                    '\"STARTUP pentru Tineri si Migranti\", unde a obtinut finantare pentru a dota afacerea cu '
                    'echipamente si resurse esentiale pentru lansare.</p>'
                    '<p><strong>Astazi, Analytics SOL SRL ofera servicii inovatoare pentru companii mici si mijlocii:</strong></p>'
                    '<ul>'
                    '<li>Suport clienti - gestionarea eficienta a interactiunilor cu clientii</li>'
                    '<li>Chatbot-uri inteligente - raspuns rapid si automat la intrebari frecvente</li>'
                    '<li>Rute inteligente de apeluri - directionarea automata catre agenti calificati</li>'
                    '<li>Rapoarte de analiza - evidentierea oportunitatilor si provocarilor pentru optimizare</li>'
                    '</ul>'
                    '<p>In primul an de la lansare, Cristian a incheiat contracte internationale si a format o '
                    'echipa de patru profesionisti. Planul sau pentru viitor: extinderea companiei si atragerea '
                    'tot mai multor clienti din Republica Moldova, contribuind la digitalizarea si dezvoltarea '
                    'mediului de afaceri local. Istoria lui Cristian confirma importanta investitiilor strategice '
                    'in dezvoltarea mediului antreprenorial si a revenirii tinerilor Acasa.</p>'
                ),
                'image_src': 'success-stories/story1.webp',
                'order': 1,
            },
            {
                'company_name': 'YOUNG SMART SRL',
                'title': 'O platforma de educatie online creata pentru copiii si parintii care aleg excelenta si flexibilitatea in invatare',
                'category': 'EdTech',
                'short_description': (
                    'Platforma de educatie online care conecteaza profesori dedicati cu elevi din Moldova '
                    'si diaspora, oferind lectii interactive si personalizate.'
                ),
                'content': (
                    '<p>Compania YOUNG SMART SRL, rezidenta in cadrul Incubatorului Municipal de Afaceri, '
                    'dezvolta o platforma de educatie online creata pentru copiii si parintii care aleg excelenta '
                    'si flexibilitatea in invatare! Aceasta scoala moderna conecteaza profesori dedicati din '
                    'intreaga tara cu elevi din Moldova si diaspora, oferind lectii online, interactive si '
                    'personalizate pentru fiecare copil.</p>'
                    '<p><strong>Serviciile oferite includ meditatii individuale la:</strong></p>'
                    '<ul>'
                    '<li>Limbi straine: engleza, germana, franceza, romana, rusa</li>'
                    '<li>Discipline scolare: matematica, limba romana, fizica, chimie, biologie, istorie</li>'
                    '<li>Cursuri de limbi straine si pentru adulti</li>'
                    '</ul>'
                    '<p><strong>Alte servicii oferite:</strong></p>'
                    '<ul>'
                    '<li>Pregatire pentru examene: clasa a 4-a, a 9-a si BAC</li>'
                    '<li>Ateliere online pentru copii si parinti sustinute de psihologi</li>'
                    '<li>Lectii de dictie si comunicare clara</li>'
                    '<li>Profesori cu experienta, cu o abordare prietenoasa si individualizata</li>'
                    '</ul>'
                    '<p>Misiunea platformei este de a oferi educatie de calitate din orice colt al lumii, '
                    'fara drumuri sau stres, ci doar cu rezultate reale. Incubatorul Municipal de Afaceri este '
                    'creat si finantat de Primaria Municipiului Chisinau si administrat de CMDA.</p>'
                ),
                'image_src': 'success-stories/story2.webp',
                'order': 2,
            },
            {
                'company_name': 'AI SKILLS SRL',
                'title': 'Denis Zacon - un exemplu de succes din Incubatorul Municipal de Afaceri Chisinau',
                'category': 'IT & AI',
                'short_description': (
                    'Platforma educationala dedicata inteligentei artificiale cu cursuri video, '
                    'traininguri practice pentru tineri si profesionisti.'
                ),
                'content': (
                    '<p>Cum transformi pasiunea pentru inteligenta artificiala intr-o afacere sustenabila si cu '
                    'impact real? Raspunsul il ofera Denis Zacon, fondatorul companiei AI SKILLS S.R.L., un '
                    'tanar vizionar care dezvolta educatia digitala in domeniul AI, chiar din inima Chisinaului. '
                    'Denis este rezident al Incubatorului Municipal de Afaceri, un proiect al Primariei '
                    'Municipiului Chisinau, care ofera infrastructura, consultanta si mentoratul necesar pentru '
                    'ca tinerii sa isi poata realiza visurile antreprenoriale acasa.</p>'
                    '<p><strong>Datorita sprijinului incubatorului, Denis a reusit:</strong></p>'
                    '<ul>'
                    '<li>Sa creeze o platforma educationala dedicata inteligentei artificiale</li>'
                    '<li>Sa produca cursuri video de inalta calitate, utilizand studioul IMA</li>'
                    '<li>Sa livreze traininguri practice pentru tineri, profesionisti si someri in recalificare</li>'
                    '<li>Sa creasca rapid impactul companiei prin parteneriate active in retea cu alti rezidenti</li>'
                    '</ul>'
                    '<p><strong>AI SKILLS ofera cursuri precum:</strong></p>'
                    '<ul>'
                    '<li>Upskill AI - Pregatit pentru Viitorul Tau Profesional</li>'
                    '<li>AI pentru Profesionisti si Antreprenori</li>'
                    '<li>Ateliere despre integrarea ChatGPT, Claude AI, Gemini AI, dar si automatizari fara programare (no-code tools)</li>'
                    '</ul>'
                    '<p>Rezultatul? Un startup in plina expansiune, cu o contributie semnificativa la digitalizarea '
                    'educatiei si pregatirea fortei de munca pentru era AI. Incubatorul Municipal de Afaceri nu '
                    'este doar un spatiu - este o rampa de lansare.</p>'
                ),
                'image_src': 'success-stories/story3.webp',
                'order': 3,
            },
            {
                'company_name': "Corina's Desserts",
                'title': "Corina's Desserts - un laborator dulce construit cu sprijinul programului Startup pentru Tineri si Migranti",
                'category': 'Cofetarie',
                'short_description': (
                    'De la pasiune la 16 ani - la un atelier de cofetarie modern, elegant si complet echipat, '
                    'cu grant de 200.000 MDL.'
                ),
                'content': (
                    "<p>De la vis la realitate - CORINA'S DESSERTS, un laborator dulce construit cu sprijinul "
                    "Programului STARTUP pentru TINERI si MIGRANTI! La doar 16 ani, Corina Gorincioi a "
                    "descoperit pasiunea pentru prajituri. Astazi, cu sprijinul Primariei Municipiului Chisinau, "
                    "prin intermediul CMDA, gratie unui grant in valoare de 200.000 MDL, Corina este fondatoarea "
                    'brandului "CORINA\'S DESSERTS" S.R.L., un atelier de cofetarie modern, elegant si complet '
                    "echipat in sectorul Botanica.</p>"
                    '<p><strong>Ce a reusit sa realizeze?</strong></p>'
                    '<ul>'
                    '<li>A deschis un spatiu propriu de productie, respectand toate normele tehnico-sanitare</li>'
                    '<li>A achizitionat echipamente profesionale de top: cuptoare UNOX, mixere planetare KitchenAid, '
                    'dulapuri frigorifice industriale, mese si chiuvete din inox, masina de spalat vase</li>'
                    '<li>A creat un punct de preluare a comenzilor intr-un ambient curat, stilat si prietenos cu clientii</li>'
                    '</ul>'
                    '<p>Produsele realizate in atelierul Corinei nu sunt doar gustoase - ele spun povesti. '
                    'De la torturi aniversare cu mesaje creative, pana la deserturi tematice personalizate, '
                    'fiecare creatie impresioneaza prin design si rafinament.</p>'
                    '<p>Cu o echipa formata deja din doua persoane angajate, afacerea functioneaza la turatie '
                    'maxima, atragand zilnic clienti fideli care aleg calitatea si originalitatea.</p>'
                    '<p><strong>Viziunea Corinei?</strong> "Deschiderea unei cofetarii proprii, cu acces direct, '
                    'unde clientii sa poata savura deserturile pe loc."</p>'
                ),
                'image_src': 'success-stories/story4.webp',
                'order': 4,
            },
            {
                'company_name': 'NAKA BOO',
                'title': 'Industria textila din Chisinau prinde culoare cu NAKA BOO',
                'category': 'Textile',
                'short_description': (
                    'Articole vestimentare premium pentru copii si lenjerii de pat, realizate local '
                    'cu grant de 196.700 MDL.'
                ),
                'content': (
                    '<p>Industria textila din Chisinau prinde culoare cu NAKA BOO - un succes antreprenorial '
                    'in cadrul Programului municipal STARTUP pentru TINERI si MIGRANTI! Fondat de antreprenoarea '
                    'Olesea Macari, brandul "NAKA BOO" S.R.L. aduce pe piata locala articole vestimentare '
                    'premium pentru copii si lenjerii de pat, realizate cu grija, estetica rafinata si materiale '
                    'prietenoase cu pielea celor mici. Cu sprijinul financiar al Primariei Municipiului Chisinau, '
                    'prin intermediul CMDA, a fost oferit un grant de 196.700 MDL, visul antreprenorial al '
                    'Olesei a devenit realitate intr-un spatiu de productie modern, amplasat in sectorul Centru.</p>'
                    '<p><strong>Atelierul NAKA BOO a fost dotat cu echipamente de ultima generatie:</strong></p>'
                    '<ul>'
                    '<li>Masini de brodat si tricotat pentru personalizari fine</li>'
                    '<li>Masini de cusut industriale SIRUBA si DISON</li>'
                    '<li>Surfilatoare si masini de crosetat pentru finisaje impecabile</li>'
                    '<li>Scaune ergonomice si layout productiv pentru confortul echipei</li>'
                    '</ul>'
                    '<p><strong>Rezultatele sunt deja vizibile:</strong></p>'
                    '<ul>'
                    '<li>Colectii elegante si colorate de pijamale pentru copii</li>'
                    '<li>Piese vestimentare si lenjerii realizate 100% local</li>'
                    '<li>3 locuri de munca create si un spatiu care inspira profesionalism si creativitate</li>'
                    '</ul>'
                    '<p>NAKA BOO demonstreaza ca "o idee buna, sustinuta de echipament profesionist si implicare '
                    'autentica, poate transforma o nisa de piata intr-un brand de referinta."</p>'
                ),
                'image_src': 'success-stories/story5.webp',
                'order': 5,
            },
            {
                'company_name': 'JOCK MEDIA HUB',
                'title': 'Un hub muzical modern in inima sectorului Ciocana',
                'category': 'Media & Muzica',
                'short_description': (
                    'Studio complet echipat pentru productie audio profesionala, evenimente muzicale '
                    'si inchiriere echipamente pentru artisti independenti.'
                ),
                'content': (
                    '<p>Cand pasiunea pentru muzica devine afacere, un succes marca STARTUP pentru TINERI '
                    'si MIGRANTI! "JOCK MEDIA HUB" S.R.L., fondata de tanarul antreprenor Mircea-Florin Sandu, '
                    'este dovada ca si in Chisinau se pot crea spatii profesionale, competitive international, '
                    'pentru industria creativa. Cu sprijinul Programului municipal "STARTUP pentru TINERI si '
                    'MIGRANTI", implementat de Primaria Municipiului Chisinau prin intermediul Centrului Municipal '
                    'pentru Dezvoltarea Antreprenoriatului (CMDA), s-a nascut un hub muzical modern in inima '
                    'sectorului Ciocana.</p>'
                    '<p><strong>Ce este JOCK MEDIA HUB? Este un studio complet echipat, dedicat:</strong></p>'
                    '<ul>'
                    '<li>Productiei audio profesionale (voce, muzica, mixaj)</li>'
                    '<li>Organizarii de evenimente muzicale cu logistica proprie</li>'
                    '<li>Inchirierii echipamentelor si studioului pentru artisti independenti, DJ-i si creatori de continut</li>'
                    '</ul>'
                    '<p><strong>Cu ajutorul grantului si contributiei proprii, au fost achizitionate:</strong></p>'
                    '<ul>'
                    '<li>Microfoane profesionale Neumann</li>'
                    '<li>Consola DJ Pioneer</li>'
                    '<li>Mixere Allen &amp; Heath</li>'
                    '<li>Sintetizatoare, monitoare de studio, MacBook Pro, controller Roland, camere Sony pentru continut video</li>'
                    '<li>Mobilier acustic, lumini, sistem de tratare fonica</li>'
                    '</ul>'
                    '<p>JOCK MEDIA HUB este mai mult decat un studio - este un loc unde visele suna bine.</p>'
                ),
                'image_src': 'success-stories/story6.webp',
                'order': 6,
            },
            {
                'company_name': 'Cristian Frunze',
                'title': 'Cristian Frunze - exemplul unei generatii de tineri inovatori din Chisinau',
                'category': 'EdTech & AI',
                'short_description': (
                    'De la fondator Smart Curs la Minerva University, San Francisco. '
                    'Ken AI - startup SaaS cu 10 clienti in 11 zile.'
                ),
                'content': (
                    '<p>Cristian Frunze, tanar antreprenor si inovator din Chisinau, demonstreaza ca ambitia, '
                    'educatia si perseverenta pot transforma o idee simpla intr-un impact global. Si-a startat '
                    'afacerea la Incubatorul Municipal de Afaceri, si a ajuns sa studieze la Minerva University '
                    'din San Francisco, una dintre cele mai selective si inovatoare universitati din lume.</p>'
                    '<p>La doar 14 ani, Cristian a fondat Smart Curs, o companie de productie de cursuri online '
                    'care a devenit rapid lider in Romania si Moldova, atingand peste 50.000 de studenti. In 2023, '
                    'a transformat afacerea intr-o organizatie nonprofit, oferind acces gratuit la toate cursurile. '
                    'Rezultatul: inca 25.000 de inscrieri in doar cateva luni.</p>'
                    '<p>Observand potentialul pietei educationale, Cristian a lansat Ken Group, o agentie care '
                    'ajuta expertii sa creeze si sa vanda produse educationale. Cu rezultate remarcabile - clientii '
                    'si-au dublat profiturile in mai putin de trei luni - Ken Group a devenit rapid o agentie cu '
                    'cerere ridicata.</p>'
                    '<p>In 2024 pe cand era rezident al IMA, Cristian a fondat Ken AI, un startup de tip SaaS '
                    'care combina inteligenta artificiala cu interactiunea umana pentru a sprijini afacerile B2B '
                    'in atragerea de clienti de calitate. In doar 11 zile, startup-ul a inregistrat 10 clienti '
                    'activi, devenind un exemplu de inovatie aplicata si scalabila.</p>'
                    '<p>Cristian este, de asemenea, speaker TEDx, invitat frecvent la emisiuni TV si podcasturi, '
                    'si un model inspirational pentru tinerii antreprenori din regiune.</p>'
                    '<blockquote>"Visul meu este sa construiesc afaceri care ajuta oamenii sa creasca prin '
                    'educatie si tehnologie." - Cristian Frunze</blockquote>'
                    '<p>Povestea lui Cristian Frunze nu este doar o reusita individuala, ci o sursa de inspiratie '
                    'pentru o intreaga generatie de tineri moldoveni care viseaza sa creeze, sa inoveze si sa '
                    'contribuie activ la dezvoltarea societatii prin educatie si tehnologie.</p>'
                ),
                'quote': 'Visul meu este sa construiesc afaceri care ajuta oamenii sa creasca prin educatie si tehnologie.',
                'image_src': 'success-stories/story7.webp',
                'order': 7,
            },
            {
                'company_name': 'VOFFLIGHT SRL',
                'title': 'VOFFLIGHT SRL - solutii inovatoare pentru eficienta energetica, dezvoltate in cadrul Incubatorului Municipal de Afaceri',
                'category': 'Energie',
                'short_description': (
                    'Proiectare electrica de inalta precizie, audituri energetice conforme UE '
                    'si solutii fotovoltaice complete.'
                ),
                'content': (
                    '<p>Intr-o lume in care eficienta energetica nu mai reprezinta un trend, ci o necesitate, '
                    'compania VOFFLIGHT SRL, rezidenta in cadrul Incubatorului Municipal de Afaceri, propune o '
                    'noua abordare in domeniul energetic:</p>'
                    '<ul>'
                    '<li>Proiectare electrica de inalta precizie</li>'
                    '<li>Audituri energetice conforme cu normele Uniunii Europene</li>'
                    '<li>Solutii fotovoltaice complete, de la faza de concept pana la implementare</li>'
                    '</ul>'
                    '<p>Fondata de Vladislav Cocimariuc, compania VOFFLIGHT SRL este condusa de o echipa cu '
                    'expertiza practica si orientare catre rezultate concrete. Misiunea companiei consta in '
                    'reducerea cu 30% a pierderilor si riscurilor electrice in urmatorii trei ani. Oferta '
                    'companiei include:</p>'
                    '<ul>'
                    '<li>Solutii eficiente, rapide si fara erori de executie</li>'
                    '<li>Expertiza reala in proiectare si implementare</li>'
                    '<li>Utilizarea tehnologiilor moderne: Revit, PVsyst, Helioscope, solutii de automatizare</li>'
                    '<li>Respectarea normelor tehnice in vigoare: NCM, NAIE, PUE, standarde ale Uniunii Europene</li>'
                    '</ul>'
                    '<p><strong>Principalii beneficiari ai serviciilor VOFFLIGHT:</strong></p>'
                    '<ul>'
                    '<li>Companii si dezvoltatori imobiliari</li>'
                    '<li>Institutii publice: autoritati locale, unitati de invatamant, spitale</li>'
                    '<li>Investitori in proiecte de energie regenerabila, inclusiv parcuri fotovoltaice</li>'
                    '</ul>'
                    '<p>Programul de accelerare este implementat de Primaria Municipiului Chisinau, in cadrul '
                    'Incubatorului Municipal de Afaceri, prin intermediul Centrului Municipal de Dezvoltare a '
                    'Antreprenoriatului (CMDA).</p>'
                ),
                'image_src': 'success-stories/story8.webp',
                'order': 8,
            },
            {
                'company_name': 'FIN-TAXY',
                'title': 'FIN-TAXY - startup din Chisinau, recunoscut in topul global AI de pe platforma F6S',
                'category': 'FinTech',
                'short_description': (
                    'Locul 17 mondial in topul AI pe F6S, din peste 2 milioane de startupuri. '
                    'Automatizare contabila cu AI.'
                ),
                'content': (
                    '<p>Startup-ul FIN-TAXY, parte a comunitatii Incubatorului Municipal de Afaceri, a fost '
                    'clasat pe locul 17 in topul companiilor de inteligenta artificiala (AI) de pe platforma '
                    'internationala F6S, pentru luna iunie 2025. Performanta este remarcabila, avand in vedere ca '
                    'selectia s-a realizat din peste 2 milioane de startupuri la nivel global.</p>'
                    '<p>Fondat de rezidentii incubatorului Denis Bradu si Cristian Preguza, FIN-TAXY dezvolta o '
                    'tehnologie de ultima generatie care isi propune sa automatizeze procesele contabile pentru '
                    '1 milion de companii din intreaga lume.</p>'
                    '<p>Cu o abordare bazata pe combinarea inteligentei artificiale si expertizei contabile, '
                    'FIN-TAXY contribuie la eficientizarea proceselor financiare si eliminarea erorilor umane, '
                    'oferind o solutie de contabilitate automata, simplificata si adaptata antreprenorilor si '
                    'freelancerilor.</p>'
                    '<p><strong>Ce ofera FIN-TAXY:</strong></p>'
                    '<ul>'
                    '<li>Automatizarea completa a activitatilor contabile</li>'
                    '<li>Eliminarea necesitatii utilizarii foilor de calcul</li>'
                    '<li>Reducerea stresului cauzat de termene-limita si obligatii fiscale</li>'
                    '<li>Asistenta bazata pe AI, completata de interventie umana specializata</li>'
                    '</ul>'
                    '<p>Ne bucuram ca aceasta initiativa inovatoare s-a lansat chiar in Chisinau - un oras in '
                    'plin proces de transformare digitala si sustinere activa a ecosistemului antreprenorial.</p>'
                ),
                'image_src': 'success-stories/story9.webp',
                'order': 9,
            },
        ]

        for data in stories_data:
            image_path = self._copy_image(data['image_src'], 'stories')
            is_featured = data['company_name'] in homepage_companies

            story, created = SuccessStory.objects.get_or_create(
                company_name=data['company_name'],
                defaults={
                    'title': data['title'],
                    'category': data['category'],
                    'short_description': data['short_description'],
                    'content': data['content'],
                    'image': image_path,
                    'quote': data.get('quote', ''),
                    'is_featured': is_featured,
                    'order': data['order'],
                },
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] SuccessStory: {story.company_name}')

    # ------------------------------------------------------------------
    # Partners
    # ------------------------------------------------------------------

    def load_partners(self):
        self.stdout.write('\n--- Partners ---')

        partners_data = [
            {
                'name': 'TIKA',
                'logo_file': 'tika.webp',
                'description': 'Agentia Turca de Cooperare si Coordonare',
                'partner_type': 'internal',
                'order': 1,
            },
            {
                'name': 'Fundatia ALT',
                'logo_file': 'ALTFoundation.webp',
                'description': 'Suport pentru dezvoltarea antreprenoriatului social',
                'partner_type': 'internal',
                'order': 2,
            },
            {
                'name': 'CCI Moldova',
                'logo_file': 'CCI.webp',
                'description': 'Camera de Comert si Industrie a Republicii Moldova',
                'partner_type': 'internal',
                'order': 3,
            },
            {
                'name': 'EURObridge',
                'logo_file': 'EURObridge.webp',
                'description': 'Program de cooperare transfrontaliera',
                'partner_type': 'international',
                'order': 4,
            },
            {
                'name': 'FINEDU',
                'logo_file': 'FinEdu.webp',
                'description': 'Educatie financiara si antreprenoriala',
                'partner_type': 'internal',
                'order': 5,
            },
            {
                'name': 'Startup Moldova',
                'logo_file': 'StartupMoldova.webp',
                'description': 'Asociatia pentru dezvoltarea ecosistemului startup',
                'partner_type': 'internal',
                'order': 6,
            },
            {
                'name': 'UN Women',
                'logo_file': 'UNWomen.webp',
                'description': 'Entitatea Natiunilor Unite pentru egalitatea de gen',
                'partner_type': 'international',
                'order': 7,
            },
            {
                'name': 'Uniunea Europeana',
                'logo_file': 'EU.webp',
                'description': 'Programe de finantare si dezvoltare',
                'partner_type': 'international',
                'order': 8,
            },
        ]

        for data in partners_data:
            logo_path = self._copy_image(data['logo_file'], 'partners')

            partner, created = Partner.objects.get_or_create(
                name=data['name'],
                defaults={
                    'logo': logo_path,
                    'description': data['description'],
                    'partner_type': data['partner_type'],
                    'order': data['order'],
                    'is_active': True,
                },
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] Partner: {partner.name}')

    # ------------------------------------------------------------------
    # EU Projects
    # ------------------------------------------------------------------

    def load_eu_projects(self):
        self.stdout.write('\n--- EU Projects ---')

        projects_data = [
            {
                'title': 'EUroBRIDGE_UA_MD',
                'description': 'Program de cooperare transfrontaliera pentru dezvoltarea antreprenoriatului',
                'funder': 'Uniunea Europeana',
                'status': 'active',
                'order': 1,
            },
            {
                'title': 'PNUD - Comunitati reziliente',
                'description': 'Dezvoltarea comunitatilor locale prin antreprenoriat sustenabil',
                'funder': 'PNUD',
                'status': 'active',
                'order': 2,
            },
            {
                'title': 'SOCIALCAP',
                'description': 'Capital social pentru intreprinderi sociale si inovatie',
                'funder': 'Uniunea Europeana',
                'status': 'active',
                'order': 3,
            },
            {
                'title': 'DIGICROSS',
                'description': 'Digitalizare si cooperare transfrontaliera',
                'funder': 'Uniunea Europeana',
                'status': 'active',
                'order': 4,
            },
            {
                'title': 'CEDDI',
                'description': 'Centru de excelenta pentru dezvoltare digitala si inovatie',
                'funder': 'Uniunea Europeana',
                'status': 'active',
                'order': 5,
            },
            {
                'title': 'GrowthUP Chisinau',
                'description': 'Accelerator de crestere pentru startup-uri locale',
                'funder': 'Uniunea Europeana',
                'status': 'active',
                'order': 6,
            },
            {
                'title': 'GEN-E',
                'description': 'Retea globala de antreprenoriat pentru tineri',
                'funder': 'Uniunea Europeana',
                'status': 'active',
                'order': 7,
            },
        ]

        for data in projects_data:
            project, created = EUProject.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'funder': data['funder'],
                    'status': data['status'],
                    'order': data['order'],
                },
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] EUProject: {project.title}')

    # ------------------------------------------------------------------
    # Gallery Photos
    # ------------------------------------------------------------------

    def load_gallery_photos(self):
        self.stdout.write('\n--- Gallery Photos ---')

        # All photo files from static/img/ matching the pattern
        photo_files = sorted([
            'photo_1_2026-02-08_01-46-56.webp',
            'photo_2_2026-02-08_01-46-56.webp',
            'photo_3_2026-02-08_01-46-56.webp',
            'photo_4_2026-02-08_01-46-56.webp',
            'photo_5_2026-02-08_01-46-56.webp',
            'photo_6_2026-02-08_01-46-56.webp',
            'photo_7_2026-02-08_01-46-56.webp',
            'photo_8_2026-02-08_01-46-56.webp',
            'photo_9_2026-02-08_01-46-56.webp',
            'photo_10_2026-02-08_01-46-56.webp',
            'photo_11_2026-02-08_01-46-56.webp',
            'photo_12_2026-02-08_01-46-56.webp',
            'photo_13_2026-02-08_01-46-56.webp',
            'photo_14_2026-02-08_01-46-56.webp',
            'photo_15_2026-02-08_01-46-56.webp',
            'photo_16_2026-02-08_01-46-56.webp',
            'photo_17_2026-02-08_01-46-56.webp',
            'photo_18_2026-02-08_01-46-56.webp',
            'photo_19_2026-02-08_01-46-56.webp',
            'photo_20_2026-02-08_01-46-56.webp',
            'photo_21_2026-02-08_01-46-56.webp',
            'photo_22_2026-02-08_01-46-56.webp',
            'photo_23_2026-02-08_01-46-56.webp',
            'photo_24_2026-02-08_01-46-56.webp',
            'photo_25_2026-02-08_01-46-56.webp',
            'photo_26_2026-02-08_01-46-56.webp',
            'photo_27_2026-02-08_01-46-56.webp',
            'photo_28_2026-02-08_01-46-56.webp',
            'photo_29_2026-02-08_01-46-56.webp',
            'photo_30_2026-02-08_01-46-56.webp',
            'photo_31_2026-02-08_01-46-56.webp',
            'photo_32_2026-02-08_01-46-56.webp',
            'photo_33_2026-02-08_01-46-56.webp',
            'photo_34_2026-02-08_01-46-56.webp',
            'photo_35_2026-02-08_01-46-56.webp',
            'photo_36_2026-02-08_01-46-56.webp',
            'photo_1_2026-02-08_01-50-15.webp',
            'photo_2_2026-02-08_01-50-15.webp',
            'photo_3_2026-02-08_01-50-15.webp',
            'photo_4_2026-02-08_01-50-15.webp',
        ])

        for idx, filename in enumerate(photo_files, start=1):
            image_path = self._copy_image(filename, 'gallery')

            photo, created = GalleryPhoto.objects.get_or_create(
                image=image_path,
                defaults={
                    'caption': '',
                    'order': idx,
                },
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] GalleryPhoto: {filename}')

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def load_statistics(self):
        self.stdout.write('\n--- Statistics ---')

        stats_data = [
            # --- Impact general (from index.html) ---
            {
                'key': 'consultations',
                'value': '4215',
                'suffix': '+',
                'decimal_places': 0,
                'label': 'consultatii individuale',
                'icon_class': 'fas fa-chart-line',
                'category': 'impact',
                'order': 1,
            },
            {
                'key': 'beneficiaries',
                'value': '7733',
                'suffix': '+',
                'decimal_places': 0,
                'label': 'beneficiari instruiti',
                'icon_class': 'fas fa-graduation-cap',
                'category': 'impact',
                'order': 2,
            },
            {
                'key': 'investments',
                'value': '33.3',
                'suffix': ' mil. lei',
                'decimal_places': 1,
                'label': 'investitii atrase',
                'icon_class': 'fas fa-rocket',
                'category': 'impact',
                'order': 3,
            },
            # --- Programs (STARTUP) from index.html ---
            {
                'key': 'startup_applications',
                'value': '82',
                'suffix': '+',
                'decimal_places': 0,
                'label': 'dosare procesate',
                'icon_class': 'fas fa-rocket',
                'category': 'programs',
                'order': 1,
            },
            {
                'key': 'startup_funded',
                'value': '16',
                'suffix': '',
                'decimal_places': 0,
                'label': 'proiecte finantate',
                'icon_class': 'fas fa-rocket',
                'category': 'programs',
                'order': 2,
            },
            {
                'key': 'startup_jobs',
                'value': '450',
                'suffix': '+',
                'decimal_places': 0,
                'label': 'locuri de munca',
                'icon_class': 'fas fa-rocket',
                'category': 'programs',
                'order': 3,
            },
            {
                'key': 'startup_pending',
                'value': '69',
                'suffix': '',
                'decimal_places': 0,
                'label': 'cereri in evaluare',
                'icon_class': 'fas fa-rocket',
                'category': 'programs',
                'order': 4,
            },
            # --- Supporting stats (from index.html bottom row) ---
            {
                'key': 'mentors',
                'value': '15',
                'suffix': '',
                'decimal_places': 0,
                'label': 'mentori specializati',
                'icon_class': 'fas fa-users',
                'category': 'impact',
                'order': 4,
            },
            {
                'key': 'hackathons',
                'value': '4',
                'suffix': '',
                'decimal_places': 0,
                'label': 'hackathoane & AI School',
                'icon_class': 'fas fa-lightbulb',
                'category': 'impact',
                'order': 5,
            },
            {
                'key': 'ima_growth',
                'value': '600',
                'suffix': '%',
                'decimal_places': 0,
                'label': 'crestere cifra afaceri IMA',
                'icon_class': 'fas fa-building',
                'category': 'ima',
                'order': 1,
            },
            # --- IMA stats (from ima.html) ---
            {
                'key': 'ima_residents',
                'value': '11',
                'suffix': '',
                'decimal_places': 0,
                'label': 'Rezidenti activi',
                'icon_class': 'fas fa-building',
                'category': 'ima',
                'order': 2,
            },
            {
                'key': 'ima_applications',
                'value': '20',
                'suffix': '',
                'decimal_places': 0,
                'label': 'Aplicatii primite',
                'icon_class': 'fas fa-clipboard-list',
                'category': 'ima',
                'order': 3,
            },
            # --- Partners stats (from parteneri.html) ---
            {
                'key': 'partners_count',
                'value': '25',
                'suffix': '',
                'decimal_places': 0,
                'label': 'Parteneri din 8 tari europene',
                'icon_class': 'fas fa-globe',
                'category': 'partners',
                'order': 1,
            },
            {
                'key': 'partners_projects_value',
                'value': '70',
                'suffix': ' mil. lei',
                'decimal_places': 0,
                'label': 'Proiecte si propuneri',
                'icon_class': 'fas fa-briefcase',
                'category': 'partners',
                'order': 2,
            },
            {
                'key': 'partners_active_programs',
                'value': '15',
                'suffix': '+',
                'decimal_places': 0,
                'label': 'Programe active',
                'icon_class': 'fas fa-handshake',
                'category': 'partners',
                'order': 3,
            },
        ]

        for data in stats_data:
            stat, created = Statistic.objects.get_or_create(
                key=data['key'],
                defaults={
                    'value': data['value'],
                    'suffix': data['suffix'],
                    'decimal_places': data['decimal_places'],
                    'label': data['label'],
                    'icon_class': data['icon_class'],
                    'category': data['category'],
                    'order': data['order'],
                },
            )
            status = 'CREATED' if created else 'EXISTS'
            self.stdout.write(f'  [{status}] Statistic: {stat.key} = {stat.value}{stat.suffix}')
