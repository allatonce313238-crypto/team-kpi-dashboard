# Block!: braced (held), shield jolts (19-30), pushes back to the stance (41-52), holds. Frames 31-40 had white
# floor streaks from Kling, so they are skipped. 2 s x 2.
python3 ../../tools/make_apng.py "$1" . block --seq 1,19,21,23,25,27,28,29,30,41,42,43,44,45,46,47,48,50,52,60 --durs 500,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,60,60,580 --loops 2
