from django.template import Library

register = Library()

@register.filter(name='get_before')
def get_before(value, arg):
    arg = int(arg)
    l_lim = arg - 5
    if l_lim < 1:
        l_lim = 1
    return range(l_lim, arg)

@register.filter(name='get_after')
def get_after(value, arg):
    arg = int(arg)
    r_lim = arg + 5
    if r_lim > len(value):
        r_lim = len(value)+1
    return range(arg+1, r_lim)  