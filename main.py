import subprocess
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class URLRequest(BaseModel):
    url: str

@app.post("/extract")
def extract_metadata(data: URLRequest):
    try:
        # Run yt-dlp to extract JSON metadata without downloading the media
        command = ["yt-dlp", "--dump-json", "--no-playlist", data.url]
        result = subprocess.run(command, capture_precision=True, text=True, check=True, timeout=30)
        
        metadata = json.loads(result.stdout)
        
        # Filter out only what you need (e.g., title, direct URL, thumbnail)
        return {
            "title": metadata.get("title"),
            "thumbnail": metadata.get("thumbnail"),
            "duration": metadata.get("duration"),
            "direct_url": metadata.get("url") # or formats list
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"yt-dlp failed: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))