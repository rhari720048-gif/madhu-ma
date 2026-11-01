# madhu-ma- : scroll-driven birthday film

Static site (no build step). `index.html` is the whole experience.

## Structure
- `index.html`      curtain -> question -> date rewind -> sunrise -> messages -> story video -> cat question gates
- `frames/`         sun_###.webp (sunrise), story_###.webp (desktop 1440px, 12fps), m_###.webp (phone portrait 608x1080)
- `cat/`            cat clips (14 actions, 24fps) + front.png
- `vercel.json`     long cache headers for frames/cat
- `tools/catgen/`   Python generator for the cat clips (pip install -r requirements.txt)
- `assets/refs/`    face crops, uniform, college, jhumka references for Flow prompts
- `docs/`           story timeline, Flow prompt

## Deploy (Vercel)
Import the repo, Framework = Other, leave build/output empty, Deploy.

## Edit the questions
Search `QUESTIONS=[` in `index.html`. Each gate has `at:atOf(seconds)`, `ask` clip, text `q`, answer logic `f`.
Story seconds: 0:06 earring, 0:22 song, 0:24 college, 0:32 cake.

## Regenerate cat clips
`python tools/catgen/run.py idle,ask1,happy` writes into `cat/<clip>/NNN.webp` (definitions in tools/catgen/clips.py).
