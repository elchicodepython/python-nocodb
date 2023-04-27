from typing import List
from ..nocodb import WhereFilter


class Or(WhereFilter):
    def __init__(self, *filters: List[WhereFilter]):
        self.__filters = filters

    def get_where(self) -> str:
        return (
            "("
            + "~or".join([filter.get_where() for filter in self.__filters])
            + ")"
        )


class And(WhereFilter):
    def __init__(self, *filters: List[WhereFilter]):
        self.__filters = filters

    def get_where(self) -> str:
        return (
            "("
            + "~and".join([filter.get_where() for filter in self.__filters])
            + ")"
        )


class Not(WhereFilter):
    def __init__(self, filter: WhereFilter):
        self.__filter = filter

    def get_where(self) -> str:
        return "~not" + self.__filter.get_where()
