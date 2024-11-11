def int_to_roman(integer_number: int) -> str:
    roman_numerals = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]

    result = []

    for value, numeral in roman_numerals:
        while integer_number >= value:
            result.append(numeral)
            integer_number -= value

    return ''.join(result)