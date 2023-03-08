
from dataclasses import dataclass
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
