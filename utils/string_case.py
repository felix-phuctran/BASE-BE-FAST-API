import json
import re
from collections.abc import Mapping

ACRONYM_RE = re.compile(r"([A-Z\d]+)(?=[A-Z\d]|$)")
PASCAL_RE = re.compile(r"([^\-_]+)")
SPLIT_RE = re.compile(r"([\-_]*[A-Z][^A-Z]*[\-_]*)")
UNDERSCORE_RE = re.compile(r"(?<=[^\-_])[\-_]+[^\-_]")


def to_snake_case(string: str) -> str:
    """
    Converts a string from camelCase or PascalCase into snake_case.

    Note:
        Uppercase letters are treated as word boundaries, which become underscores.

    Args:
        string (str): The input in camelCase or PascalCase format.

    Returns:
        str: The string converted to snake_case.

    Example:
        >>> to_snake_case("CamelCaseExample")
        'camel_case_example'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return "".join(["_" + i.lower() if i.isupper() else i for i in string]).lstrip("_")


def to_camel_case(snake_str: str) -> str:
    """
    Converts a string from snake_case into camelCase.

    Args:
        snake_str (str): The input in snake_case format.

    Returns:
        str: The string converted to camelCase.

    Example:
        >>> to_camel_case("snake_case_example")
        'snakeCaseExample'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def to_camel(string: str) -> str:
    """
    Converts a string from snake_case into CamelCase (a.k.a. PascalCase without a leading lowercase).

    Args:
        string (str): The input in snake_case format.

    Returns:
        str: The string converted to CamelCase.

    Example:
        >>> to_camel("snake_case_example")
        'SnakeCaseExample'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return "".join(word.capitalize() for word in string.split("_"))


def convert_filter_to_camel_case(filter="{}") -> str:
    """
    Despite the function name, it actually converts all JSON keys to snake_case.

    - Loads the given JSON string.
    - Converts **every key** to snake_case.
    - Returns a JSON string with updated keys.

    Args:
        filter (str): A JSON string. Keys may be in any format.

    Returns:
        str: A JSON string where all keys have been converted to snake_case.

    Example:
        >>> convert_filter_to_camel_case('{"snakeCaseKey": "value"}')
        '{"snake_case_key": "value"}'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    filter_json = json.loads(filter)

    if isinstance(filter_json, dict):
        filter_sk = _dict_to_snake_case(filter_json)
    else:
        filter_sk = [_dict_to_snake_case(fl) for fl in filter_json]
    return json.dumps(filter_sk)


def pascalize(str_or_iter):
    """
    Converts a string (or keys in a dict/list) to PascalCase.

    - If the input is a dict or list, applies the transformation recursively to the keys (and nested keys).
    - Otherwise, transforms a single string.

    Args:
        str_or_iter (str | list | dict): Input data to convert.

    Returns:
        str | list | dict: Data converted to PascalCase.

    Example:
        >>> pascalize("snake_case_example")
        'SnakeCaseExample'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if isinstance(str_or_iter, (list, Mapping)):
        return _process_keys(str_or_iter, pascalize)

    s = _is_none(str_or_iter)
    if s.isupper() or s.isnumeric():
        return str_or_iter

    def _replace_fn(match):
        return match.group(1)[0].upper() + match.group(1)[1:]

    s = camelize(PASCAL_RE.sub(_replace_fn, s))
    return s[0].upper() + s[1:] if s else s


def camelize(str_or_iter):
    """
    Converts a string (or keys in a dict/list) to camelCase.

    - If the input is a dict or list, applies the transformation recursively to the keys (and nested keys).
    - Otherwise, transforms a single string to camelCase.

    Args:
        str_or_iter (str | list | dict): Input data to convert.

    Returns:
        str | list | dict: Data converted to camelCase.

    Example:
        >>> camelize("snake_case_example")
        'snakeCaseExample'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if isinstance(str_or_iter, (list, Mapping)):
        return _process_keys(str_or_iter, camelize)

    s = _is_none(str_or_iter)
    if s.isupper() or s.isnumeric():
        return str_or_iter

    if len(s) != 0 and not s[:2].isupper():
        s = s[0].lower() + s[1:]

    return UNDERSCORE_RE.sub(lambda m: m.group(0)[-1].upper(), s)


def kebabize(str_or_iter):
    """
    Converts a string (or keys in a dict/list) to kebab-case.

    - If the input is a dict or list, applies the transformation recursively to the keys (and nested keys).
    - Otherwise, transforms a single string to kebab-case.

    Args:
        str_or_iter (str | list | dict): Input data to convert.

    Returns:
        str | list | dict: Data converted to kebab-case.

    Example:
        >>> kebabize("snake_case_example")
        'snake-case-example'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if isinstance(str_or_iter, (list, Mapping)):
        return _process_keys(str_or_iter, kebabize)

    s = _is_none(str_or_iter)
    if s.isnumeric():
        return str_or_iter

    if not s.isupper() and (is_camelcase(s) or is_pascalcase(s)):
        return _separate_words(string=_fix_abbreviations(s), separator="-").lower()

    return UNDERSCORE_RE.sub(lambda m: "-" + m.group(0)[-1], s)


def decamelize(str_or_iter):
    """
    Converts a string (or keys in a dict/list) to snake_case, usually from camelCase or PascalCase.

    - If the input is a dict or list, applies the transformation recursively to the keys (and nested keys).
    - Otherwise, transforms a single string.

    Args:
        str_or_iter (str | list | dict): Input data to convert.

    Returns:
        str | list | dict: Data converted to snake_case.

    Example:
        >>> decamelize("camelCaseExample")
        'camel_case_example'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if isinstance(str_or_iter, (list, Mapping)):
        return _process_keys(str_or_iter, decamelize)

    s = _is_none(str_or_iter)
    if s.isupper() or s.isnumeric():
        return str_or_iter

    return _separate_words(_fix_abbreviations(s)).lower()


def depascalize(str_or_iter):
    """
    Converts a string (or keys in a dict/list) from PascalCase to snake_case.

    Essentially a wrapper around decamelize.

    Args:
        str_or_iter (str | list | dict): Input data in PascalCase.

    Returns:
        str | list | dict: Data converted to snake_case.

    Example:
        >>> depascalize("PascalCaseExample")
        'pascal_case_example'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return decamelize(str_or_iter)


def dekebabize(str_or_iter):
    """
    Converts a string (or keys in a dict/list) from kebab-case to snake_case.

    - If the input is a dict or list, applies the transformation recursively to the keys (and nested keys).
    - Otherwise, replaces hyphens (“-”) with underscores (“_”).

    Args:
        str_or_iter (str | list | dict): Input data in kebab-case.

    Returns:
        str | list | dict: Data converted to snake_case.

    Example:
        >>> dekebabize("kebab-case-example")
        'kebab_case_example'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if isinstance(str_or_iter, (list, Mapping)):
        return _process_keys(str_or_iter, dekebabize)

    s = _is_none(str_or_iter)
    if s.isnumeric():
        return str_or_iter

    return s.replace("-", "_")


def is_camelcase(str_or_iter):
    """
    Checks if a string (or every key in a dict/list) is in camelCase format.

    Internally compares the input with the result of camelize().

    Args:
        str_or_iter (str | list | dict): The input to check.

    Returns:
        bool: True if it's strictly in camelCase, False otherwise.

    Example:
        >>> is_camelcase("camelCaseExample")
        True

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return str_or_iter == camelize(str_or_iter)


def is_pascalcase(str_or_iter):
    """
    Checks if a string (or every key in a dict/list) is in PascalCase format.

    Internally compares the input with the result of pascalize().

    Args:
        str_or_iter (str | list | dict]): The input to check.

    Returns:
        bool: True if it's strictly in PascalCase, False otherwise.

    Example:
        >>> is_pascalcase("PascalCaseExample")
        True

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return str_or_iter == pascalize(str_or_iter)


def is_kebabcase(str_or_iter):
    """
    Checks if a string (or every key in a dict/list) is in kebab-case format.

    Internally compares the input with the result of kebabize().

    Args:
        str_or_iter (str | list | dict): The input to check.

    Returns:
        bool: True if it's strictly in kebab-case, False otherwise.

    Example:
        >>> is_kebabcase("kebab-case-example")
        True

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return str_or_iter == kebabize(str_or_iter)


def is_snakecase(str_or_iter):
    """
    Checks if a string (or every key in a dict/list) is in snake_case format.

    Internally compares the input with the result of decamelize().

    Args:
        str_or_iter (str | list | dict): The input to check.

    Returns:
        bool: True if it's strictly in snake_case, False otherwise.

    Example:
        >>> is_snakecase("snake_case_example")
        True

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if is_kebabcase(str_or_iter) and not is_camelcase(str_or_iter):
        return False
    return str_or_iter == decamelize(str_or_iter)


def _is_none(_in):
    """
    Returns an empty string if input is None; otherwise, strips all whitespace.

    Args:
        _in (str): The input string (may be None).

    Returns:
        str: Whitespace-free string, or empty if None.

    Example:
        >>> _is_none("  hello world  ")
        'helloworld'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return "" if _in is None else re.sub(r"\s+", "", str(_in))


def _process_keys(str_or_iter, fn):
    """
    Recursively applies a conversion function to each key in a dict or each element of a list.

    - If the input is a list, applies `fn` or recursion to each element.
    - If the input is a dict, applies `fn` to each key and recursion to each value.

    Args:
        str_or_iter (str | list | dict): The data to process.
        fn (callable): The function used to convert each key or element.

    Returns:
        str | list | dict: The processed data.

    Example:
        >>> _process_keys({"snake_key": "value"}, to_camel_case)
        {'snakeKey': 'value'}

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if isinstance(str_or_iter, list):
        return [_process_keys(k, fn) for k in str_or_iter]
    if isinstance(str_or_iter, Mapping):
        return {fn(k): _process_keys(v, fn) for k, v in str_or_iter.items()}
    return str_or_iter


def _fix_abbreviations(string: str) -> str:
    """
    Adjusts uppercase acronyms so decamelization can split them more consistently.

    Args:
        string (str): The input string (may contain all-caps acronyms).

    Returns:
        str: A version of the string with acronyms partially cased to allow splitting.

    Example:
        >>> _fix_abbreviations("APIResponse")
        'ApiResponse'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return ACRONYM_RE.sub(lambda m: m.group(0).title(), string)


def _separate_words(string: str, separator="_") -> str:
    """
    Splits a string by uppercase “word boundaries” and rejoins using a chosen separator.

    Note:
        This function does not convert letters to lowercase; 
        uppercase letters remain uppercase in split segments.

        Example: 
            "camelCaseExample" => "camel_Case_Example" (NOT "camel_case_example").

    Args:
        string (str): The input string where uppercase letters indicate boundaries.
        separator (str): The separator used to join each chunk.

    Returns:
        str: The joined string with each chunk separated by `separator`.

    Example:
        >>> _separate_words("camelCaseExample")
        'camel_Case_Example'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return separator.join(s for s in SPLIT_RE.split(string) if s)


def _dict_to_snake_case(dict_: dict) -> dict:
    """
    Converts all keys in a dictionary to snake_case, preserving their values.

    Args:
        dict_ (dict): The input dictionary.

    Returns:
        dict: A new dictionary with all keys converted to snake_case.

    Example:
        >>> _dict_to_snake_case({"CamelCaseKey": "value"})
        {'camel_case_key': 'value'}

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return {to_snake_case(k): dict_[k] for k in dict_}


def singularize(noun):
    """
    Converts a plural noun into a naive singular form by trimming trailing “s” or “es”.

    Warning:
        This function does not handle irregular nouns well:
        e.g., "companies" -> "companie", "wolves" -> "wolve".

    Args:
        noun (str): The plural noun to convert.

    Returns:
        str: The simplified form of the noun, possibly incorrect for many irregulars.

    Example:
        >>> singularize("users")
        'user'
        >>> singularize("companies")
        'companie'
        >>> singularize("wolves")
        'wolve'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if noun.endswith("s") or noun.endswith("es"):
        singular_form = noun[:-1]

        if singular_form.endswith("i") and not singular_form.endswith("ei"):
            singular_form = singular_form[:-1] + "y"
        elif singular_form.endswith("ves"):
            # "wolves" => "wolve" => removing "s" first leads to "wolve"
            # Then we see 'ves' -> 'f' (but it's truncated incorrectly).
            singular_form = singular_form[:-3] + "f"
        elif singular_form.endswith("es"):
            singular_form = singular_form[:-2]
        elif singular_form.endswith("ss"):
            singular_form = noun  # e.g., "bosses" => "bosses"

        return singular_form

    return noun


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # --------------------------
    # 1) to_snake_case
    # --------------------------
    expected_1 = "camel_case_example"
    actual_1 = to_snake_case("CamelCaseExample")
    print(f"1) to_snake_case('CamelCaseExample')\n"
          f"   Expected: {expected_1}\n"
          f"   Actual:   {actual_1}\n")

    # --------------------------
    # 2) to_camel_case
    # --------------------------
    expected_2 = "snakeCaseExample"
    actual_2 = to_camel_case("snake_case_example")
    print(f"2) to_camel_case('snake_case_example')\n"
          f"   Expected: {expected_2}\n"
          f"   Actual:   {actual_2}\n")

    # --------------------------
    # 3) to_camel
    # --------------------------
    expected_3 = "SnakeCaseExample"
    actual_3 = to_camel("snake_case_example")
    print(f"3) to_camel('snake_case_example')\n"
          f"   Expected: {expected_3}\n"
          f"   Actual:   {actual_3}\n")

    # --------------------------
    # 4) convert_filter_to_camel_case
    # --------------------------
    # Thực ra hàm đang chuyển key về snake_case dù tên là "convert_filter_to_camel_case"
    expected_4 = '{"snake_case_key": "value"}'
    actual_4 = convert_filter_to_camel_case('{"snakeCaseKey": "value"}')
    print(f'4) convert_filter_to_camel_case(\'{{"snakeCaseKey": "value"}}\')\n'
          f"   Expected: {expected_4}\n"
          f"   Actual:   {actual_4}\n")

    # --------------------------
    # 5) pascalize
    # --------------------------
    expected_5 = "SnakeCaseExample"
    actual_5 = pascalize("snake_case_example")
    print(f"5) pascalize('snake_case_example')\n"
          f"   Expected: {expected_5}\n"
          f"   Actual:   {actual_5}\n")

    # --------------------------
    # 6) camelize
    # --------------------------
    expected_6 = "snakeCaseExample"
    actual_6 = camelize("snake_case_example")
    print(f"6) camelize('snake_case_example')\n"
          f"   Expected: {expected_6}\n"
          f"   Actual:   {actual_6}\n")

    # --------------------------
    # 7) kebabize
    # --------------------------
    expected_7 = "snake-case-example"
    actual_7 = kebabize("snake_case_example")
    print(f"7) kebabize('snake_case_example')\n"
          f"   Expected: {expected_7}\n"
          f"   Actual:   {actual_7}\n")

    # --------------------------
    # 8) decamelize
    # --------------------------
    expected_8 = "camel_case_example"
    actual_8 = decamelize("camelCaseExample")
    print(f"8) decamelize('camelCaseExample')\n"
          f"   Expected: {expected_8}\n"
          f"   Actual:   {actual_8}\n")

    # --------------------------
    # 9) depascalize
    # --------------------------
    expected_9 = "pascal_case_example"
    actual_9 = depascalize("PascalCaseExample")
    print(f"9) depascalize('PascalCaseExample')\n"
          f"   Expected: {expected_9}\n"
          f"   Actual:   {actual_9}\n")

    # --------------------------
    # 10) dekebabize
    # --------------------------
    expected_10 = "kebab_case_example"
    actual_10 = dekebabize("kebab-case-example")
    print(f"10) dekebabize('kebab-case-example')\n"
          f"    Expected: {expected_10}\n"
          f"    Actual:   {actual_10}\n")

    # --------------------------
    # 11) is_camelcase
    # --------------------------
    expected_11 = True
    actual_11 = is_camelcase("camelCaseExample")
    print(f"11) is_camelcase('camelCaseExample')\n"
          f"    Expected: {expected_11}\n"
          f"    Actual:   {actual_11}\n")

    # --------------------------
    # 12) is_pascalcase
    # --------------------------
    expected_12 = True
    actual_12 = is_pascalcase("PascalCaseExample")
    print(f"12) is_pascalcase('PascalCaseExample')\n"
          f"    Expected: {expected_12}\n"
          f"    Actual:   {actual_12}\n")

    # --------------------------
    # 13) is_kebabcase
    # --------------------------
    expected_13 = True
    actual_13 = is_kebabcase("kebab-case-example")
    print(f"13) is_kebabcase('kebab-case-example')\n"
          f"    Expected: {expected_13}\n"
          f"    Actual:   {actual_13}\n")

    # --------------------------
    # 14) is_snakecase
    # --------------------------
    expected_14 = True
    actual_14 = is_snakecase("snake_case_example")
    print(f"14) is_snakecase('snake_case_example')\n"
          f"    Expected: {expected_14}\n"
          f"    Actual:   {actual_14}\n")

    # --------------------------
    # 15) _is_none
    # --------------------------
    expected_15 = "helloworld"
    actual_15 = _is_none("  hello world  ")
    print(f"15) _is_none('  hello world  ')\n"
          f"    Expected: '{expected_15}'\n"
          f"    Actual:   '{actual_15}'\n")

    # --------------------------
    # 16) _fix_abbreviations
    # --------------------------
    expected_16 = "ApiResponse"
    actual_16 = _fix_abbreviations("APIResponse")
    print(f"16) _fix_abbreviations('APIResponse')\n"
          f"    Expected: {expected_16}\n"
          f"    Actual:   {actual_16}\n")

    # --------------------------
    # 17) _separate_words
    # --------------------------
    expected_17 = "camel_Case_Example"
    actual_17 = _separate_words("camelCaseExample")
    print(f"17) _separate_words('camelCaseExample')\n"
          f"    Expected: {expected_17}\n"
          f"    Actual:   {actual_17}\n")

    # --------------------------
    # 18) _dict_to_snake_case
    # --------------------------
    expected_18 = {"camel_case_key": "value"}
    actual_18 = _dict_to_snake_case({"CamelCaseKey": "value"})
    print(f"18) _dict_to_snake_case({{'CamelCaseKey': 'value'}})\n"
          f"    Expected: {expected_18}\n"
          f"    Actual:   {actual_18}\n")

    # --------------------------
    # 19) singularize('companies')
    # --------------------------
    expected_19 = "companie"  # Vì hàm chưa xử lý irregular "companies" đúng (company)
    actual_19 = singularize("companies")
    print(f"19) singularize('companies')\n"
          f"    Expected: {expected_19}\n"
          f"    Actual:   {actual_19}\n")

    # --------------------------
    # 20) singularize('wolves')
    # --------------------------
    expected_20 = "wolve"  # Thay vì "wolf"
    actual_20 = singularize("wolves")
    print(f"20) singularize('wolves')\n"
          f"    Expected: {expected_20}\n"
          f"    Actual:   {actual_20}\n")

    # --------------------------
    # 21) singularize('users')
    # --------------------------
    expected_21 = "user"
    actual_21 = singularize("users")
    print(f"21) singularize('users')\n"
          f"    Expected: {expected_21}\n"
          f"    Actual:   {actual_21}\n")

