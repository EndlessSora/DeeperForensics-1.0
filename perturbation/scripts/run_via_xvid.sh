#!/usr/bin/env bash

set -x

python add_distortion_to_video.py \
    --vid_in data/input.mp4 \
    --vid_out results/output.mp4 \
    --type random \
    --level random \
    --meta_path metas/meta.txt \
    --via_xvid
