from flask import Flask, render_template, request, jsonify, send_file
import os
import yt_dlp

app = Flask(__name__)

# مجلد حفظ الفيديوهات
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"success": False, "error": "No URL provided!"})

    try:
        ydl_opts = {
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "format": "best",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(info)

        return jsonify({"success": True, "path": f"/download_file/{os.path.basename(video_path)}"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/download_file/<filename>")
def download_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
