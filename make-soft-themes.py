#!/usr/bin/env python3
# Soft 13종: 세계 디자인 시스템의 다크 표면색·강조색에서 영감을 받은 부드러운 다크 테마.
import json, os
def L(h):
    r = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    r = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in r]
    return 0.2126 * r[0] + 0.7152 * r[1] + 0.0722 * r[2]
def cr(a, b):
    x, y = sorted([L(a), L(b)], reverse=True); return (x + 0.05) / (y + 0.05)
def mix(a, b, t):
    A = [int(a[i:i+2], 16) for i in (0, 2, 4)]; B = [int(b[i:i+2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % round(x + (y - x) * t) for x, y in zip(A, B))
def fit(c, bg, target):
    t = 0
    while cr(mix(c, "FFFFFF", t), bg) < target and t < 1: t += 0.02
    return mix(c, "FFFFFF", min(t, 1))

P = [
 ("Soft Graphite", "Apple 다크 모드의 그라파이트 회색 + 시스템 색", "1F1F21", "E5E5E7", ["FF6961","5ED17A","FFD55A","5AA8FF","C88AF0","70D0F0"]),
 ("Soft Carbon", "IBM Carbon 디자인 시스템 Gray 90 표면", "262626", "F0F0F0", ["FF8389","6FDC8C","F1C21B","78A9FF","BE95FF","3DDBD9"]),
 ("Soft Material", "Google Material 3의 보랏빛 회색 표면과 톤 색", "1C1B1F", "E6E1E5", ["F2B8B5","A8DAB5","F5D98A","A8C7FA","D0BCFF","9CD8D8"]),
 ("Soft Dimmed", "GitHub Primer 'dimmed' 푸른 회색, 눈부심 최소", "22272E", "CDD9E5", ["F47067","57AB5A","C69026","539BF5","B083F0","39C5CF"]),
 ("Soft Notion", "Notion 다크 모드의 따뜻한 회색과 차분한 색", "252525", "E3E2E0", ["FF7369","4DAB9A","FFDC49","529CCA","9A6DD7","5FB8B3"]),
 ("Soft Figma", "Figma 에디터 회색 + 로고 다섯 색", "2C2C2C", "EDEDED", ["F24E1E","0FA958","FFC700","18A0FB","A259FF","1BC4C4"]),
 ("Soft Spectrum", "Adobe Spectrum 중간 회색, 가장 밝은 다크", "2A2A2A", "E8E8E8", ["E34850","2D9D78","E68619","2680EB","9256D9","1B959A"]),
 ("Soft Linear", "Linear 차가운 청회색과 인디고", "1D1E24", "E4E5E9", ["EB5757","4CB782","F2C94C","7C8BFF","A78BFA","5EC4D2"]),
 ("Soft Stripe", "Stripe 네이비 + 블러플(파랑 보라)", "1A2438", "E3E8EE", ["FF7A8A","3ECF8E","F5BE58","7A73FF","C08CFF","5FD4F4"]),
 ("Soft Braun", "Dieter Rams 브라운 제품의 웜 그레이 + 주황", "2B2A28", "E8E4DA", ["E8702A","8FA876","E5B94E","7B9EB8","A68CA8","7FAFA6"]),
 ("Soft Muji", "무인양품 흙빛 무채색, 가장 차분함", "2A2724", "E6DFD3", ["C9776B","9DAE85","D4B477","8EA6B8","B399A8","8CB0A6"]),
 ("Soft Editorial", "에디토리얼 잡지의 올리브 차콜", "2B2D2A", "E7E3D8", ["C87D6E","9CB08A","D8B870","8FA3B5","B395A6","8DB3AA"]),
 ("Soft Swiss", "지금 쓰는 Swiss Color를 회색 바탕으로 부드럽게", "202022", "E8E8E6", ["FF4A3D","5BD68A","F5C451","5AA9FF","D98CFF","4FD1D9"]),
]
meta = []
for name, desc, bg, fg, acc in P:
    normals = [fit(a, bg, 4.5) for a in acc]
    brights = [fit(mix(a, "FFFFFF", 0.18), bg, 4.5) for a in acc]
    # 흐린 회색(8번)은 흐린 글씨(배경 대비)와 입력 띠(흰 글씨 대비) 양쪽을 만족하는 값을 찾는다
    best = max((mix(bg, "FFFFFF", t / 100) for t in range(10, 70)),
               key=lambda c: min(cr(c, bg) / 3.5, cr(fg, c) / 4.5))
    pal = [mix(bg, "FFFFFF", 0.08)] + normals + [mix(fg, bg, 0.12), best] + brights + [mix(fg, "FFFFFF", 0.4)]
    with open(os.path.expanduser("~/.config/ghostty/themes/" + name), "w") as f:
        f.write("".join("palette = %d=#%s\n" % (i, p) for i, p in enumerate(pal)))
        f.write("background = #%s\nforeground = #%s\ncursor-color = #%s\ncursor-text = #%s\nselection-background = #%s\nselection-foreground = #%s\n"
                % (bg, fg, pal[1], bg, mix(bg, fg, 0.22), fg))
    low = min(cr(p, bg) for i, p in enumerate(pal) if i not in (0, 8))
    meta.append(dict(name=name, desc=desc, bg=bg, fg=fg, pal=pal))
    print("%-15s 배경 #%s  본문 %4.1f  색 최저 %3.1f  흐린글씨 %3.1f  띠위흰글씨 %3.1f" % (name, bg, cr(fg, bg), low, cr(best, bg), cr(fg, best)))
json.dump(meta, open(os.path.expanduser("~/.config/ghostty/soft-presets.json"), "w"), ensure_ascii=False, indent=1)
