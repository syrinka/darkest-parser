from darkest_parser import parse, unparse

def test_string_literal():
    string = 'x: .data "value"'
    literal = 'x: .data value'

    dark1 = parse(string)
    dark1[0].set('data', 'value', 'literal')
    assert unparse(dark1) == literal

    dark2 = parse(literal)
    dark2[0].set('data', 'value', 'string')
    assert unparse(dark2) == string

def test_none_value():
    novalue = 'x: .data'
    hasvalue = 'x: .data "value"'

    dark1 = parse(novalue)
    dark1[0].set('data', 'value')
    assert unparse(dark1) == hasvalue

    dark2 = parse(hasvalue)
    dark2[0].set('data')
    assert unparse(dark2) == novalue
