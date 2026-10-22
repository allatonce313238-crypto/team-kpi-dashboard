# Surprised: holds the shocked pose, jolts backwards (1->12) and springs back (54->63).
# Kling's middle frames (13-53) shrink him far away and smear, so they are skipped; 12 and 54 are the same size.
python3 ../../tools/make_apng.py "$1" . surprised --seq 1,10,11,12,54,56,58,60,62,63 --durs 500,50,50,60,50,50,50,50,50,90 --loops 4
