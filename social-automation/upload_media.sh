#!/bin/zsh
# Upload processed NH clips to GHL Media Library; append name->url mapping to JSON lines file.
TOKEN="${GHL_NUTRITION_HUB_TOKEN}"
DIR="/Users/apple/Desktop/NH-Story-Drop/processed"
OUTMAP="/Users/apple/Desktop/NH-Story-Drop/.work/upload_map.jsonl"
: > "$OUTMAP"
ok=0; fail=0
for f in "$DIR"/*.mp4; do
  name=$(basename "$f")
  if [[ "$name" == "IMG_1331.mp4" ]]; then
    echo "{\"name\": \"IMG_1331.mp4\", \"url\": \"https://assets.cdn.filesafe.space/HJl01216dIdKMhk1SSn1/media/615f5674-4094-4e02-91ef-18e5f9b86ecf.mp4\"}" >> "$OUTMAP"
    echo "SKIP (already uploaded) $name"; ((ok++)); continue
  fi
  resp=$(curl -s -m 300 -X POST "https://services.leadconnectorhq.com/medias/upload-file" \
    -H "Authorization: Bearer $TOKEN" -H "Version: 2021-07-28" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
    -F "file=@$f;type=video/mp4" -F "name=NH-drop-$name")
  url=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('url',''))" 2>/dev/null)
  if [[ -n "$url" ]]; then
    echo "{\"name\": \"$name\", \"url\": \"$url\"}" >> "$OUTMAP"
    echo "OK $name"; ((ok++))
  else
    echo "FAIL $name: $resp"; ((fail++))
  fi
  sleep 1
done
echo "UPLOAD DONE ok=$ok fail=$fail"
