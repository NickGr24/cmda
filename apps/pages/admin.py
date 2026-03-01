from django.contrib import admin
from django.utils.html import format_html
from .models import SuccessStory, Partner, EUProject, GalleryEvent, GalleryPhoto, Program, Statistic, Mentor, News, NewsImage, Document


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


class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 1
    fields = ['image', 'caption', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;">', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(GalleryEvent)
class GalleryEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'photo_count', 'order', 'cover_preview']
    list_editable = ['order']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryPhotoInline]

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.cover_image.url)
        return '-'
    cover_preview.short_description = 'Copertă'

    def photo_count(self, obj):
        count = obj.photos.count()
        return f'{count} foto' if count else '-'
    photo_count.short_description = 'Fotografii'


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


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ['image', 'caption', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;">', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'image_count', 'image_preview']
    list_filter = ['published_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    inlines = [NewsImageInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.image.url)
        return '-'
    image_preview.short_description = 'Foto'

    def image_count(self, obj):
        count = obj.images.count()
        return f'{count} img' if count else '-'
    image_count.short_description = 'Galerie'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'file_type', 'order', 'created_at']
    list_filter = ['category']
    list_editable = ['order']
    search_fields = ['title']

    def file_type(self, obj):
        return obj.file_extension or '-'
    file_type.short_description = 'Tip'
