#!/usr/bin/env python3
# Lab 프리셋 30종 생성기: 강조색 색상만 정하고, 밝기는 명암 대비 기준을 넘을 때까지 자동 조정한다.
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
    dark = L(bg) < 0.2
    toward = "FFFFFF" if dark else "000000"
    t = 0
    while cr(mix(c, toward, t), bg) < target and t < 1: t += 0.02
    return mix(c, toward, min(t, 1))

# (이름, 설명, 배경, 글자, [빨강 초록 노랑 파랑 보라 청록], 글꼴, 크기, 줄간격%, 대비목표)
P = [
 ("Lab Night Indigo", "도쿄 밤거리 남보라, 색 구분이 가장 쉬운 다크", "16161E","C0CAF5",["F7768E","9ECE6A","E0AF68","7AA2F7","BB9AF7","7DCFFF"],"JetBrains Mono",14,10,4.5),
 ("Lab Wave Ink", "우키요에 먹색과 바랜 물감, 차분한 한지 느낌", "1F1F28","DCD7BA",["C34043","76946A","C0A36E","7E9CD8","957FB8","6A9589"],"IBM Plex Mono",14,8,4.5),
 ("Lab Forest", "숲속 이끼색, 눈이 편한 저채도 초록", "1E2326","D3C6AA",["E67E80","A7C080","DBBC7F","7FBBB3","D699B6","83C092"],"Fira Code",14,8,4.5),
 ("Lab Retro Warm", "레트로 갈색과 주황, 따뜻하고 대비 강함", "282828","EBDBB2",["FB4934","B8BB26","FABD2F","83A598","D3869B","8EC07C"],"Source Code Pro",14,8,4.5),
 ("Lab Solar Dark", "태양광 계열 정밀 배색, 청록 바탕", "002B36","D5DFDF",["DC322F","859900","B58900","268BD2","D33682","2AA198"],"Hack",14,6,4.5),
 ("Lab Carbon", "IBM 카본 디자인, 순수한 검정과 형광 강조", "161616","F2F4F8",["EE5396","42BE65","FFE97B","33B1FF","BE95FF","3DDBD9"],"IBM Plex Mono",14,8,4.5),
 ("Lab Pure Black", "개발 도구 스타일의 순수 검정, 군더더기 없음", "0A0A0A","EDEDED",["FF6166","62C073","F2A60D","52A8FF","BF7AF0","0AC7B4"],"Geist Mono",14,12,4.5),
 ("Lab Deep Ocean", "심해 남색과 파스텔, 코드가 선명하게 뜸", "0F111A","C8CCD8",["F07178","C3E88D","FFCB6B","82AAFF","C792EA","89DDFF"],"Monaspace Neon",13,10,4.5),
 ("Lab Vampire", "보라 바탕 형광 파스텔, 밤샘 작업용", "22212C","F8F8F2",["FF9580","8AFF80","FFFF80","9580FF","FF80BF","80FFEA"],"Fira Code",14,6,4.5),
 ("Lab Phosphor", "옛날 녹색 모니터, 초록 한 가지 색", "0A0F0A","5CFF8A",["FF6B5C","5CFF8A","D6FF5C","5CD6FF","B8FF5C","5CFFD6"],"Monaspace Krypton",13,8,4.5),
 ("Lab Amber CRT", "호박색 단색 모니터, 집중 모드", "120C02","FFB54D",["FF6B4D","E6C24D","FFD54D","FFB54D","FF9A4D","F2C27A"],"Space Mono",14,4,4.5),
 ("Lab Espresso", "에스프레소 갈색과 크림, 커피챗 무드", "2B211C","EADBC8",["E0786B","A9C08A","E6B872","8FB3D1","C79BC0","86C2B4"],"IBM Plex Mono",14,10,4.5),
 ("Lab Glacier", "북유럽 빙하 청회색, 아주 차분함", "2E3440","ECEFF4",["BF616A","A3BE8C","EBCB8B","81A1C1","B48EAD","88C0D0"],"JetBrains Mono",14,10,4.5),
 ("Lab Sakura Night", "벚꽃 핑크 포인트의 부드러운 다크", "1A1520","F2E6EE",["FF7A93","A6D189","F4C27A","8CAAEE","F4A6D7","81C8BE"],"Victor Mono",15,6,4.5),
 ("Lab Cyber Neon", "사이버펑크 형광 시안·마젠타", "0B0B10","E6E6F0",["FF3D6E","3DFFA8","FFE03D","3DB8FF","FF3DF0","3DFFF0"],"Rec Mono Duotone",14,8,4.5),
 ("Lab Low Light", "불 끈 방 야간용, 밝기를 낮춘 저자극", "101014","A8A8B3",["C47A7A","8AA37A","B8A070","7A92B8","A382B0","7AA8A8"],"JetBrains Mono",15,12,4.5),
 ("Lab Moss", "회녹색 이끼, 녹색 계열로 통일", "1A1D17","D8DCCB",["D98C7A","A8C47A","D9C27A","8CB0B8","B89CC4","8CC4A8"],"Cascadia Code",14,6,4.5),
 ("Lab Slate", "웹 디자인 표준 슬레이트 회청색", "1E293B","E2E8F0",["F87171","4ADE80","FACC15","60A5FA","C084FC","22D3EE"],"Geist Mono",14,12,4.5),
 ("Lab Violet Minimal", "무채색 + 보라 하나, 요즘 SaaS 감성", "0F0F14","E6E6EE",["EB5757","4CB782","F2C94C","5E6AD2","8B7CF6","5EC4D2"],"Monaspace Neon",13,10,4.5),
 ("Lab Clay", "점토색 주황 한 가지, 따뜻한 무채색", "1F1E1D","F0EEE6",["D97757","9DB17C","E0B45E","8FA8C8","C29AC2","86B5A8"],"JetBrains Mono NL",14,10,4.5),
 ("Lab Hangul Grid", "한글·영문 폭이 정확히 맞는 D2Coding", "1B1D22","E4E6EB",["F28B82","81C995","FDD663","8AB4F8","C58AF9","78D9EC"],"D2Coding",15,6,4.5),
 ("Lab AAA Dark", "모든 색 7:1 이상, 큰 글씨 최대 가독성", "000000","FFFFFF",["FF5C5C","3CE67A","FFE14D","5CA8FF","FF7AFF","3CE6E6"],"JetBrains Mono",16,10,7),
 ("Lab Solar Light", "태양광 배색의 밝은 버전, 크림 바탕", "FDF6E3","3B4A50",["DC322F","859900","B58900","268BD2","D33682","2AA198"],"Source Code Pro",14,8,4.5),
 ("Lab Paper White", "노트 앱 같은 흰 종이와 먹색", "FFFFFF","37352F",["E03E3E","0F7B6C","DFAB01","0B6E99","6940A5","2E8F8F"],"IBM Plex Mono",14,10,4.5),
 ("Lab Dawn Rose", "새벽 장밋빛 라이트, 부드러운 필기체 이탤릭", "FAF4ED","575279",["B4637A","286983","EA9D34","56949F","907AA9","D7827E"],"Victor Mono",15,6,4.5),
 ("Lab Clean Light", "코드 저장소 사이트 같은 깔끔한 라이트", "FFFFFF","1F2328",["CF222E","116329","9A6700","0969DA","8250DF","1B7C83"],"Monaspace Neon",13,10,4.5),
 ("Lab Latte", "라떼 크림 바탕, 커피챗 라이트 버전", "F5EFE6","3B2F2A",["C0392B","5A7D2A","A66A00","2E6DA4","8E44AD","2A8074"],"JetBrains Mono",14,10,4.5),
 ("Lab Sepia", "전자책 세피아, 긴 로그 읽기용", "F4ECD8","433422",["A63D40","5B7B3A","8C6A1F","3D6A8C","7A4E8C","3D7F7A"],"IBM Plex Mono",15,12,4.5),
 ("Lab Mint Morning", "민트빛 아침 라이트, 산뜻하고 가벼움", "F2F7F4","1E2B26",["D1495B","2A9D5C","B7791F","2F6FD0","8E5BD0","1E8C8C"],"Fira Code",14,8,4.5),
 ("Lab AAA Light", "흰 바탕 모든 색 7:1 이상, 밝은 곳 최대 가독성", "FFFFFF","000000",["B00020","006B2E","6B4E00","0040B0","7A1FA2","005F6B"],"JetBrains Mono",16,10,7),
]

meta = []
for name, desc, bg, fg, acc, font, size, cell, target in P:
    dark = L(bg) < 0.2
    if dark:
        c0 = mix(bg, "FFFFFF", 0.10)
        c8 = fit(mix(bg, fg, 0.45), bg, 4.0)
        c7 = mix(fg, bg, 0.12); c15 = mix(fg, "FFFFFF", 0.4)
        brights = [fit(mix(a, "FFFFFF", 0.18), bg, target) for a in acc]
    else:
        c0 = fg
        c8 = fit(mix(bg, fg, 0.55), bg, 4.0)
        c7 = fit(mix(fg, bg, 0.3), bg, target); c15 = mix(fg, "000000", 0.3)
        brights = [fit(mix(a, "000000", 0.12), bg, target) for a in acc]
    normals = [fit(a, bg, target) for a in acc]
    pal = [c0] + normals + [c7, c8] + brights + [c15]
    sel = mix(bg, fg, 0.22)
    with open(os.path.expanduser("~/.config/ghostty/themes/" + name), "w") as f:
        f.write("".join("palette = %d=#%s\n" % (i, p) for i, p in enumerate(pal)))
        f.write("background = #%s\nforeground = #%s\ncursor-color = #%s\ncursor-text = #%s\nselection-background = #%s\nselection-foreground = #%s\n" % (bg, fg, fg, bg, sel, fg))
    low = min(cr(p, bg) for i, p in enumerate(pal) if i not in (0, 8))
    meta.append({"name": name, "desc": desc, "font": font, "size": size, "cell": cell, "body": round(cr(fg, bg), 1), "low": round(low, 1), "dim": round(cr(c8, bg), 1)})
json.dump(meta, open(os.path.expanduser("~/.config/ghostty/lab-presets.json"), "w"), ensure_ascii=False, indent=1)
for m in meta: print("%-20s 본문 %4.1f  색 최저 %4.1f  주석 %3.1f  %s %dpt +%d%%" % (m["name"], m["body"], m["low"], m["dim"], m["font"], m["size"], m["cell"]))
