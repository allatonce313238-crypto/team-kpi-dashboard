# MawKorn LINE Emoji — handoff plan

New chat? Read this whole file first, then continue from **Status** below.

## The project

- Second character set in the **Fluffy Party** series, after Mx (`line-stickers/animated-emoji/`, finished and packaged in `line-stickers/line-emoji-upload.zip`).
- Character: **Mangkorn**, a chibi red fluffy dragon. Public name: **MawKorn** (use MawKorn in anything public: titles, descriptions, file names).
- Title idea: "Fluffy Party: MawKorn Emoji Vol.1" (not confirmed yet).
- Target: **40 animated LINE emoji** (the user may still cut it down; LINE allows 8–40).
- Branch: `claude/line-stickers-bg-dicut-302vim` in `allatonce313238-crypto/team-kpi-dashboard`. Put the work in `line-stickers/mawkorn/`, one folder per emoji (`01-hello/`, …) like Mx.

## Status (2026-10-22)

- Emoji list agreed (below), except Good night: style **A or B not chosen**.
- The user wanted to see a pajamas sample first (Good night B). A ChatGPT keyframe prompt was given (see **Good night B prompt**); waiting for their image.
- Notion tracker created and **empty**: add rows only when the user says so.
- No Kling video made yet. Kling balance: **298 credits** (40 videos need about 720 at 18 each).

## Rules from the user (follow every time)

1. **Never send anything to Kling without an explicit "go".** Every job costs credits.
2. **Never change Notion until the user says so.** (Showing a prompt is not permission to save it.)
3. Put every prompt in a code block so it can be copied.
4. **No speech bubbles or text** in the art.
5. Every Kling prompt must include: *"Small, calm, cute movements only. His mouth stays the same … the whole time — he does not talk, his mouth does not open and close."*
6. Do not assume. If unsure, ask.
7. Reference images can be pointed to by GitHub path; the user's ChatGPT is connected to this repo.
8. The user sometimes types English on a Thai keyboard (e.g. "ฟยยพนอำ" = "approve").

## Workflow per emoji

1. **ChatGPT keyframe**: I write the prompt; the user makes the image in ChatGPT and sends it. Pure green (#00FF00) background, no outline, no text.
2. I review it, save it as `NN-name/kling-start.png` (and `kling-end.png` if the pose changes) and push it.
3. **Kling** (only after "go"): `mcp__Kling__image_to_video`, model `kling-video-v3_0` (18 credits),
   arguments `duration=3`, `resolution=720p`, `imageCount=1`, `prefer_multi_shots=false`, `enable_audio=false`,
   inputs `first_image` (+ `tail_image`; same image for a seamless loop, or an end pose).
   Use `raw.githubusercontent.com/.../<commit SHA>/...` URLs pinned to a commit. New `taskTraceId` UUID per job.
   Poll `query_tasks`, download `urlWithoutWatermark` to `NN-name/kling-video.mp4`.
4. **Frames + green removal**:
   `ffmpeg -v error -y -i NN-name/kling-video.mp4 RAW/%03d.png`
   `python3 -I line-stickers/tools/chroma_key.py RAW KEY [40]`
5. **APNG**: `python3 line-stickers/tools/make_apng.py KEY NN-name name --seq a,b,c --durs N --loops L`
   (save the exact command in a `make_name.sh` in the folder). Send the preview to the user.
6. User approves → update Notion (only then).

### LINE rules (check every file)
180×180 APNG, 5–20 frames, total play time a whole number of seconds and ≤ 4 s, 1–4 loops, ≤ 300,000 bytes, transparent background. Tab image 96×74. Too big → fewer frames.

### Lessons from the Mx set
- Kling 3.0 (18) is enough; Turbo cost 24.
- Kling often glitches mid-clip (stretched arms, jittery legs, smears): fix by choosing frames, not by re-running.
- Overlays (speed lines, ???, sparkles) can be added in code, but the user prefers effects drawn by Kling/ChatGPT when they look cuter.
- Friend dolls for collabs: round blob plush, dot eyes, no mouth (see `animated-emoji/16-hug/kling-start.png`).

## References

- `line-stickers/full-res/08.png`: MawKorn standing ("Fighting!" sticker), the main design reference.
- `line-stickers/full-res/07.png`: MawKorn sleeping, curled in his wings.
- `line-stickers/animated-emoji/33-mangkorn-pile/kling-start.png`: MawKorn doll version (used in Mx's set).
- Mx's equivalents for each emoji: `line-stickers/animated-emoji/NN-name/`.
- Design: red scales with cream fluffy fur, dark curved horns with gold bands, gold crown with a red gem, red wings with gold edges, fluffy tail with gold spikes, big amber eyes, small fangs.

## Notion

- Tracker: **MawKorn LINE Emoji Tracker**, https://app.notion.com/p/37112121a4ac4581b565dd8255e58921
- Data source: `collection://1ad18b1b-1b13-4f08-8c6b-cf7f0910d780`
- Columns: Emoji, No., Status (Prompt ready / Video generated / APNG done / Approved), Motion, Overlay (added in code), Frames, Kling prompt, Credits used, Notes, ChatGPT keyframe prompt, Keyframe attachments.
- Mx's tracker for comparison: `collection://f785401b-9254-4664-8560-5788320125f6`.

## The 40 emoji (agreed; numbers = LINE upload order)

| No. | Emoji | MawKorn's version |
|---|---|---|
| **Daily** | | |
| 001 | Hello | Waves one clawed paw, wings flap a little |
| 002 | Good morning | Big stretch with wings spread wide, small yawn |
| 003 | Good night | **A:** curls up on his tail, wings wrapped like a blanket, zZ · **B:** pajamas + nightcap + pillow like Mx. *Not chosen yet* |
| 004 | On my way! | Flies forward, wings beating fast, speed lines |
| 005 | Working | Little desk, claws tapping a laptop |
| 006 | Coffee break | Warms his mug with a tiny puff of fire, then sips |
| 007 | Eating | Munches a roast drumstick, happy cheeks |
| 008 | Thinking | Taps his chin, tail tip curling |
| **Replies** | | |
| 009 | OK | Holds up a red O sign |
| 010 | No | Holds up a blue X sign, gentle head shake |
| 011 | Thank you | Bows, paw on chest, wings folded |
| 012 | Sorry | Bows low, ears and wings drooping |
| 013 | Please | Paws together, big shiny eyes |
| 014 | Good job | Claw-up thumbs up, wink |
| 015 | Roger | Salute, tail stiff |
| 016 | Stop! | **No sign.** One paw held out in a stop pose, gentle head shake |
| **Happy & love** | | |
| 017 | Love | Makes a heart with his tail and paws |
| 018 | Blow kiss | Blows a kiss that becomes a heart-shaped puff of fire |
| 019 | Shy | Hides behind his own wing, peeking |
| 020 | LOL | **Plops down sitting, bursts out laughing, points one claw forward** |
| 021 | Excited | Hops with wings flapping, sparkle eyes |
| 022 | Happy dance | Sways side to side, tail wiggles |
| 023 | Congrats | Jumps with confetti in mid-air |
| 024 | Proud | Chest out, wings spread, small smoke puff from the nose |
| 025 | Sly smirk | Close-up, half-closed eyes, smoke curl from one nostril |
| **Surprised, sad & upset** | | |
| 026 | Surprised | Jumps back, crown pops up |
| 027 | Confused | Head tilt, ? → ?? → ??? |
| 028 | Sad | Sits slumped, wings drooping |
| 029 | Crying | Big tears, tiny sobbing smoke puffs |
| 030 | Tired | Lies flat, slow breathing |
| 031 | Scared | Hides inside his wings, shaking |
| 032 | Disgusted | Pokes a censored thing with a stick |
| 033 | Angry | Stomps, small burst of fire, steam from the ears |
| **Dragon action** | | |
| 034 | Fighting! | Fists up, breathes fire (like `full-res/08.png`) |
| 035 | Fire breath | Deep breath, then a big puff of fire |
| **Collab** (friends as small dolls) | | |
| 036 | Hug | Hugs a small Mx doll |
| 037–040 | TBD | One each with Lcky, Namwan, I Ploii and Earth dolls; ideas to decide with the user |

If the user goes back to a **16-emoji** set, the last discussed list was: Hello, On my way!, OK, No, Thank you, Sorry, Please, Love, LOL, Excited, Surprised, Crying, Angry, Fighting!, Tired, + 1 open slot (Hug with Mx doll or Good night). They did not want Good morning or Good night in the 16.

## Good night B prompt (given to the user, waiting for their image)

```
Use the images from my GitHub repo allatonce313238-crypto/team-kpi-dashboard, branch claude/line-stickers-bg-dicut-302vim:
- line-stickers/full-res/08.png and line-stickers/full-res/07.png = the character, a chibi red fluffy dragon (keep his exact design: red scales with cream fluffy fur, dark curved horns with gold bands, gold crown with a red gem, red wings with gold edges, fluffy tail with gold spikes, big amber eyes).
- line-stickers/animated-emoji/07-good-night/kling-start.png = the style and idea to match (a chibi knight cat in pajamas hugging a pillow).

Draw the dragon getting ready for bed, in the same pixel-art chibi style: he wears cozy cream-and-red pajamas with tiny gold star prints and a soft nightcap that drapes between his horns (horns and crown still visible). His wings poke out through the back of the pajamas and are folded and relaxed, and his fluffy tail curls around his feet. He hugs a fluffy white pillow with both paws, eyes closed, sleepy content smile with his mouth closed, slightly leaning his cheek on the pillow.

Full body, standing, centered, facing slightly to the side. No text, no speech bubble, no "Zzz" letters. No outline or white border. Solid flat pure green background (#00FF00), no shadows on the background, no floor.
```
