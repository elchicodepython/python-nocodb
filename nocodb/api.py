from enum import Enum
from urllib.parse import urljoin
from .nocodb import NocoDBProject


class NocoDBAPIUris(Enum):
    V1_DB_DATA_PREFIX = "api/v1/db/data/"
    V1_DB_META_PREFIX = "api/v1/db/meta/"


class NocoDBAPI:
    def __init__(self, base_uri: str):
        self.__base_data_uri = urljoin(base_uri + "/", NocoDBAPIUris.V1_DB_DATA_PREFIX.value)
        self.__base_meta_uri = urljoin(base_uri + "/", NocoDBAPIUris.V1_DB_META_PREFIX.value)

    def get_table_uri(self, project: NocoDBProject, table: str) -> str:
        return urljoin(self.__base_data_uri, "/".join(
            (
                project.org_name,
                project.project_name,
                table,
            )
        ))

    def get_table_count_uri(self, project: NocoDBProject, table: str) -> str:
        return "/".join(
            (
                self.get_table_uri(project, table),
                'count'
            )
        )

    def get_table_find_one_uri(self, project: NocoDBProject, table: str) -> str:
        return "/".join(
            (
                self.get_table_uri(project, table),
                'find-one'
            )
        )

    def get_row_detail_uri(
        self, project: NocoDBProject, table: str, row_id: int
    ):
        return urljoin(self.__base_data_uri, "/".join(
            (
                project.org_name,
                project.project_name,
                table,
                str(row_id),
            )
        ))

    def get_nested_relations_rows_list_uri(
        self,
        project: NocoDBProject,
        table: str,
        relation_type: str,
        row_id: int,
        column_name: str,
    ) -> str:
        return urljoin(self.__base_data_uri, "/".join(
            (
                project.org_name,
                project.project_name,
                table,
                str(row_id),
                relation_type,
                column_name,
            )
        ))

    def get_project_uri(
        self,
    ) -> str:
        return urljoin(self.__base_meta_uri, "projects")

    def get_project_tables_uri(
        self, project: NocoDBProject,
    ) -> str:
        return urljoin(self.__base_meta_uri, "/".join(
            (
                "projects",
                project.project_name,
                "tables"
            )
        ))
    
    def get_table_meta_uri(
        self, tableId: str, operation: str = None,
    ) -> str:
        additional_path = []
        if operation is not None:
            additional_path.append(operation)

        return urljoin(self.__base_meta_uri, "/".join(
            [
                "tables",
                tableId,
            ] + additional_path
        ))
    
    def get_column_uri(
        self, columnId: str, operation: str = None,
    ) -> str:
        additional_path = []
        if operation is not None:
            additional_path.append(operation)

        return urljoin(self.__base_meta_uri, "/".join(
            [
                "columns",
                columnId,
            ] + additional_path
        ))