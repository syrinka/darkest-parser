# type: ignore
from darkest_parser import parse

text = '''
header: .title "darkest-parser"
data:
    .t true .f false
    .int 15 .float 17.28 .percent 55%
    .string "yes" .literal creature
    .list 1 2 3 4 5
select: .id marble
select: .id signal
select: .id hellix .mark a
alter: .data 1 3
stack: .data
'''

dark = parse(text)


def test_header():
    header = dark[0]
    assert header.title[0] == 'darkest-parser'


def test_data():
    data = dark.find('data')
    assert data.t == [True]
    assert data.f == [False]
    assert data.int == [15]
    assert data.float == [17.28]
    assert data.percent == [0.55]
    assert data.string == ['yes']
    assert data.literal == ['creature']
    assert data.list == [1, 2, 3, 4, 5]


def test_select():
    assert len(dark.findall('select')) == 3
    marked = dark.find(id='hellix')
    assert marked.mark[0] == 'a'


def test_alter():
    alter = dark.find('alter')
    assert alter.data == [1, 3]

    alter.data = ["36%"]
    assert alter.data == [.36]

    alter.data = [2, 6]
    assert alter.data == [2, 6]

    alter.data = [True, False]
    assert alter.data == [True, False]

    alter.set('data', [7, 9])
    assert alter.data == [7, 9]

    alter.data = [1, *alter.data, 3]
    assert alter.data == [1, 7, 9, 3]


def test_pop_n_set():
    stack = dark.find('stack')
    stack.pop('data')
    assert stack.has('data') == False
    stack.set('data')
    assert stack.has('data') and len(stack.data) == 0
    stack.pop('data')
    try:
        stack.pop('data')
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False