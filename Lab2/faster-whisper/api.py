from fastapi import FastAPI, UploadFile, File, Form
from faster_whisper import WhisperModel
import os
import uuid

app = FastAPI(title="ASR Transcription Service")

# 全局模型（不会被覆盖）
asr_model = WhisperModel("base", device="cpu", compute_type="int8")

# 健康检查
@app.get("/health")
async def health():
    return {"status": "healthy"}

# 模型列表
@app.get("/v1/models")
async def list_models():
    return {
        "data": [
            {"id": "faster-whisper", "object": "model", "owned_by": "local"}
        ]
    }

# 核心转写接口（修复重名问题！）
@app.post("/v1/audio/transcriptions")
async def transcriptions(
    file: UploadFile = File(...),
    model: str = Form(...)  # 这个是参数，不会覆盖全局模型
):
    temp_file = f"temp_{uuid.uuid4()}.wav"

    # 保存上传的音频
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # 这里用 asr_model 而不是 model！
    segments, info = asr_model.transcribe(temp_file, language="zh")
    text = "".join([seg.text for seg in segments])

    os.remove(temp_file)
    return {"text": text}
