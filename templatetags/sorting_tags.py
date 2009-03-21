from django import template
from django.http import Http404
from django.conf import settings

register = template.Library()

DEFAULT_SORT_UP = getattr(settings, 'DEFAULT_SORT_UP' , '&uarr;')
DEFAULT_SORT_DOWN = getattr(settings, 'DEFAULT_SORT_DOWN' , '&darr;')

sort_directions = {
    'asc': {'icon':DEFAULT_SORT_UP, 'inverse':'desc'}, 
    'desc': {'icon':DEFAULT_SORT_DOWN, 'inverse':'asc'}, 
    '': {'icon':DEFAULT_SORT_DOWN, 'inverse':'asc'}, 
}

def th(parser, token):
    """
    Parses a tag that's supposed to be in this format:
    {% sth field title%}    
    """
    bits = token.contents.split()
    if len(bits) < 2:
        raise TemplateSyntaxError, "th tag takes at least 1 argument"
    try:
        title = bits[2]
    except IndexError:
        title = bits[1].capitalize()
    return SortHeaderNode(bits[1].strip(), title.strip())
    

class SortHeaderNode(template.Node):
    """
    Renedrs a <th> HTML tag with a link which href attribute 
    includes the field on which we sort and the direction.
    and adds an up or down arrow if the field is the one 
    currently being sorted on.

    Eg.
        {% th name Name %} generates
        <th><a href="?sort=name" title="Name">Name</a></th>

    """
    def __init__(self, field, title):
        self.field = field
        self.title = title

    def render(self, context):
        getvars = context['request'].GET.copy()
        if 'sort' in getvars:
            sortby = getvars['sort']
            del getvars['sort']
        else:
            sortby = ''
        if 'dir' in getvars:
            sortdir = getvars['dir']
            del getvars['dir']
        else:
            sortdir = ''
        if sortby == self.field:
            getvars['dir'] = sort_directions[sortdir]['inverse']
            icon = sort_directions[sortdir]['icon']
        else:
            icon = ''
        if len(getvars.keys()) > 0:
            urlappend = "&%s" % getvars.urlencode()
        else:
            urlappend = ''
        self.title = "%s %s" % (self.title, icon)

        url = '?sort=%s%s' % (self.field, urlappend)
        return '<th><a href="%s" title="%s">%s</a></th>' % (url, self.title,
                self.title)


def autosort(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError, "autosort tag takes exactly one argument"
    return SortedDataNode(bits[1])

class SortedDataNode(template.Node):
    """
        automatically sort a queryset with 
        {% autosort queryset %}
    """
    def __init__(self, queryset_var, context_var=None):
        self.queryset_var = template.Variable(queryset_var)
        self.context_var = context_var

    def render(self, context):
        key = self.queryset_var.var
        value = self.queryset_var.resolve(context)
        order_by = context['request'].field
        if len(order_by) > 1:
            context[key] = value.order_by(order_by)
        else:
            context[key] = value

        return ''


th = register.tag(th)
autosort = register.tag(autosort)

