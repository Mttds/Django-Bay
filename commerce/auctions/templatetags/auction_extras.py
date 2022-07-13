from django.template.defaultfilters import register

# custom filters to be used in the templating engine for the auctions app
# the app must be included in the INSTALLED_APPS in settings
# this file must be in a directory called templatetags under the application folder (i.e auctions)
# and the __init__.py should be present to mark it as a python module
@register.filter(name='dict_key')
def dict_key(d, k):
    """Returns the given key from a dictionary."""
    return d[k]
