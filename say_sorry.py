import math as m
import random
import turtle as t
import tkinter.font as tkf

# ------------------------------------------------------------
# 100 WAYS TO SAY SORRY (Vibrant Sunset Dusk & Tiny Diamond Stars)
# ------------------------------------------------------------

TICK = 12             # ~83 FPS for ultra-smooth rotation
INTERVAL = 11         # ticks between each apology appearing
R_INNER = 128         # where the spokes start
R_MAX = 342           # where the longest spoke may end
SLIDE = 22            # slide-in distance for new spokes

# Rich Dusk & Warm Gold Theme (inspired by the video, with vibrant contrast)
BG_TOP = (0.04, 0.03, 0.11)    # Deep night indigo
BG_BOT = (0.14, 0.06, 0.16)    # Warm twilight plum
GOLD   = (0.98, 0.80, 0.42)    # Radiant warm gold
CREAM  = (1.00, 0.96, 0.90)    # Soft warm cream
MUTED  = (0.68, 0.56, 0.66)    # Dusty rose-mauve

# Vibrant gradient stops (Royal Indigo -> Violet -> Magenta Rose -> Coral -> Gold)
STOPS = [
    (0.42, 0.52, 0.86),  # Cool Indigo
    (0.60, 0.46, 0.84),  # Soft Violet
    (0.84, 0.44, 0.62),  # Dusty Rose
    (0.96, 0.55, 0.47),  # Warm Coral
    (0.84, 0.44, 0.62),  # Back through Rose
    (0.60, 0.46, 0.84),  # Back through Violet
    (0.42, 0.52, 0.86),  # Seamless return to Cool Indigo
]

PHRASES = [
    "I'm so sorry", "I was wrong", "Please forgive me",
    "I take full responsibility", "That was my mistake",
    "I should have listened", "I owe you an apology",
    "I didn't mean to hurt you", "I'm sorry I let you down", "I messed up",
    "I'm truly sorry", "I regret my words", "I was selfish",
    "I should have been there", "I'm sorry for yelling",
    "I wasn't honest", "I wasn't thinking of you",
    "I handled it badly", "I'm ashamed of how I acted", "You deserved better",
    "I broke my promise", "I'm sorry I forgot",
    "I put my pride first", "I'm sorry I didn't call", "I was unfair to you",
    "I judged too quickly", "I'm sorry I dismissed you",
    "I should have trusted you", "I'm sorry I interrupted", "I wasn't fair",
    "I made it about me", "I'm sorry I was distant",
    "I'm sorry I was late again", "I ignored what you needed",
    "I let my temper win", "I said things I didn't mean",
    "I'm sorry I made you worry", "I didn't see your side",
    "I should have asked first", "I'm sorry I stayed silent",
    "I took you for granted", "I'm sorry I was careless",
    "I hurt someone I love", "I'm sorry I broke your trust",
    "I was too proud to say it", "I'm sorry I wasn't listening",
    "I should have said it sooner", "I'm sorry it took so long",
    "I'm sorry I made excuses", "No excuses, just sorry",
    "I want to make it right", "Let me make it up to you",
    "I'm here to listen now", "I'll do better, I promise",
    "I'm learning from this", "I'll be more patient",
    "Tell me how to fix it", "I miss you, and I'm sorry",
    "You matter more than winning", "I can't lose you over this",
    "I'm sorry for the hurt", "I'm sorry for the tears",
    "I wish I could undo it", "I'd take it back if I could",
    "I'm sorry for my harsh words", "I was scared and lashed out",
    "I let stress speak for me", "I'm sorry I wasn't kind",
    "You didn't deserve that", "It was never your fault",
    "I'm sorry I blamed you", "I'm sorry I compared us",
    "I'm sorry I overreacted", "I misunderstood you",
    "I wasn't there for you", "I should have shown up",
    "I'm sorry I missed it", "I forgot what mattered",
    "I was busy, not present", "I took it out on you",
    "I'm sorry for the bad timing", "I made you feel small",
    "I'm sorry I doubted you", "I'm sorry I walked away",
    "I'm sorry I wasn't gentle", "I'm sorry I held a grudge",
    "I'm sorry I lied", "I'm sorry I hid the truth",
    "You can trust me again", "Give me another chance", "I'm ready to talk",
    "I'm sorry, and I mean it", "I'm sorry from my heart",
    "Forgive me when you can", "I'm grateful for you",
    "I love you, and I'm sorry", "Can we start over?", "I'm sorry. Always."
]

N = len(PHRASES)

s = t.Screen()
s.setup(width=800, height=800, startx=2380, starty=140)
s.title("100 Ways to Say Sorry")
s.bgcolor(BG_TOP)
s.tracer(0)
cv = s.getcanvas()
rng = random.Random(7)


def hx(rgb):
    return "#%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in rgb)


def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))


def clamp(v):
    return max(0.0, min(1.0, v))


def palette(k):
    x = clamp(k) * (len(STOPS) - 1)
    i = min(int(x), len(STOPS) - 2)
    return mix(STOPS[i], STOPS[i + 1], x - i)


# ------------ background: dusk gradient, tiny diamond stars, rings ------------
BANDS = 80
for i in range(BANDS):
    y0 = -400 + i * 800 / BANDS
    y1 = -400 + (i + 1) * 800 / BANDS + 1
    c = mix(BG_TOP, BG_BOT, (i / (BANDS - 1)) ** 1.4)
    cv.create_rectangle(-400, y0, 400, y1, fill=hx(c), outline="")

# 121 tiny stars (+10% more than video's 110) outside the main ring
WHITE = (1.0, 1.0, 1.0)
stars = []
for _ in range(121):
    x, y = rng.uniform(-400, 400), rng.uniform(-400, 400)
    if m.hypot(x, y) < 352:
        continue
    b = rng.uniform(0.35, 0.85)
    sz = rng.choice((1, 1, 2))
    col = hx(mix(BG_BOT, WHITE, b))

    cx, cy = x + sz * 0.5, y + sz * 0.5
    arm = sz + 1.2
    rh = cv.create_line(cx - arm, cy, cx + arm, cy, fill=col, width=1)
    rv = cv.create_line(cx, cy - arm, cx, cy + arm, fill=col, width=1)
    core = cv.create_oval(x, y, x + sz, y + sz, fill=col, outline="")
    stars.append((core, rh, rv, b))

for rad, k in ((R_INNER - 14, 0.35), (R_INNER - 10, 0.18), (R_MAX + 10, 0.12)):
    cv.create_oval(-rad, -rad, rad, rad, outline=hx(mix(BG_TOP, GOLD, k)), width=1)

RING = 356
cv.create_oval(-RING, -RING, RING, RING, outline=hx(mix(BG_TOP, GOLD, 0.16)), width=1)

# ------------ spokes ------------
fs = 9
while fs > 5:
    f = tkf.Font(root=cv, family="Georgia", size=fs)
    if max(f.measure(p) for p in PHRASES) <= R_MAX - R_INNER:
        break
    fs -= 1

spokes = []
for i, text in enumerate(PHRASES):
    th = m.pi / 2 - i * (2 * m.pi / N)  # start at 12 o'clock, go clockwise
    # Placed off-screen initially so there is zero dark smudge in the center
    sid = cv.create_text(
        -2000, -2000, text=text, font=("Georgia", fs),
        fill=hx(BG_TOP), anchor="w"
    )
    spokes.append({
        "id": sid, "th": th,
        "color": palette(i / (N - 1)),
        "born": None
    })

# ------------ centre ------------
title = cv.create_text(
    0, -52, text="1 0 0   W A Y S   T O   S A Y",
    font=("Georgia", 8, "bold"), fill=hx(BG_TOP)
)
title2 = cv.create_text(
    0, -36, text="S O R R Y",
    font=("Georgia", 7, "bold"), fill=hx(BG_TOP)
)
phrase = cv.create_text(
    0, 2, text="", font=("Georgia", 15, "italic"),
    fill=hx(CREAM), width=210, justify="center"
)
rule = cv.create_line(-26, 32, 26, 32, fill=hx(BG_TOP), width=1)
counter = cv.create_text(
    0, 48, text="", font=("Consolas", 8), fill=hx(BG_TOP)
)

arc = cv.create_arc(
    -RING, -RING, RING, RING, start=90, extent=-0.01,
    style="arc", outline=hx(GOLD), width=2
)

# ------------ state ------------
tick = 0
rot = 0.0
shown = 0
cur = 0
cur_t = 0
done_t = None


def show_center(i):
    global cur, cur_t
    cur, cur_t = i, tick
    cv.itemconfig(phrase, text=PHRASES[i])
    cv.itemconfig(counter, text="Nº %03d" % (i + 1))


def place(p, slide):
    th = (p["th"] - rot + m.pi) % (2 * m.pi) - m.pi
    rr = R_INNER + slide
    x, y = rr * m.cos(th), rr * m.sin(th)
    if m.pi / 2 < th or th <= -m.pi / 2:
        ang, anc = m.degrees(th) + 180.0, "e"
    else:
        ang, anc = m.degrees(th), "w"
    cv.coords(p["id"], x, -y)
    cv.itemconfig(p["id"], angle=round(ang % 360.0, 2), anchor=anc)


def step():
    global tick, rot, shown, done_t
    tick += 1
    rot += 0.00075 if shown < N else 0.0014

    # reveal the next apology
    if shown < N and tick % INTERVAL == 1:
        i = shown
        spokes[i]["born"] = tick
        shown += 1
        show_center(i)
        cv.itemconfig(arc, extent=-max(0.01, min(359.9, 360 * shown / N)))
        if shown == N:
            done_t = tick

    # when finished, keep the centre alive
    if done_t and (tick - done_t) > 150 and (tick - cur_t) >= 110:
        show_center(rng.choice([k for k in range(N) if k != cur]))

# spokes: fade in, slide out, and shift color dynamically as the wheel rotates
    sweep = (tick * 0.28) % N
    color_shift = tick * 0.0025  # speed of the flowing color wave

    for i, p in enumerate(spokes):
        if p["born"] is None:
            continue
        u = clamp((tick - p["born"]) / 45)
        e = 1 - (1 - u) ** 3
        place(p, (1 - e) * SLIDE)

        # Dynamically recalculate spoke color based on its moving position
        dyn_color = palette((i / N - color_shift) % 1.0)
        p["color"] = dyn_color

        glow = 0.0
        if done_t:
            d = abs(i - sweep)
            d = min(d, N - d)
            glow = max(0.0, 1 - (d / 3.0) ** 2) * 0.65

        pop = 4 * u * (1 - u) * clamp(1 - (tick - p["born"]) / 55) * 0.45
        col = mix(BG_BOT, dyn_color, 0.85 * e)
        col = mix(col, CREAM, max(glow, pop))
        cv.itemconfig(p["id"], fill=hx(col))

    # centre text
    a = clamp((tick - 5) / 50)
    cv.itemconfig(title, fill=hx(mix(BG_TOP, GOLD, 0.85 * a)))
    cv.itemconfig(title2, fill=hx(mix(BG_TOP, MUTED, 0.65 * a)))
    cv.itemconfig(rule, fill=hx(mix(BG_TOP, GOLD, 0.35 * a)))

    if shown:
        fv = clamp((tick - cur_t) / 18)
        c = mix(BG_TOP, mix(CREAM, spokes[cur]["color"], 0.35), fv)
        cv.itemconfig(phrase, fill=hx(c))
        cv.itemconfig(counter, fill=hx(mix(BG_TOP, MUTED, 0.75 * fv)))

    # Pure white diamond twinkle
    for _ in range(4):
        core, rh, rv, b = rng.choice(stars)
        flash = rng.uniform(0.4, 1.9)
        c_core = hx(mix(BG_BOT, WHITE, clamp(b * flash)))
        c_ray = hx(mix(BG_BOT, WHITE, clamp(b * flash * 0.85)))
        cv.itemconfig(core, fill=c_core)
        cv.itemconfig(rh, fill=c_ray)
        cv.itemconfig(rv, fill=c_ray)

    cv.after(TICK, step)


try:
    cv.after(200, step)
    t.done()
except (t.Terminator, Exception):
    pass