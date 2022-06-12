def get_query_params(filter_obj, params) -> dict:
    query_params = params or {}
    if filter_obj:
        query_params["where"] = filter_obj.get_where()
    return query_params
