from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]

    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    file_path = stream.download()

    # Send file as attachment
    response = send_file(file_path, as_attachment=True)

    # Remove the downloaded file after sending
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")

    return response

if __name__ == "__main__":
    # Use 0.0.0.0 so Wasmer can access it externally
    app.run(host="0.0.0.0", port=8000)
