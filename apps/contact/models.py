from django.db import models


class ContactSubmission(models.Model):
    REQUEST_TYPES = [
        ('consultanta', 'Consultanță'),
        ('startup', 'Program STARTUP'),
        ('incubator', 'Incubator'),
        ('parteneriate', 'Parteneriate'),
        ('altele', 'Altele'),
    ]

    name = models.CharField('Nume', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Telefon', max_length=20, blank=True)
    request_type = models.CharField('Tip solicitare', max_length=50, choices=REQUEST_TYPES, blank=True)
    message = models.TextField('Mesaj')
    created_at = models.DateTimeField('Data', auto_now_add=True)
    is_read = models.BooleanField('Citit', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Solicitare'
        verbose_name_plural = 'Solicitări'

    def __str__(self):
        return f"{self.name} – {self.email} ({self.created_at:%Y-%m-%d})"
