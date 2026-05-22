from typing import Annotated
from fastapi import Depends, UploadFile, File, HTTPException
import filetype


class AudioFileValidator:
    def __init__(self, allowed_extensions: set[str]) -> None:
        self.allowed_extensions: set[str] = allowed_extensions
    
    async def __call__(self, file: UploadFile = File(...)) -> UploadFile:
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=415, detail="Payload must be an audio file")
        
        header_bytes = await file.read(2048)
        await file.seek(0)

        kind = filetype.guess(header_bytes)

        if kind is None or not kind.mime.startswith("audio/"):
            raise HTTPException(status_code=415, detail="Invalid audio signature.")
        
        if kind.extension not in self.allowed_extensions:
            raise HTTPException(
                status_code=415, 
                detail=f"Format '{kind.extension}' not allowed."
            )
        
        return file

AudioFile = Annotated[UploadFile, Depends(AudioFileValidator({"mp3", "webm", "m4a", "ogg"}))]
