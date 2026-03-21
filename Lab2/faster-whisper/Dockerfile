#---
# name: faster-whisper
# group: audio
# depends: [ctranslate2, onnxruntime, huggingface_hub, numpy]
# requires: '>=34.1.0'
# test: test.py
# notes: Faster Whisper transcription with CTranslate2 (https://github.com/SYSTRAN/faster-whisper)
#---
#---
# name: faster-whisper-asr:fastapi
# group: audio
# depends: [python:3.10-slim, ffmpeg]
#---

FROM python:3.10-slim

ARG ASR_ROOT="/opt/asr-fastapi"
ARG ASR_MODELS="${ASR_ROOT}/models"

WORKDIR ${ASR_ROOT}

# 安装系统依赖（ffmpeg 必须）
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制代码
COPY api.py ${ASR_ROOT}/
COPY requirements.txt ${ASR_ROOT}/

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口（你要求 5092）
EXPOSE 5092

ENV PYTHONPATH="${ASR_ROOT}:$PYTHONPATH" \
    MODEL_DIR="${ASR_MODELS}"

# 启动服务（持久化，和 kokoro 一样）
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5092"]
