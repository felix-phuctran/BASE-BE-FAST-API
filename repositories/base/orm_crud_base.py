from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.base.class_base import Base
from repositories.base.query_builder import get_filter, query_builder
from utils.crypto import clone_model
from utils.string_case import decamelize

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ORMCRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    A generic CRUD class providing common operations for an SQLAlchemy model, using AsyncSession.

    This class supports typical operations such as:
    - get / get_including_soft_deleted
    - get_multi / get_multi_including_soft_deleted
    - create
    - update / patch
    - remove (soft-delete)
    - delete (hard-delete)
    - get_one_by / get_one_by_or_fail (filter-based retrieval)
    - clone / save
    - batch_insert_with_objects / batch_insert_with_mappings

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initializes the ORMCRUDBase with a specific SQLAlchemy model class.
        
        Args:
            model (Type[ModelType]): The SQLAlchemy model class.
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Retrieves a single record by its ID, ignoring records with non-null `deleted_at`.

        Args:
            db (AsyncSession): The active async database session.
            id (Any): The primary key of the record to retrieve.

        Returns:
            Optional[ModelType]: The record if found, otherwise None.
        """
        obj = await db.get(self.model, id)
        if obj and getattr(obj, "deleted_at", None) is None:
            return obj
        return None

    async def get_including_soft_deleted(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Retrieves a single record by its ID, including soft-deleted records.

        Args:
            db (AsyncSession): The active async database session.
            id (Any): The primary key of the record to retrieve.

        Returns:
            Optional[ModelType]: The record if found, otherwise None.
        """
        return await db.get(self.model, id)

    async def get_multi(
        self,
        db: AsyncSession,
        filter_param: dict = None,
    ) -> List[ModelType]:
        """
        Retrieves multiple records (excluding soft-deleted ones) based on optional filter parameters.

        Args:
            db (AsyncSession): The active async database session.
            filter_param (dict, optional): Dictionary of filters, ordering, includes, etc.

        Returns:
            List[ModelType]: A list of matching records.
        """
        if filter_param is None:
            filter_param = {}

        query = query_builder(
            model=self.model,
            filter=filter_param.get("filter"),
            order_by=filter_param.get("order_by"),
            include=filter_param.get("include"),
            join=filter_param.get("join"),
        )

        # Exclude soft-deleted
        query = query.filter(self.model.deleted_at.is_(None))

        # Pagination
        query = query.offset(filter_param.get("skip")).limit(filter_param.get("limit"))

        result = await db.execute(query)
        return result.scalars().all()

    async def get_multi_including_soft_deleted(
        self,
        db: AsyncSession,
        filter_param: dict = None,
    ) -> List[ModelType]:
        """
        Retrieves multiple records, including soft-deleted ones, based on optional filter parameters.

        Args:
            db (AsyncSession): The active async database session.
            filter_param (dict, optional): Dictionary of filters, ordering, includes, etc.

        Returns:
            List[ModelType]: A list of matching records.
        """
        if filter_param is None:
            filter_param = {}

        query = query_builder(
            model=self.model,
            filter=filter_param.get("filter"),
            order_by=filter_param.get("order_by"),
            include=filter_param.get("include"),
            join=filter_param.get("join"),
        )

        query = query.offset(filter_param.get("skip")).limit(filter_param.get("limit"))
        result = await db.execute(query)
        return result.scalars().all()

    async def get_multi_by(
        self,
        db: AsyncSession,
        filter_param: dict = None,
    ) -> Dict[str, Any]:
        """
        Retrieves multiple records (excluding soft-deleted) and returns total count plus the records.

        Args:
            db (AsyncSession): The active async database session.
            filter_param (dict, optional): Dictionary of filters, ordering, includes, etc.

        Returns:
            Dict[str, Any]: A dictionary with 'total' and 'results'.
        """
        if filter_param is None:
            filter_param = {}

        query = query_builder(
            model=self.model,
            filter=filter_param.get("filter"),
            order_by=filter_param.get("order_by"),
            include=filter_param.get("include"),
            join=filter_param.get("join"),
        )

        # Count total before filtering out soft-deleted
        stmt_count = select(func.count()).select_from(query.subquery())
        total = await db.scalar(stmt_count)

        # Exclude soft-deleted
        query = query.filter(self.model.deleted_at.is_(None))

        # Pagination
        query = query.offset(filter_param.get("skip")).limit(filter_param.get("limit"))

        results = await db.execute(query)
        return {
            "total": total,
            "results": results.scalars().all(),
        }

    async def get_multi_including_soft_deleted_by(
        self,
        db: AsyncSession,
        filter_param: dict = None,
    ) -> Dict[str, Any]:
        """
        Retrieves multiple records (including soft-deleted) and returns total count plus the records.

        Args:
            db (AsyncSession): The active async database session.
            filter_param (dict, optional): Dictionary of filters, ordering, includes, etc.

        Returns:
            Dict[str, Any]: A dictionary with 'total' and 'results'.
        """
        if filter_param is None:
            filter_param = {}

        query = query_builder(
            model=self.model,
            filter=filter_param.get("filter"),
            order_by=filter_param.get("order_by"),
            include=filter_param.get("include"),
            join=filter_param.get("join"),
        )

        # Count total rows, including soft-deleted
        total = await db.scalar(query.with_entities(func.count()))

        # Pagination
        query = query.offset(filter_param.get("skip", 0)).limit(filter_param.get("limit", 10))
        results = await db.execute(query)

        return {
            "total": total,
            "results": results.scalars().all(),
        }

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Creates a new record in the database.

        Args:
            db (AsyncSession): The active async database session.
            obj_in (CreateSchemaType): A Pydantic schema for creation.

        Returns:
            ModelType: The newly created record.

        Raises:
            HTTPException: If integrity constraints fail (e.g., unique constraint).
        """
        obj_in_data = decamelize(jsonable_encoder(obj_in))
        # Convert ISO datetime strings to Python datetime objects if present
        for field in ["created_at", "updated_at", "deleted_at", "expires_at"]:
            if field in obj_in_data and isinstance(obj_in_data[field], str):
                try:
                    obj_in_data[field] = datetime.fromisoformat(obj_in_data[field].replace('Z', '+00:00'))
                except ValueError:
                    pass

        db_obj = self.model(**obj_in_data)  # type: ignore

        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=e.orig.diag.message_detail or "Key already exists"
            ) from None

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Performs a full update on an existing record.

        Args:
            db (AsyncSession): The active async database session.
            db_obj (ModelType): The existing database record to update.
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): The update payload.

        Returns:
            ModelType: The updated record.
        """
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_defaults=True)

        update_data = decamelize(update_data)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def patch(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Performs a partial update (patch) on an existing record (only updates fields provided).

        Args:
            db (AsyncSession): The active async database session.
            db_obj (ModelType): The existing database record to patch.
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): The partial update payload.

        Returns:
            ModelType: The patched record.
        """
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data = decamelize(update_data)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: Any) -> ModelType:
        """
        Soft-deletes a record by setting 'deleted_at' to the current time 
        (and optionally 'is_active' to False if defined).

        Args:
            db (AsyncSession): The active async database session.
            id (Any): The primary key of the record to soft-delete.

        Returns:
            ModelType: The soft-deleted record.
        """
        db_obj = await db.get(self.model, id)
        db_obj.is_active = False
        db_obj.deleted_at = datetime.now()

        db.add(db_obj)
        await db.commit()
        return db_obj

    async def delete(self, db: AsyncSession, *, id: Any) -> ModelType:
        """
        Hard-deletes a record from the database by primary key.

        Args:
            db (AsyncSession): The active async database session.
            id (Any): The primary key of the record to hard-delete.

        Returns:
            ModelType: The deleted record (object is gone from DB after commit).
        """
        obj = await db.get(self.model, id)
        await db.delete(obj)
        await db.commit()
        return obj

    async def delete_obj(self, db: AsyncSession, *, obj: ModelType) -> ModelType:
        """
        Hard-deletes a given record from the database.

        Args:
            db (AsyncSession): The active async database session.
            obj (ModelType): The record to delete.

        Returns:
            ModelType: The deleted record (object is gone from DB after commit).
        """
        await db.delete(obj)
        await db.commit()
        return obj

    async def get_one_by_or_fail(self, db: AsyncSession, filter: dict = {}) -> Optional[ModelType]:
        """
        Retrieves a single record by applying filter criteria; raises 404 if no record matches.

        Args:
            db (AsyncSession): The active async database session.
            filter (dict, optional): Filter conditions.

        Returns:
            Optional[ModelType]: The matched record, if found.

        Raises:
            HTTPException: 404 if not found.
        """
        model = await self.get_one_by(db, filter)
        if not model:
            self._throw_not_found_exception()
        return model

    async def get_one_by(self, db: AsyncSession, filter: dict = {}) -> Optional[ModelType]:
        """
        Retrieves a single record by applying filter criteria, ignoring soft-deleted records.

        Args:
            db (AsyncSession): The active async database session.
            filter (dict, optional): Filter conditions.

        Returns:
            Optional[ModelType]: The matched record, if found.
        """
        stmt = select(self.model).filter(
            and_(
                self.model.deleted_at.is_(None),
                get_filter(self.model, filter),
            )
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_one_including_soft_deleted_by(self, db: AsyncSession, filter: dict = {}) -> Optional[ModelType]:
        """
        Retrieves a single record by applying filter criteria, including soft-deleted records.

        Args:
            db (AsyncSession): The active async database session.
            filter (dict, optional): Filter conditions.

        Returns:
            Optional[ModelType]: The matched record, if found.
        """
        stmt = select(self.model).filter(
            and_(
                get_filter(self.model, filter),
            )
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def update_one_by(
        self,
        db: AsyncSession,
        filter: dict = {},
        obj_in: Union[UpdateSchemaType, Dict[str, Any]] = "{}",
    ) -> Optional[ModelType]:
        """
        Finds a single record by filter (ignoring soft-deleted), then applies an update if found.

        Args:
            db (AsyncSession): The active async database session.
            filter (dict, optional): Filter conditions.
            obj_in (Union[UpdateSchemaType, Dict[str, Any]], optional): Update payload. Defaults to "{}".

        Returns:
            Optional[ModelType]: The updated record, or None if not found.
        """
        stmt = select(self.model).filter(
            and_(
                self.model.deleted_at.is_(None),
                get_filter(self.model, filter),
            )
        )
        result = await db.execute(stmt)
        model = result.scalars().first()

        if not model:
            return None

        return await self.update(db=db, db_obj=model, obj_in=obj_in)

    def _throw_not_found_exception(self):
        """
        Helper method to raise a 404 Not Found HTTPException with a generic message.
        """
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found"
        )

    async def clone(self, db: AsyncSession, model_obj: ModelType, modify: dict = {}):
        """
        Clones an existing record and inserts the cloned object into the database.

        Args:
            db (AsyncSession): The active async database session.
            model_obj (ModelType): The existing record to clone.
            modify (dict, optional): Additional fields to override in the clone.

        Returns:
            ModelType: The cloned record.
        """
        dict_ = {**clone_model(model_obj), **modify}
        clone_obj = self.model(**dict_)
        try:
            db.add(clone_obj)
            await db.commit()
            await db.refresh(clone_obj)
            return clone_obj
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=422,
                detail=e.orig.diag.message_detail or "Key already exists"
            ) from None

    async def save(self, db: AsyncSession, model_obj: ModelType) -> ModelType:
        """
        Saves (persists) any model object to the database (insert or update).

        Args:
            db (AsyncSession): The active async database session.
            model_obj (ModelType): The record to save.

        Returns:
            ModelType: The saved record.
        """
        db.add(model_obj)
        await db.commit()
        await db.refresh(model_obj)
        return model_obj

    async def batch_insert_with_objects(
        self,
        db: AsyncSession,
        objects: List[ModelType]
    ) -> List[Dict[str, Any]]:
        """
        Performs a batch insert of multiple ORM objects (already constructed model instances).

        Args:
            db (AsyncSession): The active async database session.
            objects (List[ModelType]): List of model instances to insert.

        Returns:
            List[Dict[str, Any]]: The inserted objects in dictionary form.

        Raises:
            HTTPException: If any error occurs during batch insert.
        """
        try:
            mappings = [jsonable_encoder(obj) for obj in objects]
            await db.execute(
                self.model.__table__.insert().values(mappings)
            )
            await db.commit()
            return mappings
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=422,
                detail=f"Batch insert failed: {str(e)}"
            )

    async def batch_insert_with_mappings(
        self,
        db: AsyncSession,
        mappings: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Performs a batch insert using raw dictionary mappings (column->value).

        Args:
            db (AsyncSession): The active async database session.
            mappings (List[Dict[str, Any]]): List of dictionaries mapping column names to values.

        Returns:
            List[Dict[str, Any]]: The inserted mappings.

        Raises:
            HTTPException: If any error occurs during batch insert.
        """
        try:
            await db.execute(
                self.model.__table__.insert().values(mappings)
            )
            await db.commit()
            return mappings
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=422,
                detail=f"Batch insert failed: {str(e)}"
            )
