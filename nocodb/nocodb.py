from abc import ABC, abstractmethod
from typing import Optional

"""
License MIT

Copyright 2022 Samuel López Saura

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class AuthToken(ABC):
    @abstractmethod
    def get_header(self) -> dict:
        pass


class APIToken:
    def __init__(self, token: str):
        self.__token = token

    def get_header(self) -> dict:
        return {"xc-token": self.__token}


class JWTAuthToken:
    def __init__(self, token: str):
        self.__token = token

    def get_header(self) -> dict:
        return {"xc-auth": self.__token}


class WhereFilter(ABC):
    @abstractmethod
    def get_where(self) -> str:
        pass


"""This could be great but actually I don't know how to join filters in the
NocoDB DSL. I event don't know if this is possible through the current API.
I hope they add docs about it soon.

class NocoDBWhere:

    def __init__(self):
        self.__filter_array: List[WhereFilter] = []

    def add_filter(self, where_filter: WhereFilter) -> NocoDBWhere:
        self.__filter_array.append(
                where_filter
        )
        return self

    def get_where(self) -> str:
        return '&'.join([filter_.get_where() for filter_ in self.__filter_array])

    def __str__(self):
        return f'Where: "{self.get_where()}"'
"""


class NocoDBProject:
    def __init__(self, org_name: str, project_name: str):
        self.project_name = project_name
        self.org_name = org_name


class NocoDBClient:
    @abstractmethod
    def table_row_list(
        self, project: NocoDBProject, table: str, filter_obj=None, params=None
    ) -> dict:
        pass

    @abstractmethod
    def table_row_list(
        self,
        project: NocoDBProject,
        table: str,
        filter_obj: Optional[WhereFilter] = None,
        params: Optional[dict] = None,
    ) -> dict:
        pass

    @abstractmethod
    def table_row_create(
        self, project: NocoDBProject, table: str, body: dict
    ) -> dict:
        pass

    @abstractmethod
    def table_row_detail(
        self, project: NocoDBProject, table: str, row_id: int
    ) -> dict:
        pass

    @abstractmethod
    def table_row_update(
        self, project: NocoDBProject, table: str, row_id: int, body: dict
    ) -> dict:
        pass

    @abstractmethod
    def table_row_delete(
        self, project: NocoDBProject, table: str, row_id: int
    ) -> int:
        pass

    @abstractmethod
    def table_row_nested_relations_list(
        self,
        project: NocoDBProject,
        table: str,
        relation_type: str,
        row_id: int,
        column_name: str,
    ) -> dict:
        pass

    @abstractmethod
    def table_create(
        self, project: NocoDBProject, body: dict
    ) -> dict:
        pass

    @abstractmethod
    def table_list(
        self,
        project: NocoDBProject,
        params: Optional[dict] = None,
    ) -> dict:
        pass

    @abstractmethod
    def table_read(
        self, tableId: str,
    ) -> dict:
        pass

    @abstractmethod
    def table_update(
        self, tableId: str, body: dict,
    ) -> bool:
        pass

    @abstractmethod
    def table_delete(
        self, tableId: str,
    ) -> dict:
        pass

    @abstractmethod
    def table_reorder(
        self, tableId: str, order: int,
    ) -> dict:
        pass

    @abstractmethod
    def table_column_create(
        self, tableId: str, body: dict,
    ) -> dict:
        pass

    @abstractmethod
    def table_column_update(
        self, columnId: str, body: dict,
    ) -> dict:
        pass

    @abstractmethod
    def table_column_delete(
        self, columnId: str,
    ) -> dict:
        pass

    @abstractmethod
    def table_column_set_primary(
        self, columnId: str,
    ) -> dict:
        pass
