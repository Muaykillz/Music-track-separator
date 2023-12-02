from fastapi import FastAPI, File, UploadFile, HTTPException
from spleeter.separator import Separator
import shutil
import os

app = FastAPI()
separator = Separator('spleeter:2stems')

@app.post("/separate")
async def separate_audio(audio_file: UploadFile = File(...)):
    # Ensure the file is an audio file
    if not audio_file.filename.lower().endswith(('.mp3', '.wav', '.ogg')):
        raise HTTPException(status_code=400, detail="Only audio files are supported")

    # Save the uploaded file
    file_path = f"uploads/{audio_file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(audio_file.file, f)

    # Perform separation using Spleeter
    output_path = 'output/'
    os.makedirs(output_path, exist_ok=True)
    separator.separate_to_file(file_path, output_path)

    # Return the paths to the separated components
    return {
        'vocals_path': f'{output_path}audio_example/vocals.wav',
        'accompaniment_path': f'{output_path}audio_example/accompaniment.wav'
    }