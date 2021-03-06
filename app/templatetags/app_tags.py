from datetime import date
from django import template
from django.conf import settings

from app.models import (
    Advert,
    ContactPage,
    FormPage,
    Logo,
    Page,
    Social,
    StandardIndexPage,
    StandardPage
)

register = template.Library()


# settings value
@register.simple_tag()
def get_google_maps_key():
    return getattr(settings, 'GOOGLE_MAPS_KEY', "")


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('app/tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    parent.active = (calling_page.url == '/'
                     if calling_page else False)
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'parent': parent,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('app/tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

@register.inclusion_tag('app/tags/logo.html', takes_context=True)
def logo(context):
    return {
        'logo_image': getattr(get_site_root(context).specific, 'logo_image', ''),
        'logo_text': getattr(get_site_root(context).specific, 'logo_text', ''),
        'request': context['request'],
    }

# Page promotion for footer
@register.inclusion_tag(
    'app/tags/footer_promotions.html',
    takes_context=True
)
def footer_promotions(context, count=2):
    promos = getattr(get_site_root(context).specific, 'footer_promotions', None),
    if type(promos) is tuple:
        promos = promos[0]
    if promos:
        promos = promos.all()
        promos[:count]
    return {
        'footer_promotions': promos if promos else '',
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

@register.inclusion_tag('app/tags/contact_footer.html', takes_context=True)
def contact_footer(context):
    return {
        'contact': ContactPage.objects.live().first(),
        'request': context['request'],
    }


# Advert snippets
@register.inclusion_tag('app/tags/adverts.html', takes_context=True)
def adverts(context):
    return {
        'adverts': Advert.objects.select_related('page'),
        'request': context['request'],
    }


# Social snippets
@register.inclusion_tag('app/tags/social.html', takes_context=True)
def socials(context):
    return {
        'socials': Social.objects.all(),
        'request': context['request'],
    }



@register.inclusion_tag('app/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=2)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }
