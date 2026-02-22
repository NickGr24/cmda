import json
from django.http import JsonResponse
from django.views import View
from .forms import ContactForm


class ContactFormView(View):
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
