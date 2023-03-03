from ..nocodb import WhereFilter


class RawFilter(WhereFilter):
    def __init__(self, raw: str):
        self.__raw = raw

    def get_where(self) -> str:
        return self.__raw


class RawTemplateFilter(WhereFilter):
    def __init__(self, template: str, *args, **kwargs):
        self.__template = template
        self.__template_values = args
        self.__template_kvalues = kwargs

    def get_where(self) -> str:
        return self.__template.format(*self.__template_values, **self.__template_kvalues)
