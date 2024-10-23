from django import template

register = template.Library()

# Este es un filtro de plantilla personalizado que se encarga de agregar una clase a un campo de formulario
@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class":css})

# Este es un filtro de plantilla personalizado que se encarga de obtener un valor de un diccionario
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)