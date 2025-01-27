import io
from minio import Minio
from minio.error import S3Error
from app.models import Video

minio_client = Minio(
    "minio:9000", access_key="admin", secret_key="password", secure=False
)

def upload_to_minio(file):
    bucket_name = "videos"
    if not minio_client.bucket_exists(bucket_name=bucket_name):
        minio_client.make_bucket(bucket_name)
    
    file_data = file.file.read()
    file_size = len(file_data)
    minio_client.put_object(
        bucket_name, file.filename, io.BytesIO(file_data), file_size, content_type=file.content_type
    )
    return bucket_name, file.filename

def get_video_from_minio(video: Video):
    bucket_name = video.video_bucket
    try:
        if not minio_client.bucket_exists(bucket_name):
            raise FileNotFoundError(f"Bucket {bucket_name} does not exist")
        print()
        resp = minio_client.get_object(bucket_name=bucket_name, object_name=video.video_name)
        return resp
    except S3Error as e:
        raise Exception(f"Error fetching content: {str(e)}")