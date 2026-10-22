# Roger: standing (20, held), snaps the salute up (51-60), holds (61-73). 2 s x 2.
# The heel-snap (10-16) was cut at the user's request; Kling's slow middle (21-50) is skipped.
python3 ../../tools/make_apng.py "$1" . roger --seq 20,51,52,53,54,55,56,57,58,59,60,61,64,67,70,73 --durs 500,50,50,50,50,50,50,50,50,50,50,100,100,100,100,600 --loops 2
