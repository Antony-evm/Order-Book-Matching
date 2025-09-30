"""
This module defines the expected response when the API call is successful.
"""
from typing import Optional, Any

from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi import status
from .metadata import Metadata


class SuccessResponseModel[DataT](BaseModel):
    data: Optional[DataT] = Field(
        None,
        description="The data returned by the API call. This can be any type of data "
                    "depending on the specific API endpoint."
    )
    metadata: Metadata = Field(
        ...,
        description="Metadata object, providing additional information "
                    "about the API call such as tokens used and time taken."
    )


class SuccessResponse(JSONResponse):
    def __init__(
            self,
            metadata: Metadata,
            response_data: Optional[Any] = None,
    ):
        super().__init__(
            status_code=status.HTTP_200_OK,
            content={
                "data": (
                            response_data.model_dump()
                            if isinstance(response_data, BaseModel)
                            else response_data
                        ) or {},
                "metadata": metadata.model_dump(mode="json")
            }
        )
