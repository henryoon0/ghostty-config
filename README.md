# Ghostty 설정

[Ghostty](https://ghostty.org) 터미널 설정과 직접 만든 테마 51개입니다.

- 글꼴: JetBrains Mono 14pt, 한글은 SUIT
- 기본 테마: Studio Swiss Color (검정 배경, 흰 글씨, 선명한 6색)
- 테마 묶음: Studio 8종, Soft 13종, Lab 30종

## 1. 글꼴 설치

아래 두 글꼴을 먼저 설치하세요.

- [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- [SUIT](https://sun.fo/suit/) (한글용)

Homebrew를 쓰면:

```bash
brew install --cask font-jetbrains-mono
```

## 2. 설정 설치

```bash
git clone https://github.com/henryoon0/ghostty-config.git
cd ghostty-config
./install.sh
```

기존 설정은 `~/.config/ghostty/config.backup-날짜` 로 백업됩니다.
설치 후 Ghostty에서 `Cmd + Shift + ,` 를 누르면 바로 적용됩니다.

## 3. 테마 바꿔보기

```bash
python3 ~/.config/ghostty/theme-live.py
```

↑↓로 움직이면 색이 바로 바뀝니다. Enter로 확정, q로 취소합니다.

직접 고르려면 `~/.config/ghostty/config` 에서 이 줄만 바꾸세요.

```
theme = Studio Swiss Color
```

Lab 테마는 글꼴도 함께 바꿉니다. 해당 글꼴(Fira Code, D2Coding, Geist Mono 등)이 없으면 기본 글꼴로 보입니다.

## 파일 구성

| 파일 | 역할 |
|---|---|
| `config` | Ghostty 설정 본체 |
| `themes/` | 테마 51개 |
| `theme-live.py` | 테마 미리보기·선택 도구 |
| `*-presets.json`, `make-*.py` | 테마를 만든 원본 값과 생성 스크립트 |
| `install.sh` | 설치 스크립트 |

## 알아둘 설정

- `macos-option-as-alt = true`: Option 키를 Alt로 씁니다.
- `keybind = ctrl+key_v=text:\x16`: 한글 입력 상태에서도 Ctrl+V가 붙여넣기로 동작합니다.
