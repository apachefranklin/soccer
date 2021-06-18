from django.template.defaulttags import register

@register.filter(name="keyvalue")
def keyvalue(dictionary, key):
    return dictionary.get(key)
