from modeltranslation.translator import register, TranslationOptions
from .models import (
    SuccessStory, Partner, EUProject, GalleryEvent, GalleryPhoto,
    Program, Statistic, Mentor, News, NewsImage, Document,
)


@register(SuccessStory)
class SuccessStoryTO(TranslationOptions):
    fields = ('title', 'company_name', 'category', 'short_description', 'content', 'quote')


@register(Partner)
class PartnerTO(TranslationOptions):
    fields = ('name', 'description')


@register(EUProject)
class EUProjectTO(TranslationOptions):
    fields = ('title', 'description', 'funder')


@register(GalleryEvent)
class GalleryEventTO(TranslationOptions):
    fields = ('title', 'description')


@register(GalleryPhoto)
class GalleryPhotoTO(TranslationOptions):
    fields = ('caption',)


@register(Program)
class ProgramTO(TranslationOptions):
    fields = ('title', 'badge', 'short_description', 'content', 'highlight_text', 'cta_text')


@register(Statistic)
class StatisticTO(TranslationOptions):
    fields = ('label', 'suffix')


@register(Mentor)
class MentorTO(TranslationOptions):
    fields = ('name', 'specialization', 'bio')


@register(News)
class NewsTO(TranslationOptions):
    fields = ('title', 'excerpt', 'content')


@register(NewsImage)
class NewsImageTO(TranslationOptions):
    fields = ('caption',)


@register(Document)
class DocumentTO(TranslationOptions):
    fields = ('title',)
