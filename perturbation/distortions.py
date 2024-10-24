import math
import os
import random
import cv2
import numpy as np

def bgr2ycbcr(img_bgr):
    """
    Convert BGR image to YCbCr color space.

    Args:
        img_bgr (np.ndarray): Input image in BGR format.

    Returns:
        np.ndarray: Image converted to YCbCr format.
    """
    img_bgr = img_bgr.astype(np.float32)
    img_ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCR_CB)
    img_ycbcr = img_ycrcb[:, :, (0, 2, 1)]
    
    # Scale to [16/255, 235/255] for Y and [16/255, 240/255] for Cb and Cr
    img_ycbcr[:, :, 0] = (img_ycbcr[:, :, 0] * (235 - 16) + 16) / 255.0
    img_ycbcr[:, :, 1:] = (img_ycbcr[:, :, 1:] * (240 - 16) + 16) / 255.0
    
    return img_ycbcr

def ycbcr2bgr(img_ycbcr):
    """
    Convert YCbCr image back to BGR color space.

    Args:
        img_ycbcr (np.ndarray): Input image in YCbCr format.

    Returns:
        np.ndarray: Image converted to BGR format.
    """
    img_ycbcr = img_ycbcr.astype(np.float32)
    
    # Scale back to [0, 1]
    img_ycbcr[:, :, 0] = (img_ycbcr[:, :, 0] * 255.0 - 16) / (235 - 16)
    img_ycbcr[:, :, 1:] = (img_ycbcr[:, :, 1:] * 255.0 - 16) / (240 - 16)
    
    img_ycrcb = img_ycbcr[:, :, (0, 2, 1)]
    img_bgr = cv2.cvtColor(img_ycrcb, cv2.COLOR_YCR_CB2BGR)
    
    return img_bgr

def color_saturation(img, param):
    """
    Adjust the color saturation of the image.

    Args:
        img (np.ndarray): Input image in BGR format.
        param (float): Saturation adjustment factor (1.0 = no change).

    Returns:
        np.ndarray: Saturated image in BGR format.
    """
    ycbcr = bgr2ycbcr(img)
    ycbcr[:, :, 1] = np.clip(0.5 + (ycbcr[:, :, 1] - 0.5) * param, 0, 1)
    ycbcr[:, :, 2] = np.clip(0.5 + (ycbcr[:, :, 2] - 0.5) * param, 0, 1)
    
    img = ycbcr2bgr(ycbcr).astype(np.uint8)
    return img

def color_contrast(img, param):
    """
    Adjust the contrast of the image.

    Args:
        img (np.ndarray): Input image in BGR format.
        param (float): Contrast adjustment factor (1.0 = no change).

    Returns:
        np.ndarray: Contrast-adjusted image in BGR format.
    """
    img = np.clip(img.astype(np.float32) * param, 0, 255).astype(np.uint8)
    return img

def block_wise(img, param):
    """
    Apply block-wise masking on the image.

    Args:
        img (np.ndarray): Input image in BGR format.
        param (int): Number of blocks to mask.

    Returns:
        np.ndarray: Image with block masking applied.
    """
    width = 8
    block = np.ones((width, width, 3), dtype=np.uint8) * 128
    num_blocks = min(img.shape[0] * img.shape[1] // (width * width), param)
    
    for _ in range(num_blocks):
        r_w = random.randint(0, img.shape[1] - width)
        r_h = random.randint(0, img.shape[0] - width)
        img[r_h:r_h + width, r_w:r_w + width, :] = block
    
    return img

def gaussian_noise_color(img, param):
    """
    Add Gaussian noise to the image.

    Args:
        img (np.ndarray): Input image in BGR format.
        param (float): Standard deviation of the Gaussian noise.

    Returns:
        np.ndarray: Noisy image in BGR format.
    """
    noise = np.random.normal(0, math.sqrt(param), img.shape).astype(np.float32)
    noisy_img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    return noisy_img

def gaussian_blur(img, param):
    """
    Apply Gaussian blur to the image.

    Args:
        img (np.ndarray): Input image in BGR format.
        param (int): Kernel size for the blur (should be odd).

    Returns:
        np.ndarray: Blurred image in BGR format.
    """
    if param % 2 == 0:
        param += 1  # Ensure kernel size is odd
    img = cv2.GaussianBlur(img, (param, param), param / 6)
    return img

def jpeg_compression(img, param):
    """
    Compress the image using JPEG compression.

    Args:
        img (np.ndarray): Input image in BGR format.
        param (int): Quality factor (1-100, where 100 is highest quality).

    Returns:
        np.ndarray: JPEG-compressed image in BGR format.
    """
    if not (1 <= param <= 100):
        raise ValueError("JPEG quality parameter must be between 1 and 100.")
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), param]
    _, img_encoded = cv2.imencode('.jpg', img, encode_param)
    img_decoded = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
    
    return img_decoded

def video_compression(vid_in, vid_out, param):
    """
    Compress a video using FFmpeg.

    Args:
        vid_in (str): Input video file path.
        vid_out (str): Output video file path.
        param (int): Constant Rate Factor (CRF) for quality control.

    Raises:
        RuntimeError: If the compression command fails.
    """
    cmd = f'ffmpeg -i "{vid_in}" -crf {param} -y "{vid_out}"'
    if os.system(cmd) != 0:
        raise RuntimeError(f'Video compression failed for {vid_in}.')

