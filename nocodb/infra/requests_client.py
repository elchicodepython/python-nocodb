from typing import Optional
from ..nocodb import (
    NocoDBClient,
    NocoDBProject,
    AuthToken,
    WhereFilter,
)
from ..api import NocoDBAPI
from ..utils import get_query_params
from ..exceptions import NocoDBAPIError

import requests


class NocoDBRequestsClient(NocoDBClient):
    def __init__(self, auth_token: AuthToken, base_uri: str):
        self.__session = requests.Session()
        self.__session.headers.update(
            auth_token.get_header(),
        )
        self.__session.headers.update({"Content-Type": "application/json"})
        self.__api_info = NocoDBAPI(base_uri)

    def _request(self, method: str, url: str, *args, **kwargs):
        response = self.__session.request(method, url, *args, **kwargs)
        response_json = None
        try:
            response.raise_for_status()
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            ...
        except requests.exceptions.HTTPError as http_error:
            raise NocoDBAPIError(
                message=str(http_error),
                status_code=http_error.response.status_code,
                response_json=response_json,
                response_text=response.text
            )

        return response

    def table_row_list(
        self,
        project: NocoDBProject,
        table: str,
        filter_obj: Optional[WhereFilter] = None,
        params: Optional[dict] = None,
    ) -> dict:
        return self._request(
            "GET",
            self.__api_info.get_table_uri(project, table),
            params=get_query_params(filter_obj, params),
        ).json()

    def table_row_create(self, project: NocoDBProject, table: str, body: dict) -> dict:
        return self._request(
            "POST", self.__api_info.get_table_uri(project, table), json=body
        ).json()

    def table_row_detail(self, project: NocoDBProject, table: str, row_id: int) -> dict:
        return self._request(
            "GET",
            self.__api_info.get_row_detail_uri(project, table, row_id),
        ).json()

    def table_row_update(
        self, project: NocoDBProject, table: str, row_id: int, body: dict
    ) -> dict:
        return self._request(
            "PATCH",
            self.__api_info.get_row_detail_uri(project, table, row_id),
            json=body,
        ).json()

    def table_row_delete(self, project: NocoDBProject, table: str, row_id: int) -> int:
        return self._request(
            "DELETE",
            self.__api_info.get_row_detail_uri(project, table, row_id),
        ).json()

    def table_count(
        self,
        project: NocoDBProject,
        table: str,
        filter_obj: Optional[WhereFilter] = None,
    ) -> dict:
        return self._request(
            "GET",
            self.__api_info.get_table_count_uri(project, table),
            params=get_query_params(filter_obj),
        ).json()

    def table_find_one(
        self,
        project: NocoDBProject,
        table: str,
        filter_obj: Optional[WhereFilter] = None,
        params: Optional[dict] = None,
    ) -> dict:
        return self._request(
            "GET",
            self.__api_info.get_table_find_one_uri(project, table),
            params=get_query_params(filter_obj, params),
        ).json()

    def table_row_nested_relations_list(
        self,
        project: NocoDBProject,
        table: str,
        relation_type: str,
        row_id: int,
        column_name: str,
    ) -> dict:
        return self._request(
            "GET",
            self.__api_info.get_nested_relations_rows_list_uri(
                project, table, relation_type, row_id, column_name
            ),
        ).json()

    def project_create(self, body):
        return self._request(
            "POST", self.__api_info.get_project_uri(), json=body
        ).json()

    def table_create(
        self, project: NocoDBProject, body: dict
    ) -> dict:
        return self.__session.post(
            url=self.__api_info.get_project_tables_uri(project),
            json=body,
        ).json()

    def table_list(
        self,
        project: NocoDBProject,
        params: Optional[dict] = None,
    ) -> dict:
        return self.__session.get(
            url=self.__api_info.get_project_tables_uri(project),
            params=params,
        ).json()

    def table_read(
        self, tableId: str,
    ) -> dict:
        return self.__session.get(
            url=self.__api_info.get_table_meta_uri(tableId)
        ).json()

    def table_update(
        self, tableId: str, body: dict
    ):
        return self.__session.patch(
            url=self.__api_info.get_table_meta_uri(tableId),
            json=body,
        ).json()

    def table_delete(
        self, tableId: str,
    ) -> dict:
        return self.__session.delete(
            url=self.__api_info.get_table_meta_uri(tableId)
        ).json()

    def table_reorder(
        self, tableId: str, order: int
    ) -> dict:
        return self.__session.post(
            url=self.__api_info.get_table_meta_uri(tableId, "reorder"),
            json={ "order": order }
        ).json()
    
    def table_column_create(
        self, tableId: str, body: dict,
    ) -> dict:
        return self.__session.post(
            url=self.__api_info.get_table_meta_uri(tableId, "columns"),
            json=body,
        ).json()

    def table_column_update(
        self, columnId: str, body: dict,
    ) -> dict:
        return self.__session.patch(
            url=self.__api_info.get_column_uri(columnId),
            json=body,
        ).json()

    def table_column_delete(
        self, columnId: str,
    ) -> dict:
        return self.__session.delete(
            url=self.__api_info.get_column_uri(columnId)
        ).json()

    def table_column_set_primary(
        self, columnId: str,
    ) -> bool:
        return self.__session.post(
            url=self.__api_info.get_column_uri(columnId, "primary"),
        ).json()
