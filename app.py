from flask import Flask,request,render_template
import google.generativeai as palm
import replicate
import os

os.environ["REPLICATE_API_TOKEN"] = "r8_6QbGlfGzbsnnYeqUJg39qJACU17Tmxj3g5Osv"

model = {
    "model": "models/chat-bison-001"
}
palm.configure(api_key="AIzaSyCCT1K99BJ1JbLwhCE7qOcQ5KOZcPJ9ZZ4")

app = Flask(__name__)

name=""
flag=1

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    global name,flag
    if flag==1:
        name = request.form.get("q")
        flag=0
    return(render_template("main.html",r=name))

@app.route("/text",methods=["GET","POST"])
def text():
    return(render_template("text.html"))

@app.route("/text_reply",methods=["GET","POST"])
def text_reply():
    q = request.form.get("q")
    r = palm.chat(**model, messages=q)
    return(render_template("text_reply.html",r=r.last))


@app.route("/image",methods=["GET","POST"])
def image():
    return(render_template("image.html"))

@app.route("/image_reply",methods=["GET","POST"])
def image_reply():
    q = request.form.get("q")
    r = replicate.run(
        "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        input={
            "prompt": q,
        }
    )
    return(render_template("image_reply.html",r=r[0]))

@app.route("/music",methods=["GET","POST"])
def music():
    return(render_template("music.html"))

@app.route("/music_reply",methods=["GET","POST"])
def music_reply():
    q = request.form.get("q")
    r = replicate.run(
        "meta/musicgen:7be0f12c54a8d033a0fbd14418c9af98962da9a86f5ff7811f9b3423a1f0b7d7",
        input={
            "prompt": q,
            "duration":5
        }
    )
    return(render_template("music_reply.html",r=r))

@app.route("/video",methods=["GET","POST"])
def video():
    return(render_template("video.html"))

@app.route("/video_reply",methods=["GET","POST"])
def video_reply():
    q = request.form.get("q")
    r = replicate.run(
        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        input={
            "prompt": q,
            "num_frames":10
        }
    )
    return(render_template("video_reply.html",r=r[0]))

@app.route("/end",methods=["GET","POST"])
def end():
    global flag
    print("for gracefully ended")
    flag=1
    return(render_template("index.html"))

if __name__ == "__main__":
    app.run()
