from __future__ import annotations
from typing import Any, Literal, Generator

from lark import Lark, Tree, Token
from lark.reconstruct import Reconstructor

LEX_RULE = r'''
darkest: element*
element: tag ":" params EOL+
params: param (" " param)*
param: "." key value

tag: LITERAL
key: LITERAL
value: (NUMBER | BOOL | LITERAL | STRING)*

NUMBER: /[+-]?/ (/\d+\.\d+/ | /\d+/) /%?/
BOOL: "true"i | "false"i
LITERAL: /[\w\-\~\@]+/
STRING: "\"" (LITERAL | " ")* "\""

EOL: "\n"
IGNORE: " " | "\n"
COMMENT: "//" LITERAL
%ignore IGNORE
%ignore COMMENT
'''

LEX = Lark(LEX_RULE, start='darkest', maybe_placeholders=False)


def _postproc(items):
    #(HACK) reconstruct post proc
    # so messy, but it just works
    flag = 0
    for i in items:
        if (type(i) == str):
            yield i
            if i == ':':
                yield ' '
        else:
            yield i
            if (flag == 0):
                flag = 1
            else:
                if (i.type != 'EOL'):
                    yield ' '
                else:
                    flag = 0


def _is_number(text: str):
    try:
        float(text.rstrip('%'))
    except ValueError:
        return False
    return True


class Darkest(object):
    tree: Tree[Token]
    def __init__(self, tree: Tree) -> None:
        self.tree = tree


    def elements(self):
        for i in self.tree.children:
            yield Element(i) # type: ignore


    def finditer(self, tag: str | None = None, **conds) -> Generator[Element, Any, Any]:
        """
        eg. `findall('combat_skill', type='ranged')`
        """
        for element in self.elements():
            if tag is not None and element.tag != tag:
                continue
            for key in conds:
                try:
                    v1 = conds[key]
                    attr = getattr(element, key)
                    if len(attr) == 0:
                        break
                    v2 = attr[0]
                    if isinstance(v2, str):
                        # for more convenient string compare
                        v2 = v2.strip('"')
                    if v1 != v2:
                        break
                except KeyError:
                    break
            else:
                yield element


    def findall(self, tag: str | None = None, **conds) -> list[Element]:
        return list(self.finditer(tag, **conds))


    def find(self, tag: str | None = None, **conds) -> Element:
        """
        eg. `find('combat_skill', id='transform', level=1)`
        """
        try:
            return next(self.finditer(tag, **conds))
        except StopIteration:
            raise KeyError


    def pretty(self, indent_str='  ') -> str:
        return self.tree.pretty(indent_str)


    def __getitem__(self, index):
        return Element(self.tree.children[index])


class Element(object):
    tree: Tree[Token]
    def __init__(self, tree: Tree[Token]) -> None:
        self.tree = tree

    @property
    def tag(self) -> str:
        return self.tree.children[0].children[0].value # type: ignore

    @property
    def params(self) -> list[Tree[Token]]:
        return self.tree.children[1].children # type: ignore


    def keys(self) -> list[str]:
        return [param.children[0].children[0].value for param in self.params] # type: ignore


    def _getraw(self, key: str) -> list[Token]:
        try:
            return next(param.children[1].children for param in self.params if param.children[0].children[0].value == key) # type: ignore
        except StopIteration:
            raise KeyError


    def get(self, key: str) -> list[Any]:
        li = []
        for i in self._getraw(key):
            if i.type == 'NUMBER':
                li.append(float(i) if i[-1] != '%' else float(i[:-1])/100)
            elif i.type == 'BOOL':
                li.append(True if i.lower() == 'true' else False)
            else:
                li.append(i.strip('"'))
        return li


    def set(self, key: str, value: list[Any] | Any | None = None, type: Literal['number', 'bool', 'string', 'literal'] | None = None):
        if not isinstance(value, list):
            value = [value]
        if value[0] is not None and type is None:
            if isinstance(value[0], (int, float)) or _is_number(value[0]):
                type = 'number'
            elif isinstance(value[0], bool):
                type = 'bool'
            else:
                type = 'string'

        value = [] if value[0] is None else [
            Token(type.upper(), '"%s"'%i) if type == 'string' else Token(type.upper(), i) for i in value # type: ignore
        ]

        if not self.has(key):
            tree = Tree('param', [
                Tree('key', [
                    Token('LITERAL', key)
                ]),
                Tree('value', value)
            ])
            self.params.append(tree)
        else:
            self._getraw(key)[:] = value


    def pop(self, key: str) -> list[Token]:
        try:
            param = next(param for param in self.params if param.children[0].children[0].value == key) # type: ignore
        except StopIteration:
            raise KeyError
        self.params.remove(param)
        return param.children[1].children # type: ignore


    def has(self, key: str) -> bool:
        return key in self.keys()


    def __getattr__(self, key: str) -> Any:
        return self.get(key)


    def __setattr__(self, key: str, value: Any):
        if key != 'tree':
            self.set(key, value)
        else:
            super().__setattr__(key, value)


def parse(text: str) -> Darkest:
    return Darkest(LEX.parse(text.replace('\t', ' ') + '\n')) # +'\n' to make sure there's always a EOL


def unparse(inst: Darkest) -> str:
    return Reconstructor(LEX).reconstruct(inst.tree, postproc=_postproc).strip()
