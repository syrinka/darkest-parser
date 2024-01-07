from darkest_parser import parse

text = '''
item: .a 1 .b x .c "p" .d None
item: .a 1 .b x .c "q" .d "None"
item: .a 2 .b x .c "r" .d ""
item: .a 2 .b x .c "p" .d none
item: .a 3 .b y .c "q" .d
item: .a 3 .b y .c "r"
'''

dark = parse(text)

def test_cond1():
    assert len(dark.findall(a=1)) == 2
    assert len(dark.findall(b='x')) == 4
    assert len(dark.findall(c='p')) == 2

def test_cond2():
    assert len(dark.findall(a=2, b='y')) == 0
    assert len(dark.findall(b='x', c='r')) == 1

def test_cond3():
    assert len(dark.findall(a=3, b='x', c='q')) == 0
    assert len(dark.findall(a=3, b='y', c='r')) == 1

def test_none():
    assert len(dark.findall(d=None)) == 0