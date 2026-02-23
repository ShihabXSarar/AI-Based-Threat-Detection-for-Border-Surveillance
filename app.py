"""
Legacy entry-point preserved for compatibility.
The heavy lifting now lives inside the falcon_ai package.
"""
import os

from falcon_ai import create_app
from falcon_ai.app.core import load_model, start_processing_thread
from falcon_ai.config import Config


app = create_app(Config)


def _boot_detection():
    """Load model and spin up the background analysis thread."""
    if load_model():
        start_processing_thread(Config.DEFAULT_SOURCE)
    else:
        print("⚠️ YOLO model failed to load. Start analysis via dashboard once fixed.")


if __name__ == '__main__':
    print("=" * 72)
    print("🦅 FALCON AI - BORDER DEFENSE SYSTEM (Modular Architecture)")
    print("=" * 72)
    print(f"📡 MongoDB URI: {Config.MONGO_URI}")
    print(f"📁 Uploads Directory: {os.path.abspath(Config.get_upload_path())}")
    print("=" * 72)
    _boot_detection()
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)
    print("🚀 Application started on http://127.0.0.1:5000")
    print("🔐 Login at http://127.0.0.1:5000/auth/login")
    print("🔐 Register at http://127.0.0.1:5000/auth/register")
    print("=" * 72)
    