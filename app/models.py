from datetime import date

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils.encoding import python_2_unicode_compatible
from django import forms

from wagtail.wagtailcore.models import Page, Orderable, ClusterableModel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailsearch import index

from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from app.utils import export_event


EVENT_AUDIENCE_CHOICES = (
    ('public', "Public"),
    ('private', "Private"),
)

# Global Streamfield definition


class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"


class CustomStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")


# A couple of abstract classes that contain commonly used fields

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True


# Logo snippet

@register_snippet
@python_2_unicode_compatible
class Logo(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    caption = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
        FieldPanel('is_active'),
    ]

    def save(self, *args, **kwargs):
        if self.is_active:
            for other_logo in Logo.objects.exclude(id=self.id):
                other_logo.is_active = False
                other_logo.save()
        super(Logo, self).save(*args, **kwargs)

    def __str__(self):
        _str = 'Logo object'
        if self.caption:
            _str = self.caption
        return _str + ' (Active)' if self.is_active else _str


# Carousel items

class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Pennant Items

class PennantItem(LinkFields):
    '''
    Pennants are small flags made up of a Font Awesome icon, a header,
    a caption and an embed url.
    '''
    header = models.CharField(max_length=126, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    fa_icon = models.CharField(
        'Font Awesome Icon',
        max_length=30,
        blank=True,
        help_text='Copy the name of any icon from fontawesome.io/icons/'
    )

    panels = [
        FieldPanel('fa_icon'),
        FieldPanel('header'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, 'Link'),
    ]

    class Meta:
        abstract = True



# Related links

class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Sidebar items

class SidebarItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=30, help_text="Sidebar title")
    body = models.CharField(max_length=255, null=True, blank=True)
    button_text = models.CharField(max_length=30, null=True, blank=True)
    show_related_links = models.BooleanField(default=False)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('body'),
        MultiFieldPanel(LinkFields.panels, "Link"),
        FieldPanel('button_text'),
        FieldPanel('show_related_links'),
    ]


# Advert Snippet

class AdvertPlacement(models.Model):
    page = ParentalKey('wagtailcore.Page', related_name='advert_placements')
    advert = models.ForeignKey('app.Advert', related_name='+')


@register_snippet
@python_2_unicode_compatible
class Advert(models.Model):
    page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='adverts',
        null=True,
        blank=True
    )
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('url'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text


# Social snippet

@register_snippet
@python_2_unicode_compatible
class Social(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image',
        related_name='+'
    )
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    def __str__(self):
        return self.name


# Home Page

class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('app.HomePage', related_name='carousel_items')


class HomePagePennantItem(Orderable, PennantItem):
    page = ParentalKey('app.HomePage', related_name='pennant_items')


class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('app.HomePage', related_name='related_links')


class HomePagePromotion(Orderable):
    promotion_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='promotion_pages',
        null=True,
        blank=True
    )
    header = models.CharField(max_length=24)
    page = ParentalKey('app.HomePage', related_name='promotions')

    panels = [
        PageChooserPanel('promotion_page'),
        FieldPanel('header'),
    ]


class HomePageFooterPromotion(Orderable):
    promotion_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='footer_promotion_pages',
        null=True,
        blank=True
    )
    header = models.CharField(max_length=24)
    page = ParentalKey('app.HomePage', related_name='footer_promotions')

    panels = [
        PageChooserPanel('promotion_page'),
        FieldPanel('header'),
    ]


class HomePage(Page):
    logo_text = models.CharField(max_length=24, null=True, blank=True)
    logo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    banner_header = models.CharField(max_length=48, null=True, blank=True)
    banner_caption = models.CharField(max_length=256, null=True, blank=True)
    body = StreamField(CustomStreamBlock())
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    StreamFieldPanel('body'),
    FieldPanel('logo_text'),
    ImageChooserPanel('logo_image'),
    ImageChooserPanel('banner_image'),
    FieldPanel('banner_header'),
    FieldPanel('banner_caption'),
    InlinePanel('carousel_items', label="Carousel items"),
    InlinePanel('pennant_items', label='Penant items'),
    InlinePanel('promotions', label='Promotions'),
    InlinePanel('footer_promotions', label='Footer Promotions'),
    InlinePanel('related_links', label="Related links"),
]

HomePage.promote_panels = Page.promote_panels


# Standard index page


class StandardIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('app.StandardIndexPage', related_name='related_links')


class StandardIndexPage(Page):
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    parent_page_types = ['app.HomePage']
    subpage_types = ['app.StandardPage', 'app.FormPage']

StandardIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('related_links', label="Related links"),
]

StandardIndexPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


# Standard page

class StandardPageSidebarItem(Orderable, SidebarItem):
    page = ParentalKey('app.StandardPage', related_name='sidebar_items')


class StandardPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('app.StandardPage', related_name='carousel_items')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('app.StandardPage', related_name='related_links')


SIDEBAR_CHOICES = (
    ('no_sidebar', 'No  Sidebar'),
    ('left_sidebar', 'Left Sidebar'),
    ('right_sidebar', 'Right Sidebar')
)


class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    sidebar = models.CharField(
        max_length=13,
        choices=SIDEBAR_CHOICES,
        default='no_sidebar'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    parent_page_types = [
        'app.HomePage',
        'app.StandardPage',
        'app.StandardIndexPage'
    ]
    subpage_types = []

    def get_context(self, request):
        context = super(StandardPage, self).get_context(request)
        context['base_template'] = "app/base_{}.html".format(self.sidebar)
        return context


StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    FieldPanel('body', classname="full"),
    FieldPanel('sidebar', classname="full"),
    InlinePanel('sidebar_items', label="Sidebar items"),
    InlinePanel('carousel_items', label="Carousel items"),
    InlinePanel('related_links', label="Related links"),
]

StandardPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]

# Contact page

class ContactPage(Page, ContactFields):
    body = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    parent_page_types = [
        'app.HomePage',
        'app.StandardPage',
        'app.StandardIndexPage'
    ]
    subpage_types = []

ContactPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    MultiFieldPanel(ContactFields.panels, "Contact"),
]

ContactPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]

# Forms

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPageSidebarItem(Orderable, SidebarItem):
    page = ParentalKey('app.FormPage', related_name='sidebar_items')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    sidebar = models.CharField(
        max_length=13,
        choices=SIDEBAR_CHOICES,
        default='no_sidebar'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    parent_page_types = [
        'app.HomePage',
        'app.StandardPage',
        'app.StandardIndexPage'
    ]
    subpage_types = []

    def get_context(self, request):
        context = super(FormPage, self).get_context(request)
        context['base_template'] = "app/base_{}.html".format(self.sidebar)
        return context

FormPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('form_fields', label="Form fields"),
    FieldPanel('thank_you_text', classname="full"),
    FieldPanel('sidebar', classname="full"),
    InlinePanel('sidebar_items', label="Sidebar items"),
    MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('from_address', classname="col6"),
            FieldPanel('to_address', classname="col6"),
        ]),
        FieldPanel('subject'),
    ], "Email"),
]

FormPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]
