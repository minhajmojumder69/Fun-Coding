import math as m
import random as r
import time
import tkinter as tk
import tkinter.font as tkf

W, H = 980, 900
DURATION = 8.8       
ANIM_TIME = 0.30       
TICK = 16            
LIFT = 32
GAP = 3
BG = "#060308"
FONT_FALLBACKS = ("Georgia", "Times New Roman", "Arial")
SEED = 17

PHRASES = [
    "I LOVE YOU", "I love you", "Te amo", "Ti amo", "Je t'aime",
    "Ich liebe dich", "Eu te amo", "Seni seviyorum", "Я тебя люблю",
    "AMOUR", "LOVE", "TE QUIERO", "愛してる", "사랑해", "我爱你",
    "أحبك", "আমি তোমাকে ভালোবাসি", "मैं तुमसे प्यार करता हूँ",
    "میں تم سے پیار کرتا ہوں", "Nakupenda", "Mahal kita", "Anh yêu em",
    "Rakastan sinua", "Jag älskar dig", "Σ' αγαπώ", "Ljubim te",
    "Volim te", "Kocham cię", "Te iubesc", "Miluji tě", "Logic Hunters",
    "Ik hou van jou", "Jeg elsker deg", "Ma armastan sind", "Es tevi mīlu",
    "Aš tave myliu", "Обичам те", "Logic Hunters", "ฉันรักคุณ",
    "Aku cinta kamu", "நான் உன்னை காதலிக்கிறேன்", "నేను నిన్ను ప్రేమిస్తున్నాను",
    "ನಾನು ನಿನ್ನನ್ನು ಪ್ರೀತಿಸುತ್ತೇನೆ", "ഞാൻ നിന്നെ സ്നേഹിക്കുന്നു", "Logic Hunters",
    "म तिमीलाई माया गर्छु", "دوستت دارم", "אני אוהב אותך", "მიყვარხარ",
    "Ես քեզ սիրում եմ", "Logic Hunters", "Maite zaitut", "Tá grá agam duit",
    "Ég elska þig", "Mi amas vin", "Ngiyakuthanda", "Tiako ianao"
]

SHORT_WORDS = [
    "LOVE", "AMOUR", "Te amo", "Ti amo", "أحبك", "사랑해",
    "愛してる", "我爱你", "Ljubim te", "Volim te", "Te dua"
]


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, int(rgb[0]))),
        max(0, min(255, int(rgb[1]))),
        max(0, min(255, int(rgb[2]))),
    )


def mix_rgb(c1, c2, t):
    return (
        c1[0] + (c2[0] - c1[0]) * t,
        c1[1] + (c2[1] - c1[1]) * t,
        c1[2] + (c2[2] - c1[2]) * t,
    )


def pick_font_family(root):
    available = set(tkf.families(root))
    for f in FONT_FALLBACKS:
        if f in available:
            return f
    return "Arial"


def rose_point_color(px, py):
    cx, cy = W * 0.5, 360.0
    nx = (px - cx) / 230.0
    ny = (py - cy) / 215.0

    if -1.08 <= ny <= 1.02 and -1.18 <= nx <= 1.18:
        if ny < 0.0:
            max_w = 0.96 + 0.16 * m.sin((ny + 1.0) * m.pi)
        else:
            max_w = 1.02 * m.sqrt(max(0.0, 1.0 - 0.88 * ny * ny))

        top_wave = (
            -0.82
            - 0.12 * m.cos(3.0 * nx)
            - 0.07 * m.cos(6.0 * nx + 0.6)
            + 0.14 * (nx * nx)
        )
        bot_curve = 0.94 - 0.18 * (nx * nx)

        if top_wave <= ny <= bot_curve and abs(nx) <= max_w:
            r_dist = m.hypot(nx, ny * 1.05)
            swirl_y = (ny + 0.28) * 1.45
            swirl_r = m.hypot(nx * 0.95, swirl_y)
            swirl_theta = m.atan2(swirl_y, nx)

            petal_wave = m.sin(
                swirl_r * 13.5
                - 2.0 * m.cos(swirl_theta * 2.0)
                + 1.3 * m.sin(swirl_theta * 3.0)
            )
            cup_wave = m.cos(nx * 6.5 - ny * 3.2)

            if -0.45 < ny < 0.55 and abs(petal_wave + 0.88) < 0.11 and r_dist > 0.28:
                return None

            shade = 0.52 + 0.32 * petal_wave + 0.16 * cup_wave - 0.15 * ny
            shade = max(0.0, min(1.0, shade))

            edge_prox = min(abs(max_w - abs(nx)), abs(ny - top_wave), abs(bot_curve - ny))
            if edge_prox < 0.09:
                shade = min(1.0, shade + 0.28)

            dark_ruby = (82, 8, 22)
            mid_crimson = (198, 20, 45)
            bright_rose = (255, 82, 108)

            if shade < 0.5:
                col = mix_rgb(dark_ruby, mid_crimson, shade * 2.0)
            else:
                col = mix_rgb(mid_crimson, bright_rose, (shade - 0.5) * 2.0)

            return col, "bloom", edge_prox

    calyx_y = (py - 568.0) / 38.0
    if -0.25 <= calyx_y <= 1.0:
        calyx_w = 46.0 * (1.0 - 0.65 * calyx_y) + 18.0 * m.exp(-((calyx_y - 0.15) * 3.5) ** 2)
        if abs(px - cx) <= calyx_w:
            t_g = 1.0 - abs(px - cx) / max(1.0, calyx_w)
            col = mix_rgb((28, 78, 32), (96, 186, 86), t_g)
            return col, "stem", 0.05

    if 565 <= py <= 845:
        stem_t = (py - 565.0) / (845.0 - 565.0)
        stem_cx = cx + 7.0 * m.sin(stem_t * m.pi * 1.15)
        stem_half_w = 15.5 * (1.0 - 0.55 * (stem_t ** 2.2))
        if stem_t > 0.92:
            stem_half_w *= max(0.15, (1.0 - stem_t) / 0.08)

        dx_stem = abs(px - stem_cx)
        if dx_stem <= stem_half_w:
            highlight = 1.0 - (dx_stem / max(1.0, stem_half_w))
            col = mix_rgb((25, 72, 28), (110, 205, 96), highlight * 0.85)
            return col, "stem", 0.02

    lx, ly = px - (cx - 12.0), py - 658.0
    ang_l = m.radians(28.0)
    ul = lx * m.cos(ang_l) + ly * m.sin(ang_l)
    vl = -lx * m.sin(ang_l) + ly * m.cos(ang_l)
    if -135.0 <= ul <= 0.0:
        s = abs(ul) / 135.0
        leaf_half_h = 30.0 * m.sin(s * m.pi) * (1.0 - 0.2 * s)
        if abs(vl) <= leaf_half_h:
            vein = 1.0 - abs(vl) / max(1.0, leaf_half_h)
            col = mix_rgb((26, 75, 30), (118, 214, 104), vein * 0.9)
            return col, "leaf", 0.04

    rx, ry = px - (cx + 12.0), py - 702.0
    ang_r = m.radians(-26.0)
    ur = rx * m.cos(ang_r) + ry * m.sin(ang_r)
    vr = -rx * m.sin(ang_r) + ry * m.cos(ang_r)
    if 0.0 <= ur <= 135.0:
        s = ur / 135.0
        leaf_half_h = 29.0 * m.sin(s * m.pi) * (1.0 - 0.2 * s)
        if abs(vr) <= leaf_half_h:
            vein = 1.0 - abs(vr) / max(1.0, leaf_half_h)
            col = mix_rgb((26, 75, 30), (118, 214, 104), vein * 0.9)
            return col, "leaf", 0.04

    return None


def build_rose_items(root, rng):
    family = pick_font_family(root)

    fonts = {
        "xs": tkf.Font(family=family, size=7, weight="normal"),
        "sm": tkf.Font(family=family, size=8, weight="normal"),
        "md": tkf.Font(family=family, size=9, weight="bold"),
        "lg": tkf.Font(family=family, size=11, weight="bold"),
    }

    measured = {}
    for k, fnt in fonts.items():
        pool = SHORT_WORDS if k == "xs" else PHRASES
        measured[k] = [(p, fnt.measure(p)) for p in pool]

    items = []
    y = 148
    while y <= 845:
        is_lower = y > 570
        row_step = 11 if is_lower else 13

        spans = []
        in_span = False
        x_start = 0
        for x in range(180, W - 180, 3):
            info = rose_point_color(x, y)
            if info is not None and not in_span:
                in_span = True
                x_start = x
            elif info is None and in_span:
                in_span = False
                spans.append((x_start, x - 3))
        if in_span:
            spans.append((x_start, W - 180))

        for x0, x1 in spans:
            seg_w = x1 - x0
            if seg_w < 16:
                continue

            cursor = x0
            while cursor < x1:
                rem = x1 - cursor
                if is_lower or rem < 48:
                    f_key = "xs" if rem < 36 or rng.random() < 0.55 else "sm"
                else:
                    roll = rng.random()
                    if roll < 0.16 and rem > 80:
                        f_key = "lg"
                    elif roll < 0.45 and rem > 55:
                        f_key = "md"
                    elif roll < 0.80:
                        f_key = "sm"
                    else:
                        f_key = "xs"

                candidates = measured[f_key]
                chosen = None
                for _ in range(10):
                    text, w = rng.choice(candidates)
                    if w <= rem or (cursor == x0 and w <= seg_w + 14):
                        chosen = (text, w, f_key)
                        break

                if chosen is None:
                    for text, w in measured["xs"]:
                        if w <= rem + 8 or cursor == x0:
                            chosen = (text, w, "xs")
                            break

                if chosen is None:
                    break

                text, w, f_key = chosen
                mid_x = cursor + w * 0.5
                info = rose_point_color(mid_x, y)
                if info is None:
                    info = rose_point_color(min(x1, max(x0, mid_x)), y)
                if info is not None:
                    col, region, edge_prox = info
                    items.append({
                        "x": mid_x,
                        "y": y,
                        "text": text,
                        "font": fonts[f_key],
                        "color": col,
                        "region": region,
                        "edge_prox": edge_prox,
                    })

                cursor += w + GAP

        y += row_step

    def spawn_order(it):
        norm_y = (850.0 - it["y"]) / 700.0
        if it["region"] in ("stem", "leaf"):
            return norm_y * 0.35 + rng.uniform(-0.03, 0.03)
        edge_bonus = -0.18 if it["edge_prox"] < 0.08 else 0.0
        return 0.18 + norm_y * 0.72 + edge_bonus + rng.uniform(-0.06, 0.06)

    items.sort(key=spawn_order)
    return items, family


def main():
    rng = r.Random(SEED)
    bg_rgb = hex_to_rgb(BG)

    root = tk.Tk()
    root.title("1 Rose, Every Language")
    root.geometry(f"{W}x{H}")
    root.configure(bg=BG)
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    items, family = build_rose_items(root, rng)


    title_str = "1 Rose, Every Language"
    title_font = tkf.Font(family=family, size=24, weight="bold")
    arc_cx, arc_cy, arc_r = W * 0.5, 560.0, 485.0
    total_span = m.radians(46.0)
    start_ang = -m.pi * 0.5 - total_span * 0.5
    for idx, ch in enumerate(title_str):
        frac = idx / max(1, len(title_str) - 1)
        ang = start_ang + frac * total_span
        tx = arc_cx + arc_r * m.cos(ang)
        ty = arc_cy + arc_r * m.sin(ang)
        canvas.create_text(
            tx, ty,
            text=ch,
            font=title_font,
            fill="#d91b42",
            anchor="center"
        )

    total_items = len(items)
    for idx, item in enumerate(items):
        item["spawn_time"] = (idx / max(1, total_items - 1)) * DURATION

    active = []
    next_idx = 0
    start_clock = None

    def step():
        nonlocal next_idx, start_clock
        now = time.perf_counter()
        if start_clock is None:
            start_clock = now
        elapsed = now - start_clock

        while next_idx < total_items and items[next_idx]["spawn_time"] <= elapsed:
            it = items[next_idx]
            next_idx += 1
            start_col = rgb_to_hex(mix_rgb(bg_rgb, it["color"], 0.15))
            cid = canvas.create_text(
                it["x"],
                it["y"] + LIFT,
                text=it["text"],
                font=it["font"],
                fill=start_col,
                anchor="center",
            )
            active.append({
                "id": cid,
                "x": it["x"],
                "target_y": it["y"],
                "color": it["color"],
                "final_hex": rgb_to_hex(it["color"]),
                "born": it["spawn_time"],
                "last_hex": start_col,
            })

        still_active = []
        for p in active:
            age = elapsed - p["born"]
            t = min(1.0, max(0.0, age / ANIM_TIME))

            if t >= 1.0:
                canvas.coords(p["id"], p["x"], p["target_y"])
                if p["last_hex"] != p["final_hex"]:
                    canvas.itemconfig(p["id"], fill=p["final_hex"])
            else:
                ease = 1.0 - (1.0 - t) ** 3
                cur_y = p["target_y"] + LIFT * (1.0 - ease)
                cur_hex = rgb_to_hex(mix_rgb(bg_rgb, p["color"], ease))

                canvas.coords(p["id"], p["x"], cur_y)
                if cur_hex != p["last_hex"]:
                    canvas.itemconfig(p["id"], fill=cur_hex)
                    p["last_hex"] = cur_hex
                still_active.append(p)

        active[:] = still_active

        if next_idx < total_items or active:
            root.after(TICK, step)

    root.after(100, step)
    root.mainloop()


if __name__ == "__main__":
    main()