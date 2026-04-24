#!/usr/bin/env zsh

set -euo pipefail

SCRIPT_DIR=${0:A:h}
SCENE_NAME=${1:-RowhammerIntro}
QUALITY_FLAG=${2:--pqh}
SCENE_FILE=${3:-video_project.py}
MODULE_NAME="${SCENE_FILE%.py}"
SAFE_MEDIA_DIR="$HOME/.manim-renders/math4012-video-project"
OUTPUT_DIR="$SCRIPT_DIR/rendered"

mkdir -p "$SAFE_MEDIA_DIR" "$OUTPUT_DIR"

manim "$QUALITY_FLAG" --media_dir "$SAFE_MEDIA_DIR" "$SCRIPT_DIR/$SCENE_FILE" "$SCENE_NAME"

SOURCE_VIDEO="$SAFE_MEDIA_DIR/videos/$MODULE_NAME/1080p60/$SCENE_NAME.mp4"
if [[ "$QUALITY_FLAG" == "-pql" ]]; then
  SOURCE_VIDEO="$SAFE_MEDIA_DIR/videos/$MODULE_NAME/480p15/$SCENE_NAME.mp4"
elif [[ "$QUALITY_FLAG" == "-pqm" ]]; then
  SOURCE_VIDEO="$SAFE_MEDIA_DIR/videos/$MODULE_NAME/720p30/$SCENE_NAME.mp4"
elif [[ "$QUALITY_FLAG" == "-pqh" ]]; then
  SOURCE_VIDEO="$SAFE_MEDIA_DIR/videos/$MODULE_NAME/1080p60/$SCENE_NAME.mp4"
elif [[ "$QUALITY_FLAG" == "-pqk" ]]; then
  SOURCE_VIDEO="$SAFE_MEDIA_DIR/videos/$MODULE_NAME/2160p60/$SCENE_NAME.mp4"
fi

cp "$SOURCE_VIDEO" "$OUTPUT_DIR/$SCENE_NAME.mp4"
echo "Saved render to: $OUTPUT_DIR/$SCENE_NAME.mp4"