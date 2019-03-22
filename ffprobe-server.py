from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)


@app.route('/ffprobe-analyze', methods=["POST"])
def scan_ffprobe():
    # run ffprobe script
    command = "ffprobe -v quiet -print_format json -show_format -show_streams " +   request.json["url"]
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if(error):
        print(error)

    json_obj = json.loads(output)
    data = analyze_ports(json_obj)

    return jsonify(data)


# analyze data ffprobe output

def analyze_ports(json):
    format = json["format"]
    streams = json["streams"]
    duration = format["duration"]
    filename = format["filename"]
    audio_streams = loop_audio_channels(streams)
    dict_data = {}
    dict_data["duration"] = duration
    dict_data["filename"] = filename
    dict_data["audio_streams"] = audio_streams
    return dict_data


def loop_audio_channels(list):
    audio_channels = []
    count = 0
    for item in list:
        if(item["codec_type"] == "audio"):
            audio_channels.append(count)
        count = count + 1
    return audio_channels


app.run(host='0.0.0.0', port=9000)
