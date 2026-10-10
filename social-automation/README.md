# NH Social Automation — GHL Story/Post Pipeline (built 2026-07-14)

Scripts behind the Nutrition Hub auto-posting system in GHL Social Planner
(location `HJl01216dIdKMhk1SSn1`). Live schedule as of 7/14: **4 stories/day**
(9a/12p/3p/6p CT, FB+IG) + daily Google Business post (7:30a CT) through
**Aug 31**, reels through Sep 2. Content pool: 113 story videos in GHL Media Library.

Set `GHL_NUTRITION_HUB_TOKEN` (see `/Users/apple/GTM-Workspace/.env`) before running.

| Script | Purpose |
|---|---|
| `extend_nh_schedule.py` | Extend the story + GBP post schedule (`--test` one post, `--go` full). Collects rotation pools from existing posts. Re-run before the schedule runs dry (late Aug). |
| `process_clips.py` | Prep raw drop-folder clips: Whisper captions where real speech (skip song lyrics!), blur-pad horizontals to 9:16, skip clips <3s. Needs **ffmpeg-full** (`/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg`) + whisper-cli + `~/models/ggml-base.en.bin`. |
| `fix_captioned.py` | Caption burn via styled ASS file (inline force_style breaks ffmpeg's parser). |
| `upload_media.sh` | Bulk-upload processed clips to GHL Media Library (`POST /medias/upload-file`). Writes `upload_map.jsonl`. |
| `weave_rotation.py` | Re-assign media across future scheduled story slots, interleaving new uploads (freshest first) with the existing pool. `--dry` then `--go`. |

Workflow: Ronnie drops videos in `~/Desktop/NH-Story-Drop/` → process → upload →
weave → archive originals to `uploaded/`. Full playbook lives in Claude memory
(`project_ghl_social`). Verify publishes via CHILD posts, never the parent.
