from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class PaginationRequest:
	page: int = 1
	page_size: int = 20


@dataclass
class PaginationResponse:
	page: int
	page_size: int
	total_pages: int
	total_items: int
	has_next: bool
	has_prev: bool


@dataclass
class PaginatedResponse(Generic[T]):
	success: bool
	data: list[T]
	pagination: PaginationResponse
	error: str | None = None
