"""
Provides an abstracted form of various structures in their Groff form
"""

from typing import List, Dict, Union
from abc import ABCMeta, abstractclassmethod, abstractproperty, abstractmethod
from enum import Enum
from textwrap import dedent


# == Typing stuff == #
class HeaderLevels(Enum):
    HEADER_LARGE = '.SH 1'
    HEADER_MEDIUM = '.SH 2'
    HEADER_SMALL = '.SH 3'
    HEADER_CUSTOM = '.SH {size}'
    NUMBERED_HEADER = '.NH {size} {section}'


class GroffTextEntity(metaclass=ABCMeta):
    @property
    @abstractmethod
    def text(self) -> str:
        pass


class GroffTable:
    def __init__(self):
        pass

    def __str__(self):
        pass

    def add_row(self, content: List[List]):
        pass

    def add_column(self, title: Union[str, None] = None, width: str = None):
        pass

    @property
    def text(self) -> str:
        pass


class GroffLinebreak:
    def __init__(self):
        pass

    def __str__(self) -> str:
        return ".br\n"

    @property
    def text(self) -> str:
        return str(self)


class GroffParagraph:
    def __init__(self, content: Union[List[GroffTextEntity], str]):
        pass

    @property
    def text(self) -> str:
        pass


class GroffColouredText(GroffTextEntity):
    def __init__(self, colour: str, text: str):
        super().__init__()
        self.colour = colour
        self.raw_text = text

    @property
    def text(self) -> str:
        return "\\m[{self.colour}]{self.raw_text}\\m[]".format(self=self)

class GroffHeader(GroffTextEntity):
    """
    Represents a Groff MS-macro header. The header can be any one of the values in :class:`HeaderLevels`
    For both :code:`HeaderLevels.HEADER_CUSTOM` amd :code:`HeaderLevels.NUMBERED_HEADER`,
    additional options can be supplied

    These options are as follows::

        {
            "size": int, # The size of the header. The font gets smaller as this increases
            "section": str # For HeaderLevels.NUMBERED_HEADER only, provides explicit numbering of sections
        }

    Args:
        header_text (str): The actual text of the header. This should NOT contain any macros, as they will not display correctly
        header_level (HeaderLevels): The level/type of the header
        header_options (:obj:`dict`, optional): Additional options for
            :class:`HeaderLevels.HEADER_CUSTOM` and :class:`HeaderLevels.NUMBERED_HEADER`
    """
    def __init__(self, header_text: str, header_level: HeaderLevels, header_options: Union[Dict, None] = None):
        super().__init__()
        if header_options is None:
            header_options = {}
        self.raw_text = header_text
        if header_level is HeaderLevels.HEADER_CUSTOM:
            self._header_decl = header_level.value.format(size=header_options.get("size") or "\b")
        elif header_level is HeaderLevels.NUMBERED_HEADER:
            self._header_decl = header_level.value.format(size=header_options.get("size") or "\b",
                                                          section=header_options.get("section") or "\b")
        else:
            self._header_decl = header_level.value

    @property
    def text(self) -> str:
        return dedent("""\
        {header_line}
        {raw_text}
        """.format(header_line=self._header_decl, raw_text=self.raw_text))


