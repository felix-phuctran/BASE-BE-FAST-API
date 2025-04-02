from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')

class PaginationResponseSchema(BaseModel, Generic[T]):
    """
    Generic pagination response schema for all list endpoints.
    
    Attributes:
        total (int): The total number of records available.
        results (List[T]): The actual records for the current page.
        
    Example:
        >>> PaginationResponseSchema[UserResponseSchema](
        ...     total=100, 
        ...     results=[UserResponseSchema(...)]
        ... )
    
    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    total: int = Field(..., description="Total number of records available")
    results: List[T] = Field(..., description="Records for the current page")
    
    class Config:
        from_attributes = True 