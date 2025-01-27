from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from app import crud, database, utils
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

async def lifespan(app: FastAPI):
    database.Base.metadata.create_all(bind=database.engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_video(
    title: str = Form(...), description: str = Form(...), file: UploadFile = None
):
    if not file:
        raise HTTPException(status_code=400, detail="video file required")
    
    video_bucket, video_name = utils.upload_to_minio(file)

    db = database.get_db()
    video = crud.create_video(db, title, description, video_name, video_bucket)

    return JSONResponse({"Message": f"video uploaded: {video}"})

@app.get("/videos/{video_id}")
async def get_video(video_id: int):
    db = database.get_db()
    video = crud.get_video(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    print("found in postges")
    try:
        resp = utils.get_video_from_minio(video)
        return StreamingResponse(
            resp.stream(32 * 1024),
            media_type="application/octet-stream"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Video not found in minio {video.video_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        
