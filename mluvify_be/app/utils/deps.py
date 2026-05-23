from typing import Annotated
from fastapi import UploadFile, File, HTTPException, status, Depends
import filetype


class AudioFileValidator:
    def __init__(self, allowed_extensions: set[str]) -> None:
        self.allowed_extensions: set[str] = allowed_extensions
    
    async def __call__(self, file: UploadFile = File(...)) -> UploadFile:
        if not file.content_type or not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                detail="Payload must be an audio file."
            )
        
        header_bytes = await file.read(2048)
        
        await file.seek(0)

        kind = filetype.guess(header_bytes)

        if kind is None:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                detail="Could not determine file type."
            )

        is_valid_mime = (
            kind.mime.startswith("audio/") or 
            kind.mime in ["video/webm", "video/mp4", "application/ogg"]
        )

        if not is_valid_mime:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                detail=f"Invalid audio signature. Detected: {kind.mime}"
            )
        
        if kind.extension not in self.allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                detail=f"Format '{kind.extension}' is not allowed."
            )
        
        return file


AudioFile = Annotated[UploadFile, Depends(AudioFileValidator({"mp3", "webm", "m4a", "ogg"}))]
