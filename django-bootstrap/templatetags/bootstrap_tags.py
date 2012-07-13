from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def bootstrap_css():
    return mark_safe('<link href="http://twitter.github.com/bootstrap/'
                     'assets/css/bootstrap.css" rel="stylesheet">')

@register.simple_tag
def jquery(version='1.7.2'):
    return mark_safe('<script src="https://ajax.googleapis.com/ajax/libs/'
        'jquery/%s/jquery.min.js" type="text/javascript"></script>' % version)

@register.filter
def bootstrap(bound_field, args=''):
    """
    Enables easier bootstrap-compatible rendering of bound form fields.
    Optionally accepts a space-delimited string of arguments
    (e.g. "inline=True placeholder=E-mail span4 error")

    The following keyword arguments are recognized:
    * inline - simply adds the field, with no clearfix or input wrappers. This
      option should not be used unless you are using bootstrap to add other
      classes or a placeholder - if not, just render the field as usual.
    * placeholder - adds HTML5 placeholder text
    Other keyword arguments are ignored silently. Non-keyword arguments are
    passed to the template and included as the class of the input element.

    ..todo::
        * Support for weirder widgets:
          * Checkboxes
            * Fix existing checkbox html (TOS, others?)
          * Checkbox Multiple Selects
            * Add hooks for adding classes to div, ul, li and input elements
        * Consider bootstrap-inline tag that takes a list of elements, and wraps
          them in an inline. What would be the best way to style each of them
          (ref. address' city, state and zip with differing widths)
    """
    if not bound_field:
        return ''
    if hasattr(bound_field, 'visible_fields'):
        # bound_field is really a form. Bootstrap all the things.
        return mark_safe(
            '\n'.join([bootstrap(f, args) for f in bound_field.visible_fields()])
        )
    args = args.split()
    classes = '' # a ' '-delimited list of classes
    kwargs = {} # a dict of extra arguments
    for arg in args:
        if '=' in arg:
            k,v = arg.split('=')
            kwargs[k] = v
        else:
            classes += ' %s' % arg
        # Changes to the default widget
    if classes:
        attrs = bound_field.field.widget.attrs
        attrs['class'] = '%s%s' % (attrs.get('class', ''), classes)
    if 'placeholder' in kwargs:
        attrs['placeholder'] = kwargs['placeholder']
    #     if 'datepicker' in kwargs:
    #         attrs['data-datepicker'] = 'datepicker'
    # Changes to the bootstrap template
    inline = kwargs.get('inline', False)
    required = kwargs.get('required', False)
    return render_to_string("includes/bootstrap/field.html", {
        'field': bound_field,
        'inline': inline,
        'required': required
    })
    
    
#def get_page_list(parser, token):
#    """
#    Returns a list of pages suitable for displaying in the template.
#
#    :param:`token` expected in the form 'get_page_list page_number pages'
#
#    .. todo::
#        * catch token formatting errors
#        * allow 'get_page_list page_number pages as <variable_name>' syntax
#        * write tests
#    """
#    try:
#        tag_name, page_number, pages = token.split_contents()
#    except ValueError:
#        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
#    return PaginationNode(page_number, pages)
#
#class PaginationNode(template.Node):
#    """
#    Forms a page list which
#    * has a fixed number of cells (2*width + 1)
#    * always displays the first and last page with ...'s if needed
#    * centers on the current page as best possible
#    """
#    def __init__(self, page_number, pages):
#        self.width = 4
#        self.page_number = template.Variable(page_number)
#        self.pages = template.Variable(pages)
#    def render(self, context):
#        page_number = self.page_number.resolve(context)
#        pages = self.pages.resolve(context)
#        width = self.width
#        page_list = range(
#            max(1, page_number - width - max(width+page_number-pages,0)),
#            min(pages, page_number + width + max(width-page_number+1,0)) + 1
#        )
#        if page_list[0] != 1 and page_number > 2:
#            page_list[:1] = [1, '...']
#        if page_list[-1] != pages and page_number < pages-1:
#            page_list[-2:] = ['...', pages]
#        context['page_list'] = page_list
#        return ''
#
#register.tag('get_page_list', get_page_list)
