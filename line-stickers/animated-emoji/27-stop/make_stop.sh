# Stop!: palm out (held; frames 1-22 jitter, so one is held), turns and points at the sign (27-40), holds. 13 frames to stay under 300,000 bytes. 2 s x 2.
python3 ../../tools/make_apng.py "$1" . stop --seq 22,27,29,31,33,35,37,39,40,44,52,62,73 --durs 500,75,75,75,75,75,75,75,75,225,225,225,225 --loops 2
