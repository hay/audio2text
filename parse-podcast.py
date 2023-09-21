#!/usr/bin/env python3
from pathlib import Path
import datetime
import json
import subprocess
import sys

def error(msg):
    log(f"[ERROR] - {msg}")

def log(msg):
    global output_dir
    time = datetime.datetime.now().isoformat("T")
    out_msg = f"[{time}] <parse-podcast.py> - {msg}"
    with open(output_dir / "log.log", "a") as f:
        f.write(out_msg + "\n")
    print(out_msg)

if len(sys.argv) != 2:
    sys.exit("Usage: parse-podcast.py <index>")

# First check if the output dir exists
output_root = Path("output")
if not output_root.exists():
    sys.exit("Output dir does not exist")

# Create the dir for this item
item_id = sys.argv[1]
output_dir = output_root / item_id
output_dir.mkdir(parents = True, exist_ok = True)

log(f"created directory for podcast item with index '{item_id}'")

# Load the file with all podcasts and try to find the specific item
with open("masterlist_final.json") as f:
    all_items = json.loads(f.read())

log("Loaded all items")

podcast = None
for item in all_items:
    if str(item["index"]) == str(item_id):
        log(f"Found the item: {item['podcast_titel']}")
        podcast = item
        break

if not podcast:
    error(f"Could not find item <{item_id}> in all_items")
    sys.exit(1)

# Let's also write the data to the output dir, because why not
with open(output_dir / "item.json", "w") as f:
    f.write(json.dumps(podcast, indent = 4))

# Okay, let's make a command
url = '"' + item["audio_link"] + '"'
cmd = [
    "./audio2text.py",
    "--engine", "whisperx",
    "--language", "nl",
    "--url", url,
    "--output-format", "srt,txt,csv",
    "--output", f"output/{item_id}/text",
    "--verbose",
    "--log-file", f"output/{item_id}/log.log",
    "--output-directory", f"output/{item_id}"
]

command = " ".join(cmd)
log(f"Going to execute command: {command}")
subprocess.check_call(command, shell = True)