from enum import Enum


class BorderType(Enum):
    IGNORE = "ignore"
    REPEAT = "repeat"
    REFLECT = "reflect"


class BorderTreatment:
    def ignore(self):
        """That is to copy the borders pixels as to the enhanced matrix"""
        ...

    def repeat(self):
        """Consider as if the images continue the last row /column without changes"""
        ...

    def reflect(self):
        """Mirror The row/column across boarder"""
        ...
