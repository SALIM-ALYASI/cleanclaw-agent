#!/bin/bash
set -e

HOME_DIR="${1:-$HOME}"
TS=$(date +"%Y%m%d_%H%M%S")
OUT_MD="$HOME_DIR/PARKING/reports/scan_home_${TS}.md"

mkdir -p "$HOME_DIR/PARKING/reports"

echo "# CleanClaw Scan Report" > "$OUT_MD"
echo "Home: $HOME_DIR" >> "$OUT_MD"
echo "Time: $(date)" >> "$OUT_MD"
echo "" >> "$OUT_MD"

echo "## Projects Detected" >> "$OUT_MD"

for item in "$HOME_DIR"/*; do
  base=$(basename "$item")

  # استثناء مجلدات النظام
  case "$base" in
    Library|Applications|PARKING|MyProjects|INBOX|CLEAN_VAULT)
      continue
      ;;
  esac

  if [ -d "$item" ]; then
    if [ -d "$item/.git" ] || \
       [ -f "$item/package.json" ] || \
       [ -f "$item/composer.json" ] || \
       [ -f "$item/requirements.txt" ]; then
      echo "- $item" >> "$OUT_MD"
    fi
  fi
done

echo "" >> "$OUT_MD"
echo "## Archives Found" >> "$OUT_MD"

for item in "$HOME_DIR"/*.zip "$HOME_DIR"/*.tar.gz "$HOME_DIR"/*.tgz; do
  [ -e "$item" ] && echo "- $item" >> "$OUT_MD"
done

echo "" >> "$OUT_MD"
echo "## Other Top-Level Items" >> "$OUT_MD"

for item in "$HOME_DIR"/*; do
  base=$(basename "$item")

  case "$base" in
    Library|Applications|PARKING|MyProjects|INBOX|CLEAN_VAULT)
      continue
      ;;
  esac

  echo "- $item" >> "$OUT_MD"
done

echo "✅ Scan saved to: $OUT_MD"