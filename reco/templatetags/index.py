from django import template

register = template.Library()
import ipdb
@register.filter
def get_at_index(list, index):
    #ipdb.set_trace()
    return str(list[index])

@register.filter
def get_at_index_dict(mydict, index):
    #ipdb.set_trace()
    dictlist =[]
    for key, value in mydict.iteritems():
        temp = [value]
        dictlist = dictlist + temp
    return (dictlist[index])
