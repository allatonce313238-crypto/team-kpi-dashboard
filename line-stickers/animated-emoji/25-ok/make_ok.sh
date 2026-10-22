# OK: Kling bounced fast, so sampling the whole clip looked jumpy. Uses 18 consecutive frames (30-47; 48 matches 30)
# for one smooth bounce, 1 s x 4.
python3 ../../tools/make_apng.py "$1" . ok --seq 30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47 --durs 65,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55 --loops 4
