#!/usr/bin/env bash

set -x

python check_video.py \
    --vid_in data/input.mp4 \
    --vid_out results/output.mp4
