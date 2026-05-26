#!/usr/bin/env python3
"""极简预览探针：HTTP 返回是否已安装 tree，便于肉眼区分 PR 与基线。"""
import json
import shutil
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8080


def tree_info():
    path = shutil.which("tree")
    if not path:
        return {"installed": False, "version": None}
    try:
        out = subprocess.check_output(["tree", "--version"], text=True, stderr=subprocess.STDOUT).strip()
        return {"installed": True, "version": out}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"installed": True, "version": "unknown"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        body = json.dumps(
            {
                "preview": "demo-repo",
                "base_image": "ubuntu:22.04",
                "tree": tree_info(),
            },
            indent=2,
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):  # noqa: D102
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
