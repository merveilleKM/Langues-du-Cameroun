from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key, 0)  # Retourne 0 si la clé n'existe pas
    print(f"Récupération pour clé {key} : {value}")
    return value
    

@register.filter
def int_range(value):
    try:
        print(f"int_range reçu : {value}")
        return range(int(value))
    except (ValueError, TypeError):
        print("Erreur dans int_range, retour à 0")
        return range(0)


@register.filter
def sub(value, arg):
    """Soustrait arg de value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0
