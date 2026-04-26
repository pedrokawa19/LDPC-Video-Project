#!/usr/bin/env zsh

set -euo pipefail

SCRIPT_DIR=${0:A:h}
SCENE_NAME=${1:-RowhammerIntroPart2}
QUALITY_FLAG=${2:--pqh}
SCENE_FILE=${3:-video_project.py}
MODULE_NAME="${SCENE_FILE%.py}"
SAFE_MEDIA_DIR="$HOME/.manim-renders/math4012-video-project"
OUTPUT_DIR="$SCRIPT_DIR/rendered"

mkdir -p "$SAFE_MEDIA_DIR" "$OUTPUT_DIR"

# ── Helper: resolve output path for a given scene name ───────────────────────
scene_path() {
  local name=$1
  if [[ "$QUALITY_FLAG" == "-pql" ]]; then
    echo "$SAFE_MEDIA_DIR/videos/$MODULE_NAME/480p15/$name.mp4"
  elif [[ "$QUALITY_FLAG" == "-pqm" ]]; then
    echo "$SAFE_MEDIA_DIR/videos/$MODULE_NAME/720p30/$name.mp4"
  elif [[ "$QUALITY_FLAG" == "-pqk" ]]; then
    echo "$SAFE_MEDIA_DIR/videos/$MODULE_NAME/2160p60/$name.mp4"
  else
    echo "$SAFE_MEDIA_DIR/videos/$MODULE_NAME/1080p60/$name.mp4"
  fi
}

# ── Render a single scene and copy it into rendered/ ─────────────────────────
manim "$QUALITY_FLAG" --media_dir "$SAFE_MEDIA_DIR" "$SCRIPT_DIR/$SCENE_FILE" "$SCENE_NAME"
cp "$(scene_path $SCENE_NAME)" "$OUTPUT_DIR/$SCENE_NAME.mp4"
echo "Saved render to: $OUTPUT_DIR/$SCENE_NAME.mp4"
