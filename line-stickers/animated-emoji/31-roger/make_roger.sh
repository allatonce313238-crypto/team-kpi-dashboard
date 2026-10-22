# Roger: at ease (1, held), snaps straight (10-16), stands (20), snaps the salute up (51-60), holds (73). 2 s x 2.
# Kling did not follow the plan exactly: the salute only comes at the end, so the middle (21-50) is skipped.
python3 ../../tools/make_apng.py "$1" . roger --seq 1,10,11,12,13,14,15,16,20,51,52,53,54,55,56,57,58,59,60,73 --durs 400,40,40,40,40,40,40,40,200,40,40,40,40,40,40,40,40,40,40,720 --loops 2
