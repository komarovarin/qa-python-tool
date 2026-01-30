import random
import string

from weasyprint.css.computed_values import length


def generate_random_number_str(length):
    result = ''
    for i in range(0, length):
        result += str(random.randint(0,9))
    return result

def generate_random_letter_str(length):
    result = ''
    for i in range(0, length):
        result += str(random.choice(string.ascii_letters[random.randint(0,5)]))
    return result

def generate_random_phone_number(length):
    result = ''
    for i in range(0, length):
        result += str(random.randint(0,9))
    return result