from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/', methods=["GET"])
def test_route():
    return "ffprobe server running: Route to http:0.0.0.0:5000/ffprobe-analyze"

@app.route('/ffprobe-analyze', methods=["POST"])
def scan_ffprobe():
    # run ffprobe script which will provide JSON object, which can be filtered
    command = "ffprobe -v quiet -print_format json -show_format -show_streams " +   request.json["url"]
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # print out errors if script fials to run 

    if(error):
        print(error)

    json_obj = json.loads(output)
    
    audio_data = analyze_ports(json_obj)
    video_data = analyse_video_code(json_obj)

    # combine audio channels and video data into one object dir
    audio_data.update(video_data)
    data = audio_data

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

def analyse_video_code(json):
    streams = json["streams"]
    dict_data = {}
    for item in streams:
        if(item["codec_type"] == "video"):
            dict_data = item
    return dict_data


app.run(host='0.0.0.0', port=5000)
