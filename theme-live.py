#!/usr/bin/env python3
# Ghostty 테마 고르기: ↑↓로 옮기면 색·글꼴·크기·줄간격이 즉시 적용된다.
import os, re, sys, json, select, termios, tty, subprocess, unicodedata

HOME = os.path.expanduser("~/.config/ghostty")
CFG = HOME + "/config"
BUILTIN = "/Applications/Ghostty.app/Contents/Resources/ghostty/themes"
BEGIN, END = "# >>> theme-picker", "# <<< theme-picker"

def item(name, theme, desc, group, font=None, size=None, cell=None):
    return dict(name=name, theme=theme, desc=desc, group=group, font=font, size=size, cell=cell)

ITEMS = [item("원래 색", None, "배경 #1D1E27 + 직접 만든 팔레트", "기본")]
for m in json.load(open(HOME + "/soft-presets.json")):
    ITEMS.append(item(m["name"], m["name"], m["desc"], "Soft 13종 · 디자인 회사 팔레트 · 부드러운 다크"))
for n, d in [("Studio Ink", "따뜻한 먹색 + 한지색 글씨, 빨강만 강조"), ("Studio Graphite", "탁한 파스텔, 오래 봐도 덜 피곤"),
             ("Studio Blueprint", "설계도 남색 + 시안·노랑"), ("Studio Swiss", "흑백 + 빨강 하나 (diff 구분 약함)"), ("Studio Swiss Color", "Swiss 검정·흰 글씨 + 선명한 6색"),
             ("Studio Contrast", "모든 색 7:1 이상"), ("Studio Paper", "종이색 라이트 + 인쇄 잉크"), ("Studio Riso", "리소 형광 잉크 라이트")]:
    ITEMS.append(item(n, n, d, "Studio 7종 · 색만 바꿈"))
for m in json.load(open(HOME + "/lab-presets.json")):
    dark = m["name"] not in ("Lab Solar Light", "Lab Paper White", "Lab Dawn Rose", "Lab Clean Light", "Lab Latte", "Lab Sepia", "Lab Mint Morning", "Lab AAA Light")
    ITEMS.append(item(m["name"], m["name"], m["desc"], "Lab 30종 · " + ("다크" if dark else "라이트") + " · 색+글꼴+줄간격", m["font"], m["size"], m["cell"]))
for n, d in [("Monokai Classic", "개발자들이 오래 써온 대표 배색"), ("Monokai Pro", "Monokai를 다듬은 버전"), ("Ayu", "미니멀 다크"),
             ("GitHub Dark Default", "GitHub 화면과 같은 색"), ("Catppuccin Mocha", "인기 파스텔 다크"), ("Desert", "따뜻한 다크"),
             ("Nordfox", "차분한 청회색"), ("Adwaita Dark", "GNOME 기본 다크"), ("Synthwave", "네온 다크"),
             ("Ayu Light", "라이트 (일부 색 안 보임)"), ("Primary", "라이트 (일부 색 안 보임)"), ("Tinacious Design Light", "라이트 (일부 색 안 보임)"),
             ("Catppuccin Latte", "라이트 (일부 색 안 보임)"), ("One Half Light", "라이트 (일부 색 안 보임)")]:
    ITEMS.append(item(n, n, d, "기사 14종 · itsfoss.com"))

def parse(lines):
    c = {"palette": {}}
    for ln in lines:
        m = re.match(r"^\s*(background|foreground)\s*=\s*#?([0-9a-fA-F]{6})", ln)
        if m: c[m.group(1)] = m.group(2)
        m = re.match(r"^\s*palette\s*=\s*(\d+)\s*=\s*#?([0-9a-fA-F]{6})", ln)
        if m: c["palette"][int(m.group(1))] = m.group(2)
    return c

def colors(theme):
    if theme is None:
        return parse([re.sub(r"^#\[picker\] ", "", l) for l in open(CFG).read().splitlines()])
    own = HOME + "/themes/" + theme
    return parse(open(own if os.path.exists(own) else os.path.join(BUILTIN, theme)).read().splitlines())

def lum(h):
    r = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    r = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in r]
    return 0.2126 * r[0] + 0.7152 * r[1] + 0.0722 * r[2]
def contrast(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True); return (x + 0.05) / (y + 0.05)

def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def fg(h): return "\033[38;2;%d;%d;%dm" % rgb(h)
def bg(h): return "\033[48;2;%d;%d;%dm" % rgb(h)
RST = "\033[0m"
def width(s):
    s = re.sub(r"\033\[[0-9;]*m", "", s)
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in s)
def pad(s, n): return s + " " * max(n - width(s), 0)

W = 72
def card(it):
    c = colors(it["theme"])
    p = lambda i: fg(c["palette"].get(i, c["foreground"]))
    F = fg(c["foreground"]); B = bg(c["background"])
    row = lambda t="": "  " + B + F + "  " + t + B + " " * max(W - width(t), 0) + RST
    sw = lambda r: "".join(bg(c["palette"].get(i, "000000")) + "    " for i in r) + B
    low = min(contrast(v, c["background"]) for k, v in c["palette"].items() if k not in (0, 8))
    font = "%s %dpt · 줄간격 +%d%%" % (it["font"], it["size"], it["cell"]) if it["font"] else "글꼴은 지금 설정 그대로"
    info = "  \033[2m글꼴: %s   ·   본문 대비 %.1f   ·   가장 흐린 색 %.1f%s\033[0m" % (
        font, contrast(c["foreground"], c["background"]), low, "  ⚠ 안 보이는 색 있음" if low < 3 else "")
    return [info, row(), row(sw(range(8))), row(sw(range(8, 16))), row(),
        row(p(5) + "const " + p(4) + "greet" + F + " = (" + p(3) + "name" + F + ") => {"),
        row("  " + p(5) + "return " + p(2) + "`안녕하세요, ${name}님`" + F + "; " + p(8) + "// 인사 0Oo1lI" + F),
        row("};"),
        row(p(2) + "➜ " + p(6) + "~/workspace " + p(4) + "git:(" + p(1) + "main" + p(4) + ") " + F + "npm run dev"),
        row(p(1) + "error" + F + " 빨강   " + p(3) + "warn" + F + " 노랑   " + p(2) + "ok" + F + " 초록   " + p(8) + "흐린 글씨" + F),
        row()]

def apply(it):
    src, skip = [], False
    for l in open(CFG).read().splitlines():
        if l == BEGIN: skip = True; continue
        if l == END: skip = False; continue
        if not skip and not l.startswith("theme = "): src.append(l)
    if it["theme"] is None:
        src = [re.sub(r"^#\[picker\] ", "", l) for l in src]
    else:
        src = [("#[picker] " + l) if re.match(r"^(background|foreground|palette) =", l) else l for l in src]
        block = [BEGIN, "theme = " + it["theme"]]
        if it["font"]:
            block += ['font-family = ""', 'font-family = "%s"' % it["font"], "font-size = %d" % it["size"], "adjust-cell-height = %d%%" % it["cell"]]
            if it["font"] == "D2Coding": block.append("font-codepoint-map =")
        src += block + [END]
    open(CFG, "w").write("\n".join(src) + "\n")
    subprocess.run(["pkill", "-USR2", "-x", "ghostty"])

def current():
    for l in open(CFG).read().splitlines():
        if l.startswith("theme = "):
            t = l[8:].strip()
            for i, it in enumerate(ITEMS):
                if it["theme"] == t: return i
    return 0

def draw(sel):
    rows = os.get_terminal_size().lines
    disp, g = [], None
    for i, it in enumerate(ITEMS):
        if it["group"] != g:
            g = it["group"]
            if disp: disp.append(("", None))
            disp.append(("  \033[1;4m" + g + "\033[0m", None))
        if i == sel: disp.append(("  \033[1;7m ▶ %s \033[0m  %s" % (pad(it["name"], 22), it["desc"]), i))
        else: disp.append(("     %s   \033[2m%s\033[0m" % (pad(it["name"], 22), it["desc"]), i))
    h = max(rows - 17, 5)
    pos = next(k for k, (_, i) in enumerate(disp) if i == sel)
    top = min(max(pos - h // 2, 0), max(len(disp) - h, 0))
    view = [t for t, _ in disp[top:top + h]]
    view += [""] * (h - len(view))
    out = ["\033[H", "  \033[1mGhostty 테마 고르기\033[0m  %d/%d   ↑↓ 이동(바로 적용) · Enter 확정 · q 취소" % (sel + 1, len(ITEMS))]
    out += view + [""] + card(ITEMS[sel])
    sys.stdout.write("\r\n".join(l + "\033[K" for l in out) + "\033[J"); sys.stdout.flush()

def main():
    sel = start = current()
    fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
    sys.stdout.write("\033[?1049h\033[?25l\033[2J"); sys.stdout.flush()
    ok = False
    try:
        tty.setraw(fd)
        size = None
        while True:
            draw(sel); size = os.get_terminal_size()
            while not select.select([fd], [], [], 0.2)[0]:
                if os.get_terminal_size() != size: break
            else:
                pass
            if os.get_terminal_size() != size and not select.select([fd], [], [], 0)[0]: continue
            k = os.read(fd, 3)
            if k in (b"\x1b[A", b"k"): sel = (sel - 1) % len(ITEMS); apply(ITEMS[sel])
            elif k in (b"\x1b[B", b"j"): sel = (sel + 1) % len(ITEMS); apply(ITEMS[sel])
            elif k in (b"\r", b"\n"): ok = True; break
            elif k in (b"q", b"\x03", b"\x1b"): break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        sys.stdout.write("\033[?25h\033[?1049l"); sys.stdout.flush()
    if ok: print("\n  '%s' 로 확정했습니다. 이 탭은 닫아도 됩니다." % ITEMS[sel]["name"])
    else:
        apply(ITEMS[start]); print("\n  취소했습니다. 처음 상태(%s)로 돌아갔습니다." % ITEMS[start]["name"])

if __name__ == "__main__": main()
