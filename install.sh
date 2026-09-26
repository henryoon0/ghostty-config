#!/bin/bash
# Ghostty 설정 설치: 기존 설정은 백업하고 이 저장소의 파일을 복사한다.
set -e
DEST="$HOME/.config/ghostty"
SRC="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$DEST"
if [ -f "$DEST/config" ]; then
  cp "$DEST/config" "$DEST/config.backup-$(date +%Y%m%d%H%M%S)"
  echo "기존 설정을 백업했습니다."
fi
cp "$SRC/config" "$DEST/config"
mkdir -p "$DEST/themes"
cp "$SRC"/themes/* "$DEST/themes/"
cp "$SRC"/theme-live.py "$SRC"/soft-presets.json "$SRC"/lab-presets.json "$DEST/"
pkill -USR2 -x ghostty 2>/dev/null || true
echo "설치 완료. Ghostty에서 Cmd+Shift+, 로 설정을 다시 불러오세요."
