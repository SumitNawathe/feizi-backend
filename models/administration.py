
from dataclasses import dataclass
from typing import List


@dataclass
class User:
    _id: int
    username: str
    email: str
    password: str

@dataclass
class UploadedImage:
    _id: int
    user_id: int
    filename: str
    label: str

@dataclass
class Segmentation:
    _id: int
    image_id: int
    points: List[List[float]]

