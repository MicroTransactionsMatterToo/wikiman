"""
Provides an abstracted form of various structures in their Groff form
"""

from typing import List, Dict, Union
from abc import ABCMeta, abstractclassmethod, abstractproperty, abstractmethod
from enum import Enum, Flag, auto, _decompose
from textwrap import dedent
from itertools import chain





class HeaderLevels(Enum):
    """
    Set of usable header types within Groff using MS macros
    """
    HEADER_LARGE = '.SH 1'
    HEADER_MEDIUM = '.SH 2'
    HEADER_SMALL = '.SH 3'
    HEADER_CUSTOM = '.SH {size}'
    NUMBERED_HEADER = '.NH {size} {section}'


class GroffColumnSpecifiers(Flag):
    """
    Flags for easy combinations of Unix tbl column specifiers. To combine flags, just OR them together. Flags that cannot be combined
    will return the first viable combination of the components. See source for more details
    """
    RELATIVE_CENTER = auto()
    CENTER = auto()
    LEFT_ALIGNED = auto()
    RIGHT_ALIGNED = auto()
    NUMBER_ALIGNED = auto()
    VERTICAL_SPAN = auto()
    HORIZONTAL_SPAN = auto()

    _uncombinable = (RELATIVE_CENTER | CENTER | LEFT_ALIGNED | RIGHT_ALIGNED)

    def __or__(self, other) -> Flag:
        if not isinstance(other, self.__class__):
            return NotImplemented
        self_components = _decompose(self.__class__, self._value_)[0]
        other_components = _decompose(self.__class__, other._value_)[0]
        self_primary = list(filter(lambda x: x in self._uncombinable, self_components))[:1][0]
        other_combinable = list(filter(lambda x: x not in self._uncombinable, other_components))
        usable_output = self_primary
        for val in other_combinable:
            usable_output = Flag.__or__(usable_output, val)
        usable_output._name_ = None if len(other_combinable) > 0 else usable_output._name_
        return usable_output


class GroffColumnOptions(Flag):
    """
    Flags for options in table columns which affect presentation of column content
    """
    BOLD = auto()
    ITALIC = auto()
    VERTICAL_SPAN_START_BOTTOM = auto()
    VERTICAL_SPAN_START_TOP = auto()
    UP_HALF_LINE = auto()
    EXPAND_COLUMN = auto()
    IGNORE_COLUMN = auto()


class GroffTextEntity(metaclass=ABCMeta):
    """
    An abstract class representing any solid concept or entity present in Groff when used with the MS macro set
    """

    @abstractmethod
    def __str__(self) -> str:
        """
        Should return a fully usable version of the entity

        Returns:
            str: Usable textual version of entity
        """
        pass


class GroffText(GroffTextEntity):
    def __init__(self, text):
        self.raw_text = text

    def __str__(self):
        return self.raw_text


class GroffColouredText(GroffTextEntity):
    def __init__(self, colour: str, text: str):
        super().__init__()
        self.colour = colour
        self.raw_text = text

    def __str__(self) -> str:
        return "\m[{self.colour}]{self.raw_text}\m[]".format(self=self)


_GroffTableContent = List[Union[List[Union[GroffText, GroffColouredText]],Union[GroffText, GroffColouredText]]]

class GroffTableRow(GroffTextEntity):
    def __init__(self, content: _GroffTableContent = None):
        pass

    def __getitem__(self):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass


class GroffColumnSection(GroffTextEntity):
    """
    Contains any number of :class:`GroffTableRow`'s along with column options
    """

    def __init__(self, options: object = None):
        super().__init__()
        if options is not None:
            self.options = options
        else:
            self.options = {
                "center": False,
                "expand": False,
                "box": False,
                "allbox": False,
                "doublebox": False,
                "tab": "^",
                "linesize": None,
                "delim": None
            }

    def __str__(self):
        pass

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def add_row(self):
        pass

    def remove_row(self):
        pass

    def add_column(self):
        pass

    def remove_column(self):
        pass


class GroffTable(GroffTextEntity):
    """
    A container that forms a complete Groff table.
    The structure is such that rows are contained by their respective column configurations
    """

    def __str__(self):
        pass

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def add_section(self, column: GroffColumnSection):
        pass


class GroffLinebreak(GroffTextEntity):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return ".br\n"


class GroffParagraph(GroffTextEntity):
    """
    A paragraph in Groff, consisting of any other Groff entities preceded by the macro :code:`.LP`. Content given can
    either be a list of GroffTextEntities or a string. Objects that can be converted to strings can also be used, but
    they may produce problematic results

    Args:
        content (:obj:`list` of :class:`GroffTextEntity` or :obj:`str`): Content of the paragraph
    """
    def __init__(self, content: Union[List[GroffTextEntity], str]):
        super().__init__()
        self.raw_content = content

    def __str__(self) -> str:
        if type(self.raw_content) is str:
            return dedent("""\
            .LP
            {content}
            """.format(content=self.raw_content))
        elif type(self.raw_content) is list:
            rval = ""
            try:
                for item in self.raw_content:
                    rval += str(item)
            except AttributeError as exc:
                raise NotImplementedError(
                    "Groff paragraph contained item without any string methods implemented"
                ) from exc


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

    def __init__(self, header_text: str, header_level: HeaderLevels, header_options: Dict = None):
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

    def __str__(self) -> str:
        return dedent("""\
        {header_line}
        {raw_text}
        """.format(header_line=self._header_decl, raw_text=self.raw_text))
