from django.contrib import admin
from django.utils.html import format_html
from .models import SuccessStory, Partner, EUProject, GalleryPhoto, Program, Statistic, Mentor, News


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'category', 'is_featured', 'order', 'image_preview']
    list_filter = ['is_featured', 'category']
    list_editable = ['is_featured', 'order']
    search_fields = ['title', 'company_name', 'content']
    prepopulated_fields = {'slug': ('company_name',)}

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.image.url)
        return '-'
    image_preview.short_description = 'Foto'


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_type', 'is_active', 'order', 'logo_preview']
    list_filter = ['partner_type', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['name', 'description']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:30px;">', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'


@admin.register(EUProject)
class EUProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'funder', 'status', 'order']
    list_filter = ['status']
    list_editable = ['status', 'order']
    search_fields = ['title', 'description']


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order', 'created_at', 'image_preview']
    list_editable = ['order']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.image.url)
        return '-'
    image_preview.short_description = 'Foto'


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'badge', 'is_featured', 'highlight_number', 'order']
    list_filter = ['is_featured']
    list_editable = ['is_featured', 'order']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'suffix', 'label', 'category', 'order']
    list_filter = ['category']
    list_editable = ['value', 'suffix', 'order']
    search_fields = ['key', 'label']


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'is_active', 'order']
    list_filter = ['is_active', 'specialization']
    list_editable = ['is_active', 'order']
    search_fields = ['name', 'specialization']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'image_preview']
    list_filter = ['published_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.image.url)
        return '-'
    image_preview.short_description = 'Foto'
