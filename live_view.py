"""
live_view.py — Live Screen View Module
=======================================
Cloudflare Quick Tunnel + JS-snapshot HTTP server.

NO credentials needed — uses Cloudflare Quick Tunnels (trycloudflare.com).

How it works:
  1. Start a lightweight HTTP server on LIVE_STREAM_PORT (default 8765).
  2. Run cloudflared.exe --url http://localhost:<port> --protocol http2
     → cloudflared prints a random public URL: https://abc-xyz.trycloudflare.com
  3. Register {unique_id, username, tunnel_url, ...} to GitHub ONCE at startup.
  4. Viewers open the tunnel URL — browser shows a JS snapshot poller (~2 fps).
  5. cloudflared.exe must already exist in app_dir (no auto-download).

Public API
----------
    import live_view

    live_view.configure(
        username, unique_id, app_dir,
        api_base_url, repo, github_token, branch,
    )
    live_view.start_live_view_server()   # blocking — run in a daemon thread
"""

import os
import re
import sys
import json
import time
import base64
import logging
import secrets
import threading
import subprocess
from io import BytesIO
from datetime import datetime
from urllib.parse import parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

import requests
import pyautogui

# ── Tunable constants ─────────────────────────────────────────────────────────────

LIVE_STREAM_FPS_INTERVAL = 0.5   # seconds between snapshot captures (server-side)
LIVE_STREAM_PORT = 8765          # fixed port — change here if already in use

# ── Runtime context (injected via configure()) ────────────────────────────────────

_username = ""
_unique_id = ""
_app_dir = ""
_api_base_url = ""
_repo = ""
_github_token = ""
_branch = ""

live_stream_active = True   # set to False only on shutdown
_cf_process = None          # cloudflared subprocess handle
_tunnel_active = False      # True only while cloudflared is running
_session_token = ""         # random token issued after successful login
_live_port = None           # port the HTTP server is bound to (set in start_live_view_server)
COMMAND_POLL_INTERVAL = 15  # seconds between command file checks


def configure(username, unique_id, app_dir, api_base_url, repo, github_token, branch):
    """
    Inject runtime context from the main script.
    Must be called once before start_live_view_server().
    """
    global _username, _unique_id, _app_dir, _api_base_url, _repo, _github_token, _branch
    global _session_token
    _username = username
    _unique_id = unique_id
    _app_dir = app_dir
    _api_base_url = api_base_url
    _repo = repo
    _github_token = github_token
    _branch = branch
    _session_token = secrets.token_hex(32)  # fresh token each run


# ── HTTP request handler ──────────────────────────────────────────────────────────

class _SnapshotHandler(BaseHTTPRequestHandler):
    """
    Routes:
      GET  /login      → access-key login form
      POST /login      → validate access key, set session cookie
      GET  /           → HTML viewer (JS snapshot poller)  [auth required]
      GET  /snapshot   → single JPEG frame                 [auth required]
      GET  /stream     → MJPEG multipart stream            [auth required]
      GET  /status     → JSON status                       [auth required]
    """

    # ── auth helpers ──────────────────────────────────────────────────────────────

    def _is_authenticated(self):
        """Return True if the request carries a valid session cookie."""
        raw = self.headers.get("Cookie", "")
        for part in raw.split(";"):
            name, _, value = part.strip().partition("=")
            if name.strip() == "lv_session" and value.strip() == _session_token:
                return True
        return False

    def _redirect_to_login(self, error=False):
        dest = "/login?error=1" if error else "/login"
        self.send_response(302)
        self.send_header("Location", dest)
        self.end_headers()

    # ── routing ───────────────────────────────────────────────────────────────────

    def do_GET(self):
        path = self.path.split("?")[0]   # strip query string
        if path == "/login":
            error = "error=1" in self.path
            self._serve_login(error=error)
            return
        if path == "/status":   # status is public — no auth needed
            self._serve_status()
            return
        if not self._is_authenticated():
            self._redirect_to_login()
            return
        if path in ("/", ""):
            if not _tunnel_active:
                self._serve_paused()
            else:
                self._serve_html()
        elif path == "/snapshot":
            if not _tunnel_active:
                self._serve_503()
            else:
                self._serve_snapshot()
        elif path == "/stream":
            if not _tunnel_active:
                self._serve_503()
            else:
                self._serve_mjpeg()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

    def do_POST(self):
        path = self.path.split("?")[0]
        if path != "/login":
            self.send_response(405)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode(errors="replace")
        params = parse_qs(body)
        entered = params.get("access_key", [""])[0]
        if entered == _username:
            # Correct — set session cookie and redirect to viewer
            cookie = (
                f"lv_session={_session_token}; "
                "Path=/; HttpOnly; SameSite=Strict"
            )
            self.send_response(302)
            self.send_header("Set-Cookie", cookie)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            self._redirect_to_login(error=True)

    # ── login page ────────────────────────────────────────────────────────────────

    def _serve_login(self, error=False):
        error_html = (
            '<p class="err">Incorrect access key. Try again.</p>' if error else ""
        )
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Live View &#8211; Access Required</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #111; color: #e0e0e0; font-family: 'Segoe UI', sans-serif;
            display: flex; align-items: center; justify-content: center;
            min-height: 100vh; }}
    .card {{ background: #1e1e1e; border: 1px solid #333; border-radius: 12px;
             padding: 40px 36px; width: 340px; text-align: center; }}
    .lock {{ font-size: 2.4rem; margin-bottom: 16px; }}
    h2 {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 6px; color: #fff; }}
    p.sub {{ font-size: 0.78rem; color: #777; margin-bottom: 24px; }}
    input {{ width: 100%; padding: 10px 14px; border-radius: 8px;
             border: 1px solid #444; background: #2a2a2a; color: #fff;
             font-size: 0.95rem; outline: none; }}
    input:focus {{ border-color: #4ade80; }}
    button {{ margin-top: 14px; width: 100%; padding: 10px;
              border-radius: 8px; border: none; background: #16a34a;
              color: #fff; font-size: 0.95rem; cursor: pointer; }}
    button:hover {{ background: #15803d; }}
    p.err {{ margin-top: 14px; font-size: 0.78rem; color: #f87171; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="lock">&#128274;</div>
    <h2>Screen View Access</h2>
    <p class="sub">Enter the access key to continue</p>
    <form method="POST" action="/login">
      <input type="password" name="access_key" placeholder="Access key"
             autofocus autocomplete="off" />
      <button type="submit">Unlock</button>
    </form>
    {error_html}
  </div>
</body>
</html>""".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(html)

    # ── Paused / 503 helpers ──────────────────────────────────────────────────────

    def _serve_paused(self):
        """HTML page shown at / when streaming has not been started yet."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Live View &#8211; Paused</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #111; color: #e0e0e0; font-family: 'Segoe UI', sans-serif;
            display: flex; align-items: center; justify-content: center;
            min-height: 100vh; }}
    .card {{ background: #1e1e1e; border: 1px solid #333; border-radius: 12px;
             padding: 40px 36px; width: 380px; text-align: center; }}
    .icon {{ font-size: 2.8rem; margin-bottom: 16px; }}
    h2 {{ font-size: 1.1rem; font-weight: 600; color: #fff; margin-bottom: 8px; }}
    p  {{ font-size: 0.82rem; color: #777; line-height: 1.6; }}
    .uid {{ font-size: 0.7rem; color: #555; font-family: monospace; margin-top: 18px; }}
    .refresh {{ margin-top: 20px; display: inline-block; padding: 9px 22px;
                border-radius: 8px; background: #1f2937; color: #9ca3af;
                font-size: 0.85rem; cursor: pointer; border: 1px solid #374151;
                text-decoration: none; }}
    .refresh:hover {{ background: #374151; }}
  </style>
  <meta http-equiv="refresh" content="15">
</head>
<body>
  <div class="card">
    <div class="icon">&#9208;&#65039;</div>
    <h2>Streaming not active</h2>
    <p>The viewer has not started the stream yet.<br>
       Click <strong>&#9654; Start Stream</strong> in the Streamlit viewer,<br>
       then reload or wait — this page auto-refreshes every 15&thinsp;s.</p>
    <div class="uid">{_unique_id}</div>
    <a class="refresh" href="/">&#8635;&ensp;Refresh now</a>
  </div>
</body>
</html>""".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(html)

    def _serve_503(self):
        """Return 503 when snapshot/stream is requested but streaming is paused."""
        body = b"Streaming not active"
        self.send_response(503)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Retry-After", "15")
        self.end_headers()
        self.wfile.write(body)

    # ── HTML viewer ───────────────────────────────────────────────────────────────

    def _serve_html(self):
        """Serve a self-contained HTML page that polls /snapshot every 500 ms."""
        username = _username
        unique_id = _unique_id
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Live View \u2013 {username}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #111; color: #e0e0e0; font-family: 'Segoe UI', sans-serif;
            display: flex; flex-direction: column; align-items: center;
            min-height: 100vh; padding: 16px; }}
    header {{ width: 100%; max-width: 1300px; display: flex; align-items: center;
              justify-content: space-between; padding: 8px 0 14px; }}
    header h1 {{ font-size: 1.1rem; font-weight: 600; color: #fff; }}
    .badge {{ background: #16a34a; color: #fff; font-size: 0.75rem;
              padding: 3px 10px; border-radius: 99px; }}
    .uuid  {{ font-size: 0.72rem; color: #888; font-family: monospace; }}
    #frame-wrap {{ width: 100%; max-width: 1300px; border-radius: 8px;
                   overflow: hidden; background: #000;
                   box-shadow: 0 4px 32px rgba(0,0,0,.6); }}
    #frame-wrap img {{ width: 100%; display: block; }}
    footer {{ margin-top: 12px; font-size: 0.7rem; color: #555; }}
    #ts  {{ color: #4ade80; }}
    #fps {{ color: #888; margin-left: 8px; }}
  </style>
</head>
<body>
  <header>
    <h1>\U0001f5a5\ufe0f &nbsp;{username}</h1>
    <span class="badge">\u25cf LIVE</span>
    <span class="uuid">UUID: {unique_id}</span>
  </header>
  <div id="frame-wrap">
    <img id="frame" src="/snapshot" alt="Live screen of {username}" />
  </div>
  <footer>Started &nbsp;\u00b7&nbsp; <span id="ts"></span><span id="fps"></span></footer>
  <script>
    document.getElementById('ts').textContent = new Date().toLocaleTimeString();
    const img = document.getElementById('frame');
    let errors = 0, frames = 0, last = Date.now();
    function loadNext() {{
      const next = new Image();
      next.onload = function() {{
        img.src = next.src;
        errors = 0;
        frames++;
        if (frames % 10 === 0) {{
          const now = Date.now();
          const fps = (10000 / (now - last)).toFixed(1);
          last = now;
          document.getElementById('fps').textContent = ' \u00b7 ' + fps + ' fps';
        }}
        setTimeout(loadNext, 500);
      }};
      next.onerror = function() {{
        errors++;
        setTimeout(loadNext, Math.min(500 * errors, 5000));
      }};
      next.src = '/snapshot?' + Date.now();
    }}
    loadNext();
  </script>
</body>
</html>""".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(html)

    # ── Single JPEG snapshot ──────────────────────────────────────────────────────

    def _serve_snapshot(self):
        frame = _capture_jpeg()
        self.send_response(200)
        self.send_header("Content-Type", "image/jpeg")
        self.send_header("Content-Length", str(len(frame)))
        self.send_header("Cache-Control", "no-cache, no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(frame)

    # ── MJPEG stream (works over localhost, breaks through Cloudflare proxy) ──────

    def _serve_mjpeg(self):
        self.send_response(200)
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        while live_stream_active:
            try:
                frame = _capture_jpeg()
                self.wfile.write(
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n"
                    + f"Content-Length: {len(frame)}\r\n\r\n".encode()
                    + frame
                    + b"\r\n"
                )
                self.wfile.flush()
                time.sleep(LIVE_STREAM_FPS_INTERVAL)
            except (BrokenPipeError, ConnectionResetError):
                break
            except Exception as e:
                logging.error(f"[LiveView] MJPEG write error: {e}")
                break

    # ── JSON status ───────────────────────────────────────────────────────────────

    def _serve_status(self):
        body = json.dumps({
            "unique_id": _unique_id,
            "username": _username,
            "timestamp": datetime.now().isoformat(),
            "streaming": _tunnel_active,
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # suppress per-request access logs


class _ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle each viewer connection in its own thread."""
    daemon_threads = True


# ── Screen capture ────────────────────────────────────────────────────────────────

def _capture_jpeg(max_w=1280, quality=65):
    """Capture the full screen, resize to max_w wide, return JPEG bytes."""
    img = pyautogui.screenshot()
    if img.width > max_w:
        img = img.resize((max_w, int(img.height * max_w / img.width)))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue()


# ── cloudflared management ────────────────────────────────────────────────────────

def _get_cloudflared():
    """
    Return path to cloudflared.exe.
    When running as a frozen PyInstaller exe, PyInstaller extracts bundled
    binaries to sys._MEIPASS — check there first.
    Falls back to app_dir for running as a plain script.
    """
    # Frozen exe: PyInstaller extracts cloudflared.exe to a temp _MEIPASS folder
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidate = os.path.join(meipass, "cloudflared.exe")
        if os.path.exists(candidate):
            return candidate
    # Script mode or manual placement next to the exe
    path = os.path.join(_app_dir, "cloudflared.exe")
    if not os.path.exists(path):
        logging.error(f"[LiveView] cloudflared.exe not found at {path}")
        print(f"[LiveView] cloudflared.exe not found at {path} — place it there and restart.")
        return None
    return path


def _start_cloudflared(port):
    """
    Launch a Cloudflare Quick Tunnel for http://localhost:{port}.
    Blocks up to 30 s waiting for cloudflared to print the public URL.
    Returns (tunnel_url, process) or (None, None) on failure.
    """
    global _cf_process
    cf = _get_cloudflared()
    if not cf:
        return None, None
    try:
        proc = subprocess.Popen(
            [cf, "tunnel", "--url", f"http://localhost:{port}",
             "--protocol", "http2", "--no-autoupdate"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        _cf_process = proc
        url_re = re.compile(r"https://[a-z0-9\-]+\.trycloudflare\.com")
        deadline = time.time() + 30
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue
            m = url_re.search(line)
            if m:
                return m.group(0), proc
        logging.error("[LiveView] cloudflared did not emit a URL within 30 s.")
        return None, proc
    except Exception as e:
        logging.error(f"[LiveView] cloudflared start error: {e}")
        return None, None


# ── GitHub registry (single write per session) ────────────────────────────────────

def _registry_put(info: dict):
    """Write (or overwrite) the tunnel registry entry for this device to GitHub."""
    try:
        path = f"uploads/live/{_username+'_'+_unique_id}/tunnel.json"
        file_url = f"{_api_base_url}/repos/{_repo}/contents/{path}"
        headers = {
            "Authorization": f"token {_github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        sha = None
        try:
            r = requests.get(file_url, headers=headers, timeout=10)
            if r.status_code == 200:
                sha = r.json().get("sha")
        except Exception:
            pass
        payload = {
            "message": f"live register {_unique_id}",
            "content": base64.b64encode(json.dumps(info, indent=2).encode()).decode(),
            "branch": _branch,
        }
        if sha:
            payload["sha"] = sha
        requests.put(file_url, headers=headers, json=payload, timeout=15)
    except Exception as e:
        logging.error(f"[LiveView] Registry write error: {e}")


def _register_tunnel(tunnel_url):
    """Write tunnel URL + device info to the GitHub registry (streaming=True)."""
    info = {
        "unique_id": _unique_id,
        "username": _username,
        "tunnel_url": tunnel_url,
        "stream_url": f"{tunnel_url}/stream",
        "snapshot_url": f"{tunnel_url}/snapshot",
        "status_url": f"{tunnel_url}/status",
        "timestamp": datetime.now().isoformat(),
        "online": True,
        "streaming": True,
    }
    _registry_put(info)
    logging.info(f"[LiveView] Stream live at {tunnel_url}/stream")
    print(f"[LiveView] Stream live at {tunnel_url}/stream")


def _register_idle():
    """Register device as online but not streaming (no tunnel URL)."""
    info = {
        "unique_id": _unique_id,
        "username": _username,
        "tunnel_url": "",
        "stream_url": "",
        "snapshot_url": "",
        "status_url": "",
        "timestamp": datetime.now().isoformat(),
        "online": True,
        "streaming": False,
    }
    _registry_put(info)
    logging.info("[LiveView] Device registered as idle (streaming=False).")
    print("[LiveView] Device registered as idle — waiting for start_stream command.")


def _dir_name():
    """GitHub folder name for this device: uploads/live/{username}_{unique_id}"""
    return f"{_username}_{_unique_id}"


def _command_path():
    return f"uploads/live/{_dir_name()}/command.json"


def _read_command():
    """Read command.json from GitHub. Returns dict or None."""
    try:
        file_url = f"{_api_base_url}/repos/{_repo}/contents/{_command_path()}"
        headers = {
            "Authorization": f"token {_github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        r = requests.get(file_url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return json.loads(base64.b64decode(data["content"]).decode()), data.get("sha")
    except Exception as e:
        logging.error(f"[LiveView] Command read error: {e}")
    return None, None


def _delete_command(sha):
    """Delete command.json from GitHub after processing."""
    try:
        file_url = f"{_api_base_url}/repos/{_repo}/contents/{_command_path()}"
        headers = {
            "Authorization": f"token {_github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        requests.delete(file_url, headers=headers, json={
            "message": f"[LiveView] cleared command {_unique_id}",
            "sha": sha,
            "branch": _branch,
        }, timeout=10)
    except Exception as e:
        logging.error(f"[LiveView] Command delete error: {e}")


def _stop_cloudflared():
    """Terminate the running cloudflared process, if any."""
    global _cf_process, _tunnel_active
    if _cf_process:
        try:
            _cf_process.terminate()
            _cf_process.wait(timeout=5)
        except Exception:
            pass
        _cf_process = None
    _tunnel_active = False


def _poll_and_handle_commands():
    """
    Background thread: check GitHub every COMMAND_POLL_INTERVAL seconds.
    Supported commands:
      start_stream      — start cloudflared and register the tunnel URL.
      stop_stream       — kill cloudflared and mark device as idle.
      regenerate_tunnel — kill old tunnel and start a new one (when URL is broken).
    """
    global _tunnel_active
    while live_stream_active:
        try:
            cmd, sha = _read_command()
            if cmd:
                action = cmd.get("action", "")

                if action == "start_stream":
                    logging.info("[LiveView] start_stream command received.")
                    print("[LiveView] start_stream command received.")
                    _delete_command(sha)
                    if _tunnel_active:
                        logging.info("[LiveView] Tunnel already active — ignored.")
                    else:
                        port = _live_port or LIVE_STREAM_PORT
                        url, _ = _start_cloudflared(port)
                        if url:
                            _tunnel_active = True
                            _register_tunnel(url)
                        else:
                            logging.error("[LiveView] start_stream: tunnel failed.")
                            print("[LiveView] start_stream: tunnel failed — no URL returned.")

                elif action == "stop_stream":
                    logging.info("[LiveView] stop_stream command received.")
                    print("[LiveView] stop_stream command received.")
                    _delete_command(sha)
                    _stop_cloudflared()
                    _register_idle()

                elif action == "regenerate_tunnel":
                    logging.info("[LiveView] regenerate_tunnel command received.")
                    print("[LiveView] regenerate_tunnel command received.")
                    _delete_command(sha)
                    _stop_cloudflared()
                    port = _live_port or LIVE_STREAM_PORT
                    url, _ = _start_cloudflared(port)
                    if url:
                        _tunnel_active = True
                        _register_tunnel(url)
                        logging.info(f"[LiveView] New tunnel registered: {url}")
                        print(f"[LiveView] New tunnel registered: {url}")
                    else:
                        logging.error("[LiveView] Tunnel regeneration failed — no URL returned.")
                        print("[LiveView] Tunnel regeneration failed.")

        except Exception as e:
            logging.error(f"[LiveView] Command poll error: {e}")
        time.sleep(COMMAND_POLL_INTERVAL)


def _unregister_tunnel():
    """Mark device as offline in the GitHub registry on shutdown."""
    try:
        path = f"uploads/live/{_username+'_'+_unique_id}/tunnel.json"
        file_url = f"{_api_base_url}/repos/{_repo}/contents/{path}"
        headers = {
            "Authorization": f"token {_github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        r = requests.get(file_url, headers=headers, timeout=10)
        if r.status_code != 200:
            return
        data = r.json()
        info = json.loads(base64.b64decode(data["content"]).decode())
        info["online"] = False
        info["streaming"] = False
        info["timestamp"] = datetime.now().isoformat()
        requests.put(file_url, headers=headers, json={
            "message": f"live offline {_unique_id}",
            "content": base64.b64encode(json.dumps(info, indent=2).encode()).decode(),
            "branch": _branch,
            "sha": data["sha"],
        }, timeout=15)
    except Exception as e:
        logging.error(f"[LiveView] Unregister error: {e}")


# ── Entry point ───────────────────────────────────────────────────────────────────

def start_live_view_server():
    """
    Start the HTTP server on LIVE_STREAM_PORT, launch a Cloudflare Quick Tunnel,
    and register the public URL to GitHub.

    This function blocks — run it inside a daemon thread:
        threading.Thread(target=live_view.start_live_view_server, daemon=True).start()

    Call configure() before starting the thread.
    """
    global live_stream_active, _live_port

    port = LIVE_STREAM_PORT
    _live_port = port
    server = _ThreadedHTTPServer(("127.0.0.1", port), _SnapshotHandler)
    logging.info(f"[LiveView] Server listening on localhost:{port}")
    print(f"[LiveView] Server listening on localhost:{port}")

    # Register as idle — cloudflared will only start when viewer sends start_stream
    threading.Thread(target=_register_idle, daemon=True).start()
    threading.Thread(target=_poll_and_handle_commands, daemon=True).start()

    try:
        server.serve_forever()
    finally:
        live_stream_active = False
        _unregister_tunnel()
        if _cf_process:
            _cf_process.terminate()
