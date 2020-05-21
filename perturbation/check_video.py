import argparse
import os

import cv2


def parse_args():
    parser = argparse.ArgumentParser(description='Check video information.')
    parser.add_argument('--vid_in',
                        type=str,
                        required=True,
                        help='path to the input video')
    parser.add_argument('--vid_out',
                        type=str,
                        required=True,
                        help='path to the output video')
    args = parser.parse_args()

    return args


def get_vid_info(vid):
    w = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = vid.get(cv2.CAP_PROP_FPS)
    fourcc = vid.get(cv2.CAP_PROP_FOURCC)
    frame_count = vid.get(cv2.CAP_PROP_FRAME_COUNT)

    return w, h, fps, fourcc, frame_count


def main():
    args = parse_args()

    vid_in = args.vid_in
    vid_out = args.vid_out

    # check input args
    assert os.path.exists(vid_in), 'Input video does not exist.'
    assert os.path.exists(vid_out), 'Output video does not exist.'

    # check video info
    vid1 = cv2.VideoCapture(vid_in)
    w1, h1, fps1, fourcc1, frame_count1 = get_vid_info(vid1)
    vid1.release()
    vid2 = cv2.VideoCapture(vid_out)
    w2, h2, fps2, fourcc2, frame_count2 = get_vid_info(vid2)
    vid2.release()
    assert w1 == w2, ('Frame width should be the same, '
                      f'but got {w1} in input video, {w2} in output video.')
    assert h1 == h2, ('Frame height should be the same, '
                      f'but got {h1} in input video, {h2} in output video.')
    assert fps1 == fps2, ('Video fps should be the same, but got '
                          f'{fps1} in input video, {fps2} in output video.')
    assert fourcc1 == fourcc2, ('Video fourcc should be the same, but got '
                                f'{fourcc1} in input video, {fourcc2} in '
                                'output video.')
    assert frame_count1 == frame_count2, ('Frame count should be the same, '
                                          f'but got {frame_count1} in '
                                          f'input video, {frame_count2} in '
                                          'output video.')

    # pass all assertions, succeed
    print('No problem.')


if __name__ == '__main__':
    main()
