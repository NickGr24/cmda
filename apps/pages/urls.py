from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('despre/', views.DespreView.as_view(), name='despre'),
    path('programe/', views.ProgrameView.as_view(), name='programe'),
    path('ima/', views.ImaView.as_view(), name='ima'),
    path('contacte/', views.ContacteView.as_view(), name='contacte'),
    path('galerie/', views.GalerieView.as_view(), name='galerie'),
    path('istorii-de-succes/', views.IstoriiView.as_view(), name='istorii-de-succes'),
    path('istorii-de-succes/<slug:slug>/', views.SuccessStoryDetailView.as_view(), name='story-detail'),
    path('parteneri/', views.ParteneriView.as_view(), name='parteneri'),
    path('comunicate/<slug:slug>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('comunicate/', views.ComunicateView.as_view(), name='comunicate'),
    path('planuri/', views.PlanuriView.as_view(), name='planuri'),
    path('rapoarte/', views.RapoarteView.as_view(), name='rapoarte'),
    path('achizitii/', views.AchizitiiView.as_view(), name='achizitii'),
    path('cariera/', views.CarieraView.as_view(), name='cariera'),
    path('deplasari/', views.DeplasariView.as_view(), name='deplasari'),
    path('integritate/', views.IntegritateView.as_view(), name='integritate'),
    path('structura/', views.StructuraView.as_view(), name='structura'),
    path('echipa/', views.EchipaView.as_view(), name='echipa'),
    path('buget/', views.BugetView.as_view(), name='buget'),
]
