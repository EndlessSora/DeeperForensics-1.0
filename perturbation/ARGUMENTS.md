## Detailed Explanation of Arguments

This page provides the detailed explanation of all the arguments in our
perturbation codes.

### add_distortion_to_video.py
You can run:
```bash
python add_distortion_to_video.py -h
```
to get all the arguments and their detailed meanings:
```
usage: add_distortion_to_video.py [-h] --vid_in VID_IN --vid_out VID_OUT [--type TYPE] [--level LEVEL] [--meta_path META_PATH]
                                  [--via_xvid]

Add a distortion to video.

optional arguments:
  -h, --help            show this help message and exit
  --vid_in VID_IN       path to the input video
  --vid_out VID_OUT     path to the output video
  --type TYPE           distortion type: CS | CC | BW | GNC | GB | JPEG | VC | random
  --level LEVEL         distortion level: 1 | 2 | 3 | 4 | 5 | random
  --meta_path META_PATH
                        path to the output video meta file
  --via_xvid            if add this argument, write to XVID .avi video first, then convert it to 'vid_out' by ffmpeg
```
`--vid_in` and `--vid_out` specify the input and output videos, respectively.
These two arguments must be given by user. `--vid_in` and `--vid_out` cannot
be the same. If the root of `--vid_out` does not exist, the program will create
it.

`--type` specifies the distortion type, with options:
`CS` (**color saturation change**), `CC` (**color contrast change**),
`BW` (**local block-wise**), `GNC` (**white Gaussian noise in color components**),
`GB` (**Gaussian blur**), `JPEG` (**JPEG compression**), `VC` (**video compression**),
`random` (**random-type**). Default: `random`.

`--level` specifies the distortion level, with options:
`1` (**level-1**), `2` (**level-2**), `3` (**level-3**), `4` (**level-4**), `5` (**level-5**),
`random` (**random-level**). Default: `random`.

`--meta_path` specifies the distortion meta file path. If this argument is
not `None`, the program will also write distortion meta information to the
given file, otherwise will just process the video. Note that if the meta file
exists, the program will keep the history and automatically update it (then
it can record the mixed distortion information if you want to apply them).
If the root of`--meta_path` does not exist, the program will create it.
Default: `None`.

`--via_xvid` controls whether to write the distorted frames to an `.avi`
video with `XVID` codec first, and then convert it to `vid_out` by `FFmpeg`.
If we add this argument, the program will do this operation, otherwise not.
**Note:** if you would like to **strictly** align with the distortions in our dataset,
**please add** `--via_xvid` **in your command.**

**P.S. Why do we need** `--via_xvid` **argument?** We find that if we directly
use the format and codec of the input video (_i.e._, `.mp4` format with `H.264`
codec) as that of the output video, it may introduce unnecessary _oscillation_,
_deformation_ or _blur_ when the distortion is **very strong** (_e.g._, level-5 `GNC`
distortion. You can try it by yourself~). However, if we introduce an
intermediate video (`.avi` format with `XVID` codec) and then convert it to `vid_out`
by `FFmpeg`, the problem can be solved. (Of course, you may find another codec that
can solve the problem)


### check_video.py
Similarly, you can run:
```bash
python check_video.py -h
```
to get all the arguments and their detailed meanings:
```
usage: check_video.py [-h] --vid_in VID_IN --vid_out VID_OUT

Check video information.

optional arguments:
  -h, --help         show this help message and exit
  --vid_in VID_IN    path to the input video
  --vid_out VID_OUT  path to the output video
```
which are very easy to understand. `--vid_in` and `--vid_out` specify the input
and output videos, respectively. These two arguments must be given by user, and
both of them should exist.
