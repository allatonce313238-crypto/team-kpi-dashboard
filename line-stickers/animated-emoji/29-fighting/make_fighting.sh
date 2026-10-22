# Fighting!: punches the bag (whole clip; 73 matches 1). Kling also pulled the camera back a little while punching
# (frames 10-60), so it reads as a quick zoom-out during the punches. 16 frames to stay under 300,000 bytes. 2 s x 2.
python3 ../../tools/make_apng.py "$1" . fighting --seq 1,6,10,14,19,24,28,32,37,42,46,50,55,60,64,68 --durs 125 --loops 2
