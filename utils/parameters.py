from fastapi import Query
from utils.string_case import convert_filter_to_camel_case, to_snake_case


async def common_filter_parameters(
    page: int = 1,
    limit: int = 100,
    filter: str = "{}",
    include: str = None,
    join: str = "{}",
    orderBy: str = None,
):
    if join:
        join_ = convert_filter_to_camel_case(join)
    else:
        join_ = "{}"

    if filter:
        filter_ = convert_filter_to_camel_case(filter)
    else:
        filter_ = "{}"

    if include:
        include = to_snake_case(include)
    else:
        include = None
    skip = round((page - 1) * limit)
    if skip < 1:
        skip = 0
    if orderBy and orderBy != "":
        orderBy = to_snake_case(orderBy)
    else:
        orderBy = None
    return {
        "skip": skip,
        "limit": limit,
        "filter": filter_,
        "include": include,
        "order_by": orderBy,
        "join": join_,
    }

async def common_filter_parameters_and_actions(
    page: int = 1,
    limit: int = 100,
    filter: str = "{}",
    include: str = None,
    join: str = "{}",
    orderBy: str = None,
    action: str = "",
):
    if join:
        join_ = convert_filter_to_camel_case(join)
    else:
        join_ = "{}"

    if filter:
        filter_ = convert_filter_to_camel_case(filter)
    else:
        filter_ = "{}"

    if include:
        include = to_snake_case(include)
    else:
        include = None
    skip = round((page - 1) * limit)
    if skip < 1:
        skip = 0
    if orderBy and orderBy != "":
        orderBy = to_snake_case(orderBy)
    else:
        orderBy = None
    return {
        "skip": skip,
        "limit": limit,
        "filter": filter_,
        "include": include,
        "order_by": orderBy,
        "join": join_,
        "action": action,
    }

async def common_filter_parameters_with_id(
    page: int = 1,
    limit: int = 100,
    filter: str = "{}",
    include: str = None,
    join: str = "{}",
    orderBy: str = None,
    id: str = "",
):
    if join:
        join_ = convert_filter_to_camel_case(join)
    else:
        join_ = "{}"

    if filter:
        filter_ = convert_filter_to_camel_case(filter)
    else:
        filter_ = "{}"

    if include:
        include = to_snake_case(include)
    else:
        include = None
    skip = round((page - 1) * limit)
    if skip < 1:
        skip = 0
    if orderBy and orderBy != "":
        orderBy = to_snake_case(orderBy)
    else:
        orderBy = None
    return {
        "skip": skip,
        "limit": limit,
        "filter": filter_,
        "include": include,
        "order_by": orderBy,
        "join": join_,
        "id": id,
    }

async def search_pagination(page: int = 1, limit: int = 100, keyword: str = ""):
    return {"page": page, "limit": limit, "keyword": keyword}

async def actions(action: str = ""):
    return {"action": action}

async def actions_with_id(id: str = "", action: str = ""):
    return {"id": id, "action": action}

async def province_pagination(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    code: str = "",
    name: str = "",
    created_at: str = "",
    updated_at: str = "",
):
    return {
        "limit": limit,
        "offset": offset,
        "code": code,
        "name": name,
        "created_at": created_at,
        "updated_at": updated_at,
    }

async def district_pagination(
    name: str = "",
    prefix: str = "",
    province_id: int = 0,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    created_at: str = "",
    updated_at: str = "",
):
    return {
        "name": name,
        "prefix": prefix,
        "province_id": province_id,
        "limit": limit,
        "offset": offset,
        "created_at": created_at,
        "updated_at": updated_at,
    }

async def ward_pagination(
    name: str = "",
    prefix: str = "",
    tiki_ward_code: str = "",
    province_id: int = 297,
    district_id: int = 13,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    created_at: str = "",
    updated_at: str = "",
):
    return {
        "name": name,
        "prefix": prefix,
        "tiki_ward_code": tiki_ward_code,
        "province_id": province_id,
        "district_id": district_id,
        "limit": limit,
        "offset": offset,
        "created_at": created_at,
        "updated_at": updated_at,
    }
