from typing import Optional
from ..nocodb import (
    JWTAuthToken,
    NocoDBClient,
    NocoDBProject,
    AuthToken,
    WhereFilter,
)
from ..api import NocoDBAPI
from ..utils import get_query_params

import requests


class NocoDBRequestsClient(NocoDBClient):
    def __init__(
        self,
        base_uri: str,
        auth_token: AuthToken = None,
        email: str = None,
        password: str = None,
    ):
        self.__session = requests.Session()
        self.__api_info = NocoDBAPI(base_uri)

        if not auth_token and not (email and password):
            raise ValueError("Either сredentials or token must be provided")

        if not auth_token and (email and password):
            auth_token = JWTAuthToken(self.get_auth_token(email, password))

        self.__session.headers.update(
                auth_token.get_header(),
            )
        self.__session.headers.update({"Content-Type": "application/json"})

    def get_auth_token(self, email: str, password: str) -> str:
        auth_token = self.__session.post(
            self.__api_info.get_auth_uri(),
            json=dict(email=email, password=password)
        ).json()['token']
        return auth_token

    def table_row_list(
        self,
        project: NocoDBProject,
        table: str,
        filter_obj: Optional[WhereFilter] = None,
        params: Optional[dict] = None,
    ) -> dict:

        response = self.__session.get(
            self.__api_info.get_table_uri(project, table),
            params=get_query_params(filter_obj, params),
        )
        return response.json()

    def table_row_create(
        self, project: NocoDBProject, table: str, body: dict
    ) -> dict:
        return self.__session.post(
            self.__api_info.get_table_uri(project, table), json=body
        ).json()

    def table_row_detail(
        self, project: NocoDBProject, table: str, row_id: int
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_row_detail_uri(project, table, row_id),
        ).json()

    def table_row_update(
        self, project: NocoDBProject, table: str, row_id: int, body: dict
    ) -> dict:
        return self.__session.patch(
            self.__api_info.get_row_detail_uri(project, table, row_id),
            json=body,
        ).json()

    def table_row_delete(
        self, project: NocoDBProject, table: str, row_id: int
    ) -> int:
        return self.__session.delete(
            self.__api_info.get_row_detail_uri(project, table, row_id),
        ).json()

    def table_row_nested_relations_list(
        self,
        project: NocoDBProject,
        table: str,
        relation_type: str,
        row_id: int,
        column_name: str,
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_nested_relations_rows_list_uri(
                project, table, relation_type, row_id, column_name
            )
        ).json()

    def project_create(
        self,
        body
    ):
        return self.__session.post(
            self.__api_info.get_project_uri(), json=body
        ).json()
