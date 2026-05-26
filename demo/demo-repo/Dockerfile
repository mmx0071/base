# 基线镜像：Ubuntu，不含 tree。PR 侧在该文件增加一行安装 tree 即可形成可辨差异。
FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY serve.py /app/serve.py

EXPOSE 8080
CMD ["python3", "/app/serve.py"]
