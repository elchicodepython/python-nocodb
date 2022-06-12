from .nocodb import WhereFilter


class InFilter(WhereFilter):
    def __init__(self, column_name: str, value: str):
        self.__column_name = column_name
        self.__value = value

    def get_where(self) -> str:
        return f"({self.__column_name},like,%{self.__value}%)"


class EqFilter(WhereFilter):
    def __init__(self, column_name: str, value: str):
        self.__column_name = column_name
        self.__value = value

    def get_where(self) -> str:
        return f"({self.__column_name},eq,{self.__value})"
