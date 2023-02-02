from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/categories.html')
#the get_category_list method returns a dictionary with one key/value pairing.
#categories represents a list of all the Category objects present in the DB.
#in the register.inclusion_tag we refer to rango/categories.html. This template
#is used by the Django template engine to render the list of categories we provide in 
#the dictionary that is returned to the function. The rendered list can be 
#injected into the response of the view that initially called the template tag.
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
    'current_category': current_category}

    #note the current_category parameter for get_category_list(). We use parameterisation to
    # highlight which category we are looking at when visiting its page. If a parameter isn't
    #passed, None is used instead (implying there is no currently selected category)
