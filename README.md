# NocoDB Python Client

NocoDB is a great Airtable alternative. This client allows python developers
to use NocoDB API in a simple way.

## Usage

### Client configuration
```python
from nocodb.nocodb import NocoDBProject, APIToken, JWTAuthToken
from nocodb.filters import InFilter, EqFilter
from nocodb.infra.requests_client import NocoDBRequestsClient


# Usage with API Token
client = NocoDBRequestsClient(
        # Your API Token retrieved from NocoDB conf
        APIToken("YOUR-API-TOKEN"),
        # Your nocodb root path
        "http://localhost:8080"
)

# Usage with JWT Token
client = NocoDBRequestsClient(
        # Your API Token retrieved from NocoDB conf
        JWTAuthToken("your.jwt.token"),
        # Your nocodb root path
        "http://localhost:8080"
)
```

### Project creation
```python
# Example with default database
project_body = {"title": "My new project"}

# Example with Postgresql
project_body = {
    "title": "MyProject",
    "bases": [
        {
            "type": "pg",
            "config": {
                "client": "pg",
                "connection": {
                    "host": "localhost",
                    "port": "5432",
                    "user": "postgres",
                    "password": "postgres",
                    "database": "postgres"
                },
                "searchPath": [
                    "public"
                ]
            },
            "inflection_column": "camelize",
            "inflection_table": "camelize"
        }
    ],
    "external": True
}

project = client.project_create(body=project_body)
```

### Project selection
```python
# Be very carefull with org, project_name and table names
# weird errors from nocodb can arrive if they are wrong
# example: id is not defined...
# probably they will fix that in a future release.
project = NocoDBProject(
        "noco", # org name. noco by default
        "myproject" # project name. Case sensitive!!
)

```

### Table rows operations
```python
table_name = "tablename"

# Retrieve a page of rows from a table
table_rows = client.table_row_list(project, table_name)

# Retrieve the first 10000 rows
table_rows = client.table_row_list(project, table_name, params={'limit': 10000})

# Skip 100 rows
table_rows = client.table_row_list(project, table_name, params={'offset': 100})

# Filter the query
# Currently only one filter at a time is allowed. I don't know how to join
# multiple conditions in nocodb dsl. If you know how please let me know :).
table_rows = client.table_row_list(project, table_name, InFilter("name", "sam"))
table_rows = client.table_row_list(project, table_name, filter_obj=EqFilter("Id", 100))

# Retrieve a single row
row_id = 10
row = client.table_row_detail(project, table_name, row_id)

# Create a new row
row_info = {
    "name": "my thoughts",
    "content": "i'm going to buy samuel a beer because i love this module",
    "mood": ":)"
}
client.table_row_create(project, table_name, row_info)

# Update a row
row_id = 2
row_info = {
    "content": "i'm going to buy samuel a new car because i love this module",
}
client.table_row_update(project, table_name, row_id, row_info)

# Delete a row (only if you've already bought me a beer)
client.table_row_delete(project, table_name, row_id)
```

## Author notes

I created this package to bootstrap some personal projects and I hope it
will help other developers from the python community. It's not completed but
it has what I needed: A full CRUD with some filters.

Feel free to add new capabilities by creating a new MR.

## Contributors

- Samuel López Saura @elchicodepython
- Ilya Sapunov @davert0

