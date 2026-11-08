import json,subprocess,sys,os
key,talk,img,mom,out=sys.argv[1:6]
st={x['key']:x for x in json.load(open('batch/stories.json'))}[key]
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
d1=round(dur(mom)+0.7,2); fr=int(d1*30)
open('/tmp/c1.txt','w').write(st['caption']); open('/tmp/c2.txt','w').write(st['baby'].upper())
fs=lambda t:min(74,int(960/(0.7*len(t))))
dt=lambda t,y,n=74:f"drawtext=fontfile={F}:textfile={t}:fontsize={n}:fontcolor=white:borderw=6:bordercolor=black:x=(w-tw)/2:y=h*{y}"
r=lambda *a: subprocess.run(list(a),check=True)
r("ffmpeg","-y","-v","error","-loop","1","-i",img,"-i",mom,"-filter_complex",
  f"[0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=2160:3840,zoompan=z='min(1+0.0015*on,1.25)':x='iw/2-iw/zoom/2':y='ih/3-ih/zoom/3':d={fr}:s=1080x1920:fps=30,{dt('/tmp/c1.txt',0.12,fs(st['caption']))}[v];[1]adelay=300|300,apad[a]",
  "-map","[v]","-map","[a]","-t",str(d1),"-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-ar","44100","-ac","2","/tmp/p1.mp4")
r("ffmpeg","-y","-v","error","-i",talk,"-filter_complex",
  f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,tpad=stop_mode=clone:stop_duration=1.2,{dt('/tmp/c2.txt',0.78,fs(st['baby']))}[v];[0:a]apad=pad_dur=1.2[a]",
  "-map","[v]","-map","[a]","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-ar","44100","-ac","2","/tmp/p2.mp4")
open('/tmp/l.txt','w').write("file /tmp/p1.mp4\nfile /tmp/p2.mp4\n")
r("ffmpeg","-y","-v","error","-f","concat","-safe","0","-i","/tmp/l.txt","-c","copy",out)
print(out,dur(out))
