import argparse
import copy
import os
import random

import cv2
from tqdm import tqdm

from distortions import (block_wise, color_contrast, color_saturation,
                         gaussian_blur, gaussian_noise_color, jpeg_compression,
                         video_compression)


def parse_args():
    parser = argparse.ArgumentParser(description='Add a distortion to video.')
    parser.add_argument('--vid_in',
                        type=str,
                        required=True,
                        help='path to the input video')
    parser.add_argument('--vid_out',
                        type=str,
                        required=True,
                        help='path to the output video')
    parser.add_argument(
        '--type',
        type=str,
        default='random',
        help='distortion type: CS | CC | BW | GNC | GB | JPEG | VC | random')
    parser.add_argument('--level',
                        type=str,
                        default='random',
                        help='distortion level: 1 | 2 | 3 | 4 | 5 | random')
    parser.add_argument('--meta_path',
                        type=str,
                        default=None,
                        help='path to the output video meta file')
    parser.add_argument(
        '--via_xvid',
        action='store_true',
        help='if add this argument, write to XVID .avi video first, '
        "then convert it to 'vid_out' by ffmpeg.")
    args = parser.parse_args()

    return args


def get_distortion_parameter(type, level):
    param_dict = dict()  # a dict of list
    param_dict['CS'] = [0.4, 0.3, 0.2, 0.1, 0.0]  # smaller, worse
    param_dict['CC'] = [0.85, 0.725, 0.6, 0.475, 0.35]  # smaller, worse
    param_dict['BW'] = [16, 32, 48, 64, 80]  # larger, worse
    param_dict['GNC'] = [0.001, 0.002, 0.005, 0.01, 0.05]  # larger, worse
    param_dict['GB'] = [7, 9, 13, 17, 21]  # larger, worse
    param_dict['JPEG'] = [2, 3, 4, 5, 6]  # larger, worse
    param_dict['VC'] = [30, 32, 35, 38, 40]  # larger, worse

    # level starts from 1, list starts from 0
    return param_dict[type][level - 1]


def get_distortion_function(type):
    func_dict = dict()  # a dict of function
    func_dict['CS'] = color_saturation
    func_dict['CC'] = color_contrast
    func_dict['BW'] = block_wise
    func_dict['GNC'] = gaussian_noise_color
    func_dict['GB'] = gaussian_blur
    func_dict['JPEG'] = jpeg_compression
    func_dict['VC'] = video_compression

    return func_dict[type]


def apply_distortion_log(type, level):
    if type == 'CS':
        print(f'Apply level-{level} color saturation change distortion...')
    elif type == 'CC':
        print(f'Apply level-{level} color contrast change distortion...')
    elif type == 'BW':
        print(f'Apply level-{level} local block-wise distortion...')
    elif type == 'GNC':
        print(f'Apply level-{level} white Gaussian noise in color components '
              'distortion...')
    elif type == 'GB':
        print(f'Apply level-{level} Gaussian blur distortion...')
    elif type == 'JPEG':
        print(f'Apply level-{level} JPEG compression distortion...')
    elif type == 'VC':
        print(f'Apply level-{level} video compression distortion...')


def distortion_vid(vid_in,
                   vid_out,
                   type='random',
                   level='random',
                   via_xvid=False):
    # create output root
    root = os.path.split(vid_out)[0]
    root = '.' if root == '' else root
    os.makedirs(root, exist_ok=True)

    # get distortion type
    if type == 'random':
        dist_types = ['CS', 'CC', 'BW', 'GNC', 'GB', 'JPEG', 'VC']
        type_id = random.randint(0, 6)
        dist_type = dist_types[type_id]
    else:
        dist_type = type

    # get distortion level
    if level == 'random':
        dist_level = random.randint(1, 5)
    else:
        dist_level = int(level)

    # get distortion parameter
    dist_param = get_distortion_parameter(dist_type, dist_level)

    # get distortion function
    dist_function = get_distortion_function(dist_type)

    # apply distortion
    if dist_type == 'VC':
        apply_distortion_log(dist_type, dist_level)
        dist_function(vid_in, vid_out, dist_param)
    else:
        # extract frames
        vid = cv2.VideoCapture(vid_in)
        fps = vid.get(cv2.CAP_PROP_FPS)
        fourcc = int(vid.get(cv2.CAP_PROP_FOURCC))
        w = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f'Input video fps: {fps}')
        print(f'Input video fourcc: {fourcc}')
        print(f'Input video frame size: {w} * {h}')
        print(f'Input video frame count: {frame_count}')
        print('Extracting frames...')
        frame_list = []
        while True:
            success, frame = vid.read()
            if not success:
                break
            frame_list.append(frame)
        vid.release()
        assert len(frame_list) == frame_count

        # add distortion to the frame and write to the new video at 'vid_out'
        if via_xvid:
            writer = cv2.VideoWriter(
                f'{vid_out[:-4]}_tmp.avi',
                cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), fps, (w, h))
        else:
            writer = cv2.VideoWriter(vid_out, fourcc, fps, (w, h))
        apply_distortion_log(dist_type, dist_level)
        for frame in tqdm(frame_list):
            new_frame = dist_function(frame, dist_param)
            writer.write(new_frame)
        writer.release()
        if via_xvid:
            cmd = f'ffmpeg -i {vid_out[:-4]}_tmp.avi -y {vid_out}'
            os.system(cmd)
    if os.path.exists(f'{vid_out[:-4]}_tmp.avi'):
        os.remove(f'{vid_out[:-4]}_tmp.avi')
    print('Finished.')

    return dist_type, dist_level


def write_to_meta_file(meta_path, vid_in, vid_out, dist_type, dist_level):
    # create meta root
    root = os.path.split(meta_path)[0]
    root = '.' if root == '' else root
    os.makedirs(root, exist_ok=True)

    meta_dict = dict()  # a dict of list
    # if exist, get original meta
    if os.path.exists(meta_path):
        f = open(meta_path, 'r')
        lines = f.read().splitlines()
        f.close()
        for l in lines:
            vid_path, dist_meta = l.split()[0], l.split()[1:]
            meta_dict[vid_path] = dist_meta

    # update meta
    meta_list = copy.deepcopy(meta_dict[vid_in]) if vid_in in meta_dict else []
    meta_list.append(f'{dist_type}:{dist_level}')
    meta_dict[vid_out] = meta_list

    # write meta
    f = open(meta_path, 'w')
    for k, v in meta_dict.items():
        f.write(' '.join([k] + v) + '\n')
    f.close()


def main():
    args = parse_args()

    vid_in = args.vid_in
    vid_out = args.vid_out
    type = args.type
    level = args.level
    meta_path = args.meta_path
    via_xvid = args.via_xvid

    # check input args
    assert os.path.exists(vid_in), 'Input video does not exist.'
    assert vid_in != vid_out, ('Paths to the input and output videos '
                               'should NOT be the same.')
    type_list = ['CS', 'CC', 'BW', 'GNC', 'GB', 'JPEG', 'VC', 'random']
    if type not in type_list:
        raise ValueError(
            f"Expect distortion type in {type_list}, but got '{type}'.")
    level_list = ['1', '2', '3', '4', '5', 'random']
    if level not in level_list:
        raise ValueError(
            f"Expect distortion level in {level_list}, but got '{level}'.")

    # add distortion to the input video and write to 'vid_out'
    dist_type, dist_level = distortion_vid(vid_in, vid_out, type, level,
                                           via_xvid)

    # if meta_path is not None, write meta
    if meta_path is not None:
        # write to meta file
        write_to_meta_file(meta_path, vid_in, vid_out, dist_type, dist_level)


if __name__ == '__main__':
    main()
