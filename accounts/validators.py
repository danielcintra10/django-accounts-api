import re
from django.core.exceptions import ValidationError


def validate_mobile_phone(phone_number):
    if not re.match(r'\+\d{1,3} \d{8,15}', phone_number):
        raise ValidationError(f"El número de teléfono movil debe poseer el formato +123 4567890000, "
                              f"número introducido por usted {phone_number}")
    if re.findall(r'[^0-9 +]', phone_number):
        raise ValidationError(f"Los números telefónicos solo pueden contener caracteres numéricos 0-9 "
                              f"y el caracter especial +, número telefónico introducido por usted {phone_number}")


def validate_name(name):
    if re.findall(r'[^a-z-A-Z ÁÉÍÓÚáéíóúÑñ]', name):
        raise ValidationError(f"{name}, Los nombres propios, apellidos, nombres de ciudades o países "
                              f"solo deben contener letras")
