from pydantic import BaseModel

class VideoCreate(BaseModel):
    title: str
    description: str
    video_name: str
    video_bucket: str

class Video(VideoCreate):
    id: int

    class Config:
        orm_mode = True