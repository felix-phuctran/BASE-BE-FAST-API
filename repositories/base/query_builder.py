import json
from typing import Optional, Type, TypeVar, Union

import sqlalchemy
from databases.base.class_base import Base
from fastapi import HTTPException
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import cast

ModelType = TypeVar("ModelType", bound=Base)

# A
# filter={"title__like":"%a%"}
# --->>>   SELECT * FROM items WHERE title like '%a%'

# A and B
# filter={"title__ilike":"%a%", "id__gte":1}
# --->>>   SELECT * FROM items WHERE (title ilike '%a%') AND (id >= 1)

# A and B and C
# filter={"title__like":"%a%", "id__lt":10, "owner_id": 1}
# --->>>   SELECT * FROM items WHERE (title like '%a%') AND (id < 10) AND (owner_id = 1)

# A or B
# filter=[{"title__ilike":"%a%"}, {"id__gte":1}]
# --->>>   SELECT * FROM items WHERE (title ilike '%a%') OR (id >= 1)

# A or B or C
# filter=[{"title__like":"%a%"}, {"id__lt":10}, {"owner_id": 1}]
# --->>>   SELECT * FROM items WHERE (title like '%a%') OR (id < 10) OR (owner_id = 1)

# (A and B) or C
# filter=[{"title__like":"%a%", "id__lt":10}, {"owner_id": 1}]
# --->>>   SELECT * FROM items WHERE (title like '%a%' AND id < 10) OR owner_id = 1

# (A and B and C) or D
# filter=[{"title__like":"%a%", "id__lt":10, "id__gt": 1}, {"owner_id": 1}]
# --->>>   SELECT * FROM items WHERE (title like '%a%' AND id < 10 AND id > 1) OR owner_id = 1

# (A and B) or (C and D)
# filter=[{"title__like":"%a%", "id__lt":10}, {"id__gt":1, "owner_id":1}]
# --->>>   SELECT * FROM items WHERE (title like '%a%' AND id < 10) OR (id > 1 AND owner_id = 1)

# (A or B) and C
# filter={"0":[{"title__like":"%a%"}, {"owner_id": 1}], "owner_id__lte": 20}
# --->>>   SELECT * FROM items WHERE (title like '%a%' OR owner_id = 1) AND owner_id <= 20

# (A or B) and (C or D)
# filter={"0":[{"title__like":"%a%", "id__lt":10}, {"owner_id":1}], "1":[{"owner_id__lte":20}, {"owner_id__gte":10}]}
# --->>>   SELECT * FROM items WHERE (title like '%a%' AND id <10) OR owner_id=1) AND (owner_id<=20 OR owner_id>=10)

# (A join B), filter B.id
# filter={"b.id__": "1"}
# join={'b': {}}
# --->>>   SELECT * FROM A a JOIN B b WHERE b.id = 1


def query_builder(
    model: Type[ModelType],
    filter: Union[str, dict] = None,
    order_by: str = None,
    include: str = None,
    join: str = None,
):
    """
    Builds a SELECT query (SQLAlchemy 2.x style with AsyncSession) with optional filters, ordering, joins, and includes.

    Args:
        model (Type[ModelType]): The SQLAlchemy model to query.
        filter (Union[str, dict], optional): Filter conditions in JSON string or dictionary format.
        order_by (str, optional): Column(s) for ordering results, prefixed with '-' for descending order.
        include (str, optional): Comma-separated relationships to load with the query.
        join (str, optional): JSON string specifying table joins.

    Returns:
        Select: The constructed SQLAlchemy Select object (to be executed with `await db.execute(query)`).

    Example:
        >>> query = query_builder(
        ...     model=ItemModel,
        ...     filter='{"title__like": "%a%"}',
        ...     order_by="-id",
        ...     include="owner"
        ... )
        >>> result = await db.execute(query)
        >>> items = result.scalars().all()

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    # Start a SELECT statement
    base_query = select(model)

    # Handle 'join' logic (placeholder - you can expand this as needed)
    if join is not None:
        # parse JSON string 'join', iterate over tables to join...
        # e.g. join = '{"relation_name": {}}'
        # base_query = base_query.join(...) or base_query = base_query.outerjoin(...)
        pass

    # Build 'where' clause from filter (using get_filter)
    if filter is not None:
        if isinstance(filter, str):
            filter = json.loads(filter)
        where_clause = get_filter(model, filter)  # <--- we directly use get_filter
        if where_clause is not None:
            base_query = base_query.where(where_clause)

    # Eager loading (include)
    if include is not None:
        includes = include.split(",")
        load_options = []
        for inc in includes:
            load_options.append(selectinload(inc.strip()))
        if load_options:
            base_query = base_query.options(*load_options)

    # Order by logic
    if order_by is not None:
        orders = order_by.split(",")
        for od in orders:
            if od.startswith("-"):
                col_name = od[1:]
                base_query = base_query.order_by(getattr(model, col_name).desc())
            else:
                col_name = od
                base_query = base_query.order_by(getattr(model, col_name).asc())

    return base_query


def get_class_by_tablename(tablename: str):
    """
    Return class reference mapped to a specific table name.

    Args:
        tablename (str): The name of the database table.

    Returns:
        Type[ModelType]: The SQLAlchemy model class mapped to the table or None.

    Example:
        >>> get_class_by_tablename("items")
        <class 'app.databases.ItemModel'>

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    for c in Base._decl_class_registry.values():
        if hasattr(c, "__tablename__") and c.__tablename__ == tablename:
            return c


def get_join_table(join: dict) -> list:
    """
    Extracts table names from a join configuration.

    Args:
        join (dict): Join configuration as a dictionary.

    Returns:
        list: List of table names for joining.

    Example:
        >>> get_join_table({"b": {}})
        ['b']

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if isinstance(join, dict):
        return [key for key, _ in join.items()]
    return []


def get_filter(
    model: Type[ModelType], filters
) -> sqlalchemy.sql.elements.BooleanClauseList:
    """
    Constructs filter conditions for a SELECT statement.

    Args:
        model (Type[ModelType]): The SQLAlchemy model to apply filters to.
        filters (Union[dict, list]): Filter conditions as a dictionary or list of dictionaries.

    Returns:
        BooleanClauseList: Combined filter conditions for the query.

    Example:
        >>> get_filter(ItemModel, {"title__like": "%a%", "id__gte": 1})

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if isinstance(filters, list):
        # e.g. filter=[{"title__like": "%a%"}, {"id__gte":1}] => OR
        return or_(*[get_filter(model, f) for f in filters])

    if isinstance(filters, dict):
        # Might contain nested numeric keys for grouping
        sub_filters = [val for key, val in filters.items() if key.isnumeric()]
        and_parts = [get_filter(model, sf) for sf in sub_filters]

        # normal conditions
        conditions = [item for item in filters.items() if not item[0].isnumeric()]
        op_parts = [get_op(model, k, v) for k, v in conditions]

        return and_(*and_parts, *op_parts)

    return and_()  # return a no-op clause if filters is empty or invalid


def get_count(query: sqlalchemy.sql.Select):
    """
    Counts the number of rows matching a SELECT query.

    Args:
        query (Select): SQLAlchemy Select object.

    Returns:
        Select: A SELECT statement that can be executed to get the count.

    Example:
        >>> count_query = get_count(select(ItemModel).where(ItemModel.deleted_at==None))
        >>> result = await db.execute(count_query)
        >>> total = result.scalar()

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return select(func.count()).select_from(query.subquery())


def get_include(include: str) -> list:
    """
    Processes include parameter to load related objects with a query.

    Args:
        include (str): Comma-separated list of relationships to include.

    Returns:
        list: List of SQLAlchemy `selectinload` options for the query.

    Example:
        >>> get_include("owner,category")
        [selectinload("owner"), selectinload("category")]

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return [selectinload(r.strip()) for r in include.split(",")]


def get_order_by(model: Type[ModelType], order_by: str) -> list:
    """
    Parses order_by parameter into SQLAlchemy order conditions.

    Args:
        model (Type[ModelType]): The SQLAlchemy model to order by.
        order_by (str): Comma-separated list of columns to order by, prefixed with '-' for descending order.

    Returns:
        list: List of SQLAlchemy ordering conditions.

    Example:
        >>> get_order_by(ItemModel, "-created_at,name")
        [ItemModel.created_at.desc(), ItemModel.name.asc()]

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    orders = []
    for od in order_by.split(","):
        if od.startswith("-"):
            col = getattr(model, od[1:], None)
            if col is not None:
                orders.append(col.desc())
        else:
            col = getattr(model, od, None)
            if col is not None:
                orders.append(col.asc())
    return orders


def get_attr_order(model: Type[ModelType], attr: str):
    """
    Converts an order_by attribute to a SQLAlchemy ordering condition.

    Args:
        model (Type[ModelType]): The SQLAlchemy model.
        attr (str): Attribute to order by, prefixed with '-' for descending.

    Returns:
        ColumnElement: SQLAlchemy column ordering condition.

    Example:
        >>> get_attr_order(ItemModel, "-created_at")
        ItemModel.created_at.desc()

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    # This is no longer used if we directly parse order_by in get_order_by
    if attr.startswith("-"):
        return getattr(model, attr[1:]).desc()
    return getattr(model, attr).asc()


def get_op(model: Type[ModelType], key: str, value: str):
    """
    Builds a SQLAlchemy filter condition based on a key-value pair.

    Args:
        model (Type[ModelType]): The SQLAlchemy model.
        key (str): The column name and filter operator (e.g., 'title__like').
        value (Union[str, list, None]): The value to filter by.

    Returns:
        BinaryExpression: SQLAlchemy filter condition.

    Example:
        >>> get_op(ItemModel, "title__like", "%test%")
        ItemModel.title.like('%test%')

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    from sqlalchemy.sql.expression import cast

    column_name = key.split("__")[0]

    # If there's a dot notation, e.g. "relation.column__op"
    if "." in key:
        column_name = column_name.split(".")[1]
        sub_key = key.split(".")[0]
        ref_instance = getattr(model, sub_key)
        instance_table_name = ref_instance.property.entity.mapped_table.name
        model = get_class_by_tablename(instance_table_name)

    column_obj = getattr(model, column_name)

    op = key.split("__")[-1]
    if op == column_name:
        # means no op
        return column_obj == value
    if op == "lt":
        return column_obj < value
    if op == "lte":
        return column_obj <= value
    if op == "gte":
        return column_obj >= value
    if op == "gt":
        return column_obj > value
    if op == "neq":
        return column_obj != value
    if op == "like":
        return cast(column_obj, sqlalchemy.String).like(f"%{value}%")
    if op == "ilike":
        return cast(column_obj, sqlalchemy.String).ilike(f"%{value}%")
    if op == "in":
        return column_obj.in_(value)
    if op == "nin":
        return ~column_obj.in_(value)
    if op == "is":
        return column_obj.is_(value)
    if op == "isn":
        return column_obj.isnot(value)
    if op == "between":
        return column_obj.between(*value)
    if op == "isnull":
        if value is True:
            return column_obj.is_(None)
        else:
            return column_obj.isnot(None)

    # default eq
    return column_obj == value


def prepare_filter_param(
    common_filter_parameters: dict,
    attribute_id: Optional[str] = None,
    attribute_name: Optional[str] = None,
) -> dict:
    """
    Prepares a filter parameter dictionary by optionally adding a specific attribute and its value.

    This method performs the following steps:
    1. Retrieves the existing filter parameters from the provided dictionary.
    2. If the filter parameter is a string, attempts to parse it as JSON.
    3. If both `attribute_id` and `attribute_name` are provided, adds the attribute and its value to the filter parameters.
    4. Returns the updated filter parameters as a dictionary.

    Args:
        common_filter_parameters (dict): The dictionary containing common filter parameters.
        attribute_id (Optional[str]): The value to be added to the filter parameters. Default is None.
        attribute_name (Optional[str]): The name of the attribute to be added to the filter parameters. Default is None.

    Returns:
        dict: The updated filter parameters dictionary.

    Raises:
        HTTPException: If the filter parameter is an invalid JSON string.

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    filter_param = common_filter_parameters.get("filter", "{}")
    if isinstance(filter_param, str):
        try:
            filter_param = json.loads(filter_param)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid filter parameter")

    if attribute_id and attribute_name:
        filter_param[attribute_name] = str(attribute_id)

    return {"filter": filter_param}


def prepare_pagination(common_filter_parameters: dict) -> dict:
    """
    Prepares pagination parameters for querying items.

    This method performs the following steps:
    1. Retrieves the page number from the provided dictionary, defaulting to 1 if not provided.
    2. Retrieves the limit of items per page from the provided dictionary, defaulting to 10 if not provided.
    3. Calculates the number of items to skip based on the page number and limit.
    4. Returns the pagination parameters as a dictionary.

    Args:
        common_filter_parameters (dict): The dictionary containing common filter parameters.

    Returns:
        dict: The pagination parameters dictionary containing 'skip' and 'limit'.

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    page = common_filter_parameters.get("page", 1)
    limit = common_filter_parameters.get("limit", 10)
    skip = common_filter_parameters.get("skip", round((page - 1) * limit))
    return {"skip": skip, "limit": limit}
