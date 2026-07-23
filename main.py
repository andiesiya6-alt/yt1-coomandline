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
        
        # Fixed: changed capture_precision to capture_output
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=30)
        
        metadata = json.loads(result.stdout)
        
        return {
            "title": metadata.get("title"),
            "thumbnail": metadata.get("thumbnail"),
            "duration": metadata.get("duration"),
            "direct_url": metadata.get("url")
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"yt-dlp failed: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))