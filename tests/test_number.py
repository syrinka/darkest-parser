from darkest_parser.darkest import _is_number as isnum

def test_is_number():
    assert isnum("113")
    assert isnum("3.57")
    assert isnum("047")
    assert isnum("36%")
    assert not isnum("1234~")