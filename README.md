# darkest-parser

**darkest-parser** is a module to parser `.darkest` file originally from [Darkest Dungeon](https://www.darkestdungeon.com/) programatically.

## Usage

```sh
pip install darkest-parser
```

```python
from darkest_parser import parse, unparse

text = '''
resistances: .stun 40% .poison 40% .bleed 40% .disease 30% .move 40% .debuff 30% .death_blow 67% .trap 40%
weapon: .name "houndmaster_weapon_0" .atk 0% .dmg 4 7 .crit 4% .spd 5
armour: .name "houndmaster_armour_0" .def 10% .prot 0 .hp 21 .spd 0
combat_skill: .id "hounds_rush" .level 0 .type "ranged" .atk 85% .dmg 0% .crit 5% .launch 432 .target 1234 .effect "Beast Killer 1"
combat_skill: .id "hounds_rush" .level 1 .type "ranged" .atk 90% .dmg 0% .crit 6% .launch 432 .target 1234 .effect "Beast Killer 2"
'''

dark = parse(text)

dark[0].tag == 'resistances'
dark[0].set('stun', '60%')
dark[0].poison = '40%'


weapon0 = dark.find('weapon', name='houndmaster_weapon_0')
weapon0.tag == 'weapon'
weapon0.dmg = [14, 17]
weapon0.spd = 25

for rush in dark.finditer('combat_skill', id='hounds_rush'):
    rush.type = 'meele'
    rush.set('ignore_guarded')

rush0 = dark.find(id='hounds_rush', level=0)
# x invalid:
# rush0.effect.append('Human Killer 1')
# √ use instead:
rush0.effect = [*rush0.effect, 'Human Killer 1']

rush1 = dark.find(id='hounds_rush', level=1)
rush1.has('target') == True
rush1.set('target', '~1234', 'literal')
# literal means that the value is unquoted, it's useful in some case,
# for example: launch, target, valid_modes, etc.

print(unparse(dark))
```

## API Reference

```python
def parse(str) -> Darkest:
    ...
def unparse(Darkest) -> str:
    ...

class Darkest:
    def __getitem__(int) -> Element:
        ...
    def finditer(str | None, **{str: Any}) -> Generator[Element, Any, Any]:
        ...
    def findall(str | None, **{str: Any}) -> List[Element]:
        ...
    def find(str | None, **{str: Any}) -> Element:
        ...

class Element:
    def get(str) -> List[Any]:
        ...
    def set(str, Any | List[Any] | None, Literal['number', 'bool', 'string', 'literal'] | None):
        ...
    def pop(str):
        ...
    def has(str) -> bool:
        ...
```