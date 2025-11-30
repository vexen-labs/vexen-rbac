"""
Base DTOs and response structures.
"""

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class BaseResponse(Generic[T]):
	"""
	Generic response wrapper for use cases.

	Attributes:
		success: Whether the operation was successful
		data: The response data (if successful)
		error: Error message (if failed)
	"""

	success: bool
	data: T | None = None
	error: str | None = None

	@classmethod
	def ok(cls, data: T) -> "BaseResponse[T]":
		"""
		Create a successful response.

		Args:
			data: The response data

		Returns:
			BaseResponse: Success response with data
		"""
		return cls(success=True, data=data, error=None)

	@classmethod
	def fail(cls, error: str) -> "BaseResponse[T]":
		"""
		Create a failed response.

		Args:
			error: Error message

		Returns:
			BaseResponse: Failed response with error message
		"""
		return cls(success=False, data=None, error=error)
