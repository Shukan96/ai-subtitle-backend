from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tempfile, os
import whisper
from googletrans import Translator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = whisper.load_model("base")
translator = Translator()

@app.post("/api/translate")
async def translate_audio(audio: UploadFile = File(...), lang: str = Form(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name

        result = model.transcribe(tmp_path)
        os.remove(tmp_path)

        transcript = result["text"]
        translated = translator.translate(transcript, dest=lang).text

        return {"subtitle": translated}

    except Exception as e:
        return {"error": str(e)}