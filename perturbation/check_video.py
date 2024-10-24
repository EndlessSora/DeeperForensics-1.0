import argparse
import os
import cv2

def parse_args():
    parser = argparse.ArgumentParser(description='Check video information.')
    parser.add_argument('--vid_in', type=str, required=True, help='Path to the input video')
    parser.add_argument('--vid_out', type=str, required=True, help='Path to the output video')
    return parser.parse_args()

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

    if not os.path.exists(vid_in):
        raise FileNotFoundError('Input video does not exist.')
    
    if not os.path.exists(vid_out):
        raise FileNotFoundError('Output video does not exist.')

    try:
        vid1 = cv2.VideoCapture(vid_in)
        if not vid1.isOpened():
            raise RuntimeError('Could not open input video.')

        w1, h1, fps1, fourcc1, frame_count1 = get_vid_info(vid1)
        vid1.release()

        vid2 = cv2.VideoCapture(vid_out)
        if not vid2.isOpened():
            raise RuntimeError('Could not open output video.')

        w2, h2, fps2, fourcc2, frame_count2 = get_vid_info(vid2)
        vid2.release()

    except Exception as e:
        print(f"Error occurred: {e}")
        return

    # Check video properties
    if w1 != w2:
        raise ValueError(f'Frame width mismatch: {w1} in input vs {w2} in output.')
    if h1 != h2:
        raise ValueError(f'Frame height mismatch: {h1} in input vs {h2} in output.')
    if fps1 != fps2:
        raise ValueError(f'FPS mismatch: {fps1} in input vs {fps2} in output.')
    if fourcc1 != fourcc2:
        raise ValueError(f'FOURCC mismatch: {fourcc1} in input vs {fourcc2} in output.')
    if frame_count1 != frame_count2:
        raise ValueError(f'Frame count mismatch: {frame_count1} in input vs {frame_count2} in output.')

    print('No problem.')

if __name__ == '__main__':
    main()
