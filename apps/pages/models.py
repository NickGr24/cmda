from django.db import models
from django.utils.text import slugify


class SuccessStory(models.Model):
    title = models.CharField('Titlu', max_length=300)
    slug = models.SlugField('Slug', unique=True)
    company_name = models.CharField('Companie', max_length=200)
    category = models.CharField('Categorie', max_length=50, help_text='Ex: IT & AI, FinTech, Textile')
    short_description = models.TextField('Descriere scurtă', help_text='Previzualizare pe pagina principală')
    content = models.TextField('Conținut complet', help_text='HTML permis')
    image = models.ImageField('Imagine', upload_to='stories/')
    quote = models.TextField('Citat fondator', blank=True)
    is_featured = models.BooleanField('Pe pagina principală', default=False)
    order = models.IntegerField('Ordine', default=0)
    created_at = models.DateTimeField('Data creării', auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Istorie de succes'
        verbose_name_plural = 'Istorii de succes'

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        super().save(*args, **kwargs)


class Partner(models.Model):
    PARTNER_TYPES = [
        ('internal', 'Intern'),
        ('international', 'Internațional'),
    ]

    name = models.CharField('Nume', max_length=200)
    logo = models.ImageField('Logo', upload_to='partners/')
    website_url = models.URLField('Website', blank=True)
    description = models.TextField('Descriere', blank=True)
    partner_type = models.CharField('Tip', max_length=20, choices=PARTNER_TYPES, default='internal')
    order = models.IntegerField('Ordine', default=0)
    is_active = models.BooleanField('Activ', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Partener'
        verbose_name_plural = 'Parteneri'

    def __str__(self):
        return self.name


class EUProject(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activ'),
        ('completed', 'Finalizat'),
    ]

    title = models.CharField('Titlu', max_length=300)
    description = models.TextField('Descriere')
    funder = models.CharField('Finanțator', max_length=200, blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='active')
    order = models.IntegerField('Ordine', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Proiect european'
        verbose_name_plural = 'Proiecte europene'

    def __str__(self):
        return self.title


class GalleryPhoto(models.Model):
    image = models.ImageField('Imagine', upload_to='gallery/')
    caption = models.CharField('Descriere', max_length=200, blank=True)
    order = models.IntegerField('Ordine', default=0)
    created_at = models.DateTimeField('Data', auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Fotografie'
        verbose_name_plural = 'Galerie foto'

    def __str__(self):
        return self.caption or f'Foto #{self.pk}'


class Program(models.Model):
    title = models.CharField('Titlu', max_length=300)
    slug = models.SlugField('Slug', unique=True)
    badge = models.CharField('Badge', max_length=50, help_text='Ex: Consultanță, Educație, Granturi')
    icon_class = models.CharField('Icon CSS class', max_length=100, blank=True, help_text='Font Awesome class')
    short_description = models.TextField('Descriere scurtă')
    content = models.TextField('Conținut complet', help_text='HTML permis')
    image = models.ImageField('Imagine', upload_to='programs/', blank=True)
    highlight_number = models.CharField('Număr evidențiat', max_length=50, blank=True, help_text='Ex: 4215')
    highlight_text = models.CharField('Text evidențiat', max_length=200, blank=True, help_text='Ex: consultații oferite')
    is_featured = models.BooleanField('Featured (full-width)', default=False)
    cta_text = models.CharField('Text buton CTA', max_length=100, blank=True)
    cta_url = models.URLField('URL buton CTA', blank=True)
    order = models.IntegerField('Ordine', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Program'
        verbose_name_plural = 'Programe'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Statistic(models.Model):
    CATEGORIES = [
        ('impact', 'Impact general'),
        ('programs', 'Programe'),
        ('ima', 'IMA / Infrastructură'),
        ('partners', 'Parteneri'),
    ]

    key = models.CharField('Cheie', max_length=100, unique=True, help_text='Ex: consultations, beneficiaries')
    value = models.CharField('Valoare', max_length=50, help_text='Ex: 4215, 33.3')
    suffix = models.CharField('Sufix', max_length=50, blank=True, help_text='Ex: +, mil. lei, %')
    decimal_places = models.IntegerField('Zecimale', default=0, help_text='Pentru animația data-decimal')
    label = models.CharField('Etichetă', max_length=200, help_text='Ex: consultații oferite')
    icon_class = models.CharField('Icon CSS class', max_length=100, blank=True)
    category = models.CharField('Categorie', max_length=20, choices=CATEGORIES)
    order = models.IntegerField('Ordine', default=0)

    class Meta:
        ordering = ['category', 'order']
        verbose_name = 'Statistică'
        verbose_name_plural = 'Statistici'

    def __str__(self):
        return f'{self.label}: {self.value}{self.suffix}'


class Mentor(models.Model):
    name = models.CharField('Nume', max_length=200)
    specialization = models.CharField('Specializare', max_length=200)
    bio = models.TextField('Biografie', blank=True)
    photo = models.ImageField('Foto', upload_to='mentors/', blank=True)
    order = models.IntegerField('Ordine', default=0)
    is_active = models.BooleanField('Activ', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentori'

    def __str__(self):
        return f'{self.name} — {self.specialization}'


class News(models.Model):
    title = models.CharField('Titlu', max_length=500)
    slug = models.SlugField('Slug', unique=True, max_length=500)
    excerpt = models.TextField('Rezumat', blank=True)
    content = models.TextField('Conținut', help_text='HTML permis')
    image = models.ImageField('Imagine', upload_to='news/', blank=True)
    published_date = models.DateField('Data publicării')
    source_url = models.URLField('URL sursă', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Comunicat'
        verbose_name_plural = 'Comunicate'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:500]
        super().save(*args, **kwargs)
