# Blow kiss v2: redrawn in ChatGPT from blow-kiss-sprite-sheet.png -> chatgpt-redraw-sheet.png (5 x 4 grid).
# Cells were cut at the detected gutters, green removed (speck filter 40 px for the small hearts), and each
# frame shifted (a few px) so Max's body lines up with frame 1. 20 frames in order, 2 s x 2.
python3 ../../tools/make_apng.py "$1" . blow-kiss --seq 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 --durs 100 --loops 2
