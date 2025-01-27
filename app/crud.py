from sqlalchemy.orm import Session
from app.models import Video
from app.schemas import VideoCreate

def create_video(db: Session, title: str, description: str, video_name: str, video_bucket):
    with db() as db:
        video = Video(title=title, description=description, video_name=video_name, video_bucket=video_bucket)
        db.add(video)
        db.commit()
        db.refresh(video)
        return video.id

def get_video(db: Session, video_id: int):
    with db() as db:
        return db.query(Video).filter(Video.id==video_id).first()