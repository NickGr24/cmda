from django.db.models import Count
from django.views.generic import TemplateView, DetailView
from .models import SuccessStory, Partner, EUProject, GalleryEvent, GalleryPhoto, Program, Statistic, Mentor, News, Document


class PageView(TemplateView):
    """Base view for all pages. Provides active_page context for nav highlighting."""
    active_page = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = self.active_page
        return context


class IndexView(PageView):
    template_name = 'pages/index.html'
    active_page = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_stories'] = SuccessStory.objects.filter(is_featured=True)
        context['all_stories'] = SuccessStory.objects.all()
        context['partners'] = Partner.objects.filter(is_active=True)
        context['programs'] = Program.objects.all()
        context['stats'] = {s.key: s for s in Statistic.objects.all()}
        context['latest_news'] = News.objects.all()[:5]
        return context


class DespreView(PageView):
    template_name = 'pages/despre.html'
    active_page = 'despre'


class ProgrameView(PageView):
    template_name = 'pages/programe.html'
    active_page = 'programe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.all()
        context['stats'] = {s.key: s for s in Statistic.objects.filter(category='programs')}
        context['mentors'] = Mentor.objects.filter(is_active=True)
        return context


class ImaView(PageView):
    template_name = 'pages/ima.html'
    active_page = 'ima'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {s.key: s for s in Statistic.objects.filter(category='ima')}
        return context


class ContacteView(PageView):
    template_name = 'pages/contacte.html'
    active_page = 'contacte'


class GalerieView(PageView):
    template_name = 'pages/galerie.html'
    active_page = 'galerie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = GalleryEvent.objects.annotate(photo_count=Count('photos'))
        return context


class GalleryEventDetailView(DetailView):
    model = GalleryEvent
    template_name = 'pages/galerie_event.html'
    context_object_name = 'event'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('photos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'galerie'
        context['photos'] = self.object.photos.all()
        return context


class IstoriiView(PageView):
    template_name = 'pages/istorii-de-succes.html'
    active_page = 'istorii-de-succes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stories'] = SuccessStory.objects.all()
        return context


class SuccessStoryDetailView(DetailView):
    model = SuccessStory
    template_name = 'pages/story_detail.html'
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'istorii-de-succes'
        return context


class ParteneriView(PageView):
    template_name = 'pages/parteneri.html'
    active_page = 'parteneri'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partners'] = Partner.objects.filter(is_active=True)
        context['eu_projects'] = EUProject.objects.all()
        context['stats'] = {s.key: s for s in Statistic.objects.filter(category='partners')}
        return context


class ComunicateView(PageView):
    template_name = 'pages/comunicate.html'
    active_page = 'comunicate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all()
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'pages/news_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'comunicate'
        context['gallery_images'] = self.object.images.all()
        return context


class PlanuriView(PageView):
    template_name = 'pages/planuri.html'
    active_page = 'planuri'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['planuri'] = Document.objects.filter(category='planuri').order_by('-order')
        context['rapoarte'] = Document.objects.filter(category='rapoarte').order_by('-order')
        context['declaratii'] = Document.objects.filter(category='declaratii').order_by('-order')
        return context


class RapoarteView(PageView):
    template_name = 'pages/planuri.html'
    active_page = 'planuri'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['planuri'] = Document.objects.filter(category='planuri').order_by('-order')
        context['rapoarte'] = Document.objects.filter(category='rapoarte').order_by('-order')
        context['declaratii'] = Document.objects.filter(category='declaratii').order_by('-order')
        return context


class AchizitiiView(PageView):
    template_name = 'pages/achizitii.html'
    active_page = 'achizitii'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['planuri'] = Document.objects.filter(category='achizitii_planuri').order_by('-order')
        context['anunturi'] = Document.objects.filter(category='achizitii_anunturi').order_by('-order')
        context['rapoarte'] = Document.objects.filter(category='achizitii_rapoarte').order_by('-order')
        return context


class CarieraView(PageView):
    template_name = 'pages/cariera.html'
    active_page = 'cariera'


class DeplasariView(PageView):
    template_name = 'pages/deplasari.html'
    active_page = 'deplasari'


class ProtectiaDatelorView(PageView):
    template_name = 'pages/protectia-datelor.html'
    active_page = 'protectia-datelor'


class IntegritateView(PageView):
    template_name = 'pages/integritate.html'
    active_page = 'integritate'


class StructuraView(PageView):
    template_name = 'pages/structura.html'
    active_page = 'structura'


class EchipaView(PageView):
    template_name = 'pages/echipa.html'
    active_page = 'echipa'


class BugetView(PageView):
    template_name = 'pages/buget.html'
    active_page = 'buget'


class ProiecteView(PageView):
    template_name = 'pages/proiecte.html'
    active_page = 'proiecte'


class LegislatieView(PageView):
    template_name = 'pages/legislatie.html'
    active_page = 'legislatie'
