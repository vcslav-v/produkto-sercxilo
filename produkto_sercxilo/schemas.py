from typing import List, Optional

from pydantic import BaseModel


class FabImg(BaseModel):
    source: str
    alt: Optional[str]


class Dimensions(BaseModel):
    width: int
    height: int


class FabItem(BaseModel):

    title: str
    product_url: str
    file_format: Optional[str]
    file_size: Optional[int]
    file_dimensions: Optional[Dimensions]
    description: Optional[str]
    images: Optional[List[FabImg]]
    preview_images: Optional[List[FabImg]]
