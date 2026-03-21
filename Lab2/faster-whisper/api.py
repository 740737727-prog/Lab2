from fastapi import FastAPI, UploadFile, File, Form
from faster_whisper import WhisperModel
import os

app = FastAPI(title="Persistent ASR Transcription Service")

# 持久化加载模型（容器启动时加载一次，不重复加载）
model = WhisperModel("base", device="cpu", compute_type="int8")

# 健康检查接口
@app.get("/health")
async def health():
    return {"status": "healthy"}

# 模型列表接口
@app.get("/v1/models")
async def list_models():
    return {
        "data": [
            {"id": "faster-whisper", "object": "model", "owned_by": "local"}
        ]
    }

# 语音转写接口（兼容 OpenAI 格式）
@app.post("/v1/audio/transcriptions")
async def transcriptions(
    file: UploadFile = File(...),
    model: str = Form(...)
):
    # 保存临时音频
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # 转写
    segments, info = model.transcribe(temp_file, language="zh")
    text = "".join([seg.text for seg in segments])

    # 删除临时文件
    os.remove(temp_file)

    return {"text": text}
