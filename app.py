from __future__ import unicode_literals
from flask import Flask, request, send_file, jsonify
from threading import Thread

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from modules import converter
from modules import database
from modules import search


app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@limiter.limit("3 per minute")
@app.route("/convert", methods=["POST"])
def convert():
    if request.method == "POST":
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = request.environ['REMOTE_ADDR']
        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']

        link = request.args.get("uri")

        process_id = database.add_data(f"{link.split('watch?v=')[-1]}.mp3", ip)
        Thread(
            target=converter.download_mp3,
            args=(link, process_id, )
            ).start()

        return jsonify({
            "process_id": process_id,
            "is_limited": False
            })


@app.route("/check_status", methods=["GET"])
def check_status():
    process_id = request.args.get("process_id")
    g = database.check_status(process_id)

    return jsonify({
            "status": bool(g[0]),
            "process_id": process_id,
            "is_limited": False
        })


@app.route("/download", methods=["GET"])
def download():
    process_id = request.args.get("process_id")

    return send_file(
        f"downloads/{database.download(process_id)[0]}",
        as_attachment=True
        )


@app.route("/search", methods=["GET"])
def search_app():
    query = request.args.get("q")
    limit = request.args.get("l")

    return jsonify({
        "result": search.video_search(query, limit),
        "is_limited": False
        })


@app.route("/video_info", methods=["GET"])
def get_video_info():
    uri = request.args.get("uri")

    return jsonify(search.video_info(uri))


@app.route("/channel_info", methods=["GET"])
def get_channel_info():
    name = request.args.get("name")

    return jsonify(search.channel_info(name))


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "is_limited": True
        })


if __name__ == "__main__":
    app.run(debug=False)
