# Confused: Kling 3.0 start (no ???) -> end (???). Hold empty, the three ? pop in one by one
# (~13, ~31, ~37), blink, then hold all three before the loop restarts. Speck filter 40 px keeps the small ?. 2 s x 2.
python3 ../../tools/make_apng.py "$1" . confused --seq 1,13,16,19,22,25,28,31,34,36,38,42,48,54,60,66,73 --durs 260,80,80,80,80,80,80,80,80,80,80,90,90,90,90,90,490 --loops 2
