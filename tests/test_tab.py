from darkest_parser import parse

text = '''
inventory_system_config:	.type "raid"						.max_slots 16				.use_stack_limits true
'''

def test_tab():
    try:
        dark = parse(text)
    except Exception:
        assert False

    assert dark[0].type == ['raid']
    assert dark[0].max_slots == [16]
    assert dark[0].use_stack_limits == [True]