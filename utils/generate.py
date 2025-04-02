import random
import re
import string

from slugify import slugify as slug_convert


def generate_random_string(length=128):
    """
    Generate a random string of a given length.

    Args:
        length (int): The length of the random string to generate. Defaults to 128.

    Returns:
        str: A randomly generated string of the specified length.

    Example:
        >>> generate_random_string(5)
        'aBcDe'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string

def generate_random_3(length=3):
    """
    Generate a random uppercase string of a given length.

    Args:
        length (int): The length of the random string to generate. Defaults to 3.

    Returns:
        str: A randomly generated uppercase string of the specified length.

    Example:
        >>> generate_random_3()
        'ABC'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string.upper()

def generate_account_id(length=22):
    """
    Generate a random account ID of a given length.

    Args:
        length (int): The length of the account ID to generate. Defaults to 22.

    Returns:
        str: A randomly generated account ID.

    Example:
        >>> generate_account_id()
        'A1B2C3D4E5F6G7H8I9J0KL'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string

def generate_chat_id(length=10):
    """
    Generate a random chat ID of a given length.

    Args:
        length (int): The length of the chat ID to generate. Defaults to 10.

    Returns:
        str: A randomly generated chat ID.

    Example:
        >>> generate_chat_id()
        '12345ABCDE'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string

def generate_number(length=6):
    """
    Generate a random numeric string of a given length.

    Args:
        length (int): The length of the numeric string to generate. Defaults to 6.

    Returns:
        str: A randomly generated numeric string.

    Example:
        >>> generate_number()
        '123456'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = string.digits
    return "".join(random.choice(letters) for _ in range(length))

def slugify(text):
    """
    Generate a slug from the input text, appending a random string for uniqueness.

    Args:
        text (str): The input text to slugify.

    Returns:
        str: A slugified string with a random suffix.

    Example:
        >>> slugify('Hello World')
        'hello-world-AbCd'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if not text:
        text = generate_account_id()
    text = slug_convert(text)
    random_string = "".join(random.choice(string.ascii_letters) for _ in range(4))
    slug = re.sub(r"[\W_]+", "-", text)
    return f"{slug}-{random_string}"

def slugify_title(text):
    """
    Generate a slug from the input text, prepending a random string for uniqueness.

    Args:
        text (str): The input text to slugify.

    Returns:
        str: A slugified string with a random prefix.

    Example:
        >>> slugify_title('Hello World')
        'AbC-hello-world'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    text = slug_convert(text=text)
    random_string = "".join(random.choice(string.ascii_letters) for _ in range(3))
    slug = re.sub(r"[\W_]+", "-", text)
    return f"{random_string}-{slug}"

def generate_api_key(length=60):
    """
    Generate a random API key with a given length, prefixed with 'sk-'.

    Args:
        length (int): The length of the API key to generate (excluding the prefix). Defaults to 60.

    Returns:
        str: A randomly generated API key.

    Example:
        >>> generate_api_key()
        'sk-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return "sk-" + random_string
