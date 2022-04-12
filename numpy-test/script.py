from argparse import ArgumentError
from calendar import c
import json
from multiprocessing.sharedctypes import Value
import re
from tkinter.tix import IMAGE
from urllib.parse import _NetlocResultMixinStr
import cv2
import click
from cv2 import SparsePyrLKOpticalFlow_create
from cv2 import bilateralFilter
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import glob

LINE_THICKNESS = 2


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        if width > w:
            return image
        r = width / float(w)
        dim = (width, int(h * r))
    return cv2.resize(image, dim, interpolation=inter)


def show_image(image, name="image"):
    resize = ResizeWithAspectRatio(image, width=1280)
    cv2.imshow(name, resize)
    cv2.waitKey(0)


def replace_black_with_white(image):
    black_pixels = np.where(
        (image[:, :, 0] < 10) & (image[:, :, 1] < 10) & (image[:, :, 2] < 10)
    )
    # set those pixels to white
    image[black_pixels] = [255, 255, 255]
    return image


def find_princ_colors(image):
    COLOR_BUMP = 60
    pixels = np.float32(image.reshape(-1, 3))
    n_colors = 1
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    color = [round(x) for x in list(dominant)]
    return [x + COLOR_BUMP if x < (255 - COLOR_BUMP) else 255 for x in color]


def remove_text(image, color):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, close_kernel, iterations=1)

    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dilate = cv2.dilate(close, dilate_kernel, iterations=1)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 200 and area < 20000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(
                image, (x, y), (x + w, y + h), (color[0], color[1], color[2]), -1
            )
    return image


def get_mode(img):
    unq, count = np.unique(img.reshape(-1, img.shape[-1]), axis=0, return_counts=True)

    result = list(unq[count.argmax()])
    pixel_count = count[count.argmax()]
    fraction = pixel_count / img.shape[1]
    result.reverse()
    return (result, fraction)


def get_horizontal_lines(image, original=None, offset=0, color=None):
    IMAGE_HEIGHT = 420
    IMAGE_HEIGHT_WITH_TITLE = 510
    FRACTION_TRESHOLD = 0.1
    values = []
    deltas = []
    # show_image(image)
    # iterate over row of pixels and calculate average value
    # big changes in av. value signify start of new row of images
    while image.shape[0] > 0:
        crop_img = image[:1, :]
        image = image[1:, :]
        current_val = np.average(crop_img)
        if len(values) > 0:
            prev_val = values[-1]
            delta = abs(current_val - prev_val)
            deltas.append(delta)
        values.append(current_val)

    vals = [i for i, x in enumerate(deltas) if x > 10]

    first = vals.pop(0)

    while True:
        if original is None:
            break
        original_pos = first + offset

        # get modal value of next and previous scanline
        m_next, fraction_next = get_mode(
            original[original_pos + 1 : original_pos + 2, :]
        )
        m_prev, fraction_prev = get_mode(original[original_pos - 1 : original_pos, :])

        # if either modal val is equal to the blank out color for text ignore
        # and try the next line

        if (
            m_next == color
            and fraction_next > FRACTION_TRESHOLD
            or m_prev == color
            and fraction_prev > FRACTION_TRESHOLD
        ):
            if len(vals) == 0:
                break
            first = vals.pop(0)
            continue
        break
    first_half = first + IMAGE_HEIGHT
    first_end = first + IMAGE_HEIGHT_WITH_TITLE

    return [first, first_half, first_end]


def get_vertical_lines(image):
    IMAGE_HEIGHT = 762
    IMAGE_GUTTER = 50
    values = []
    deltas = []
    # iterate over row of pixels and calculate average value
    # big changes in av. value signify start of new row of images
    # find first column of images then assume default image_width and image_gutter
    image = np.transpose(image)

    # find first column of images
    while image.shape[0] > 0:
        crop_img = image[:1, :]
        image = image[1:, :]
        current_val = np.average(crop_img)
        if len(values) > 0:
            prev_val = values[-1]
            delta = abs(current_val - prev_val)
            deltas.append(delta)
        values.append(current_val)
    vals = [i for i, x in enumerate(deltas) if x > 3]
    lines = []
    val = vals[0]
    # find remaining image lines
    for _ in range(3):
        val_end = val + IMAGE_HEIGHT
        lines.extend([val, val_end])
        val = val_end + IMAGE_GUTTER
    return lines


def is_even_filepath(filepath):
    result = re.search(r"batch-[0-9]+-([0-9]+)\.jpg", filepath)
    i_string = result.group(1)
    i = int(i_string)
    if (i % 2) == 0:
        return True
    return False


def process_front_page(filepath):
    raise NotImplementedError()


def draw_hor_lines(image, hor_lines):
    _, width, _ = image.shape
    for val in hor_lines:
        cv2.line(
            image,
            (0, val),
            (width, val),
            (0, 255, 0),
            thickness=LINE_THICKNESS,
        )


def draw_ver_lines(image, ver_lines):
    height, _, _ = image.shape
    for val in ver_lines:
        cv2.line(
            image,
            (val, 0),
            (val, height),
            (0, 255, 0),
            thickness=LINE_THICKNESS,
        )


def get_image_bboxes(hor_lines, ver_lines):
    hor_borders = []
    for i in range(0, len(hor_lines) - 1, 3):
        bbox = {"miny": hor_lines[i], "maxy": hor_lines[i + 1]}
        hor_borders.append(bbox)
    bboxes = []
    for hor_border in hor_borders:
        for i in range(0, len(ver_lines) - 1, 2):
            bbox = hor_border | {"minx": ver_lines[i], "maxx": ver_lines[i + 1]}
            bboxes.append(bbox)
    return bboxes


def get_title_bboxes(hor_lines, ver_lines):
    hor_borders = []
    for i in range(0, len(hor_lines) - 1, 3):
        bbox = {"miny": hor_lines[i + 1], "maxy": hor_lines[i + 2]}
        hor_borders.append(bbox)
    bboxes = []
    for hor_border in hor_borders:
        for i in range(0, len(ver_lines) - 1, 2):
            bbox = hor_border | {"minx": ver_lines[i], "maxx": ver_lines[i + 1]}
            bboxes.append(bbox)
    return bboxes


def get_recipe_step_bboxes(filepath):
    CROP_TOP = 20
    CROP_BOTTOM = 200
    CROP_LEFT = 855
    CROP_RIGHT = 40

    image = cv2.imread(filepath)  # reads an image in the BGR format
    color = find_princ_colors(image)
    height, width, _ = image.shape

    image = image[CROP_TOP : height - CROP_BOTTOM, CROP_LEFT : width - CROP_RIGHT]

    image = remove_text(image, color)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width, _ = image.shape

    hor_lines = get_all_hor_lines(image, color, height, gray)
    ver_lines = get_vertical_lines(gray)

    assert len(hor_lines) == 6, "expected nr of horizontal lines to be 6"
    assert len(ver_lines) == 6, "expected nr of vertical lines to be 6"

    image_bboxes = get_image_bboxes(hor_lines, ver_lines)
    title_bboxes = get_title_bboxes(hor_lines, ver_lines)
    desc_bboxes  = get_description_bboxes(image_bboxes, title_bboxes, height, CROP_BOTTOM)

    image_bboxes=[{"minx": x["minx"]+CROP_LEFT,"miny": x["miny"]+CROP_TOP, "maxy": x["maxy"]+CROP_TOP, "maxx": x["maxx"]+CROP_LEFT} for x in image_bboxes]
    title_bboxes=[{"minx": x["minx"]+CROP_LEFT,"miny": x["miny"]+CROP_TOP, "maxy": x["maxy"]+CROP_TOP, "maxx": x["maxx"]+CROP_LEFT} for x in title_bboxes]
    desc_bboxes=[{"minx": x["minx"]+CROP_LEFT,"miny": x["miny"]+CROP_TOP, "maxy": x["maxy"]+CROP_TOP, "maxx": x["maxx"]+CROP_LEFT} for x in desc_bboxes]
    return {
        "images": image_bboxes,
        "titles": title_bboxes,
        "description": desc_bboxes,
    }

def get_description_bboxes(image_bboxes, title_bboxes, image_height, crop_bottom):
    result = []
    for i in range(0,3):
        bottom_bbox = title_bboxes[i]
        top_bbox = image_bboxes[i+3]
        miny = bottom_bbox["maxy"]
        maxy = top_bbox["miny"]
        minx = bottom_bbox["minx"]
        maxx = bottom_bbox["maxx"]
        result.append({
            "minx":minx, "maxx":maxx, "miny": miny, "maxy":maxy
        })
    for i in range(3,6):
        bottom_bbox = title_bboxes[i]
        miny = bottom_bbox["maxy"]
        maxy = image_height
        minx = bottom_bbox["minx"]
        maxx = bottom_bbox["maxx"]
        result.append({
            "minx":minx, "maxx":maxx, "miny": miny, "maxy":maxy
        })
    return result



def draw_bboxes(image, image_bboxes, color=(0, 255, 0)):
    for box in image_bboxes:
        top_left = (box["minx"], box["maxy"])
        bottom_right = (box["maxx"], box["miny"])
        cv2.rectangle(image, top_left, bottom_right, color, 2)


def get_all_hor_lines(original_image, color, height, image):
    hor_lines = get_horizontal_lines(image)
    offset = hor_lines[2] + 10
    image = image[offset:height, :]
    second_hor_lines = get_horizontal_lines(image, original_image, offset, color)
    second_hor_lines = [x + offset for x in second_hor_lines]
    hor_lines.extend(second_hor_lines)
    return hor_lines


def process_back_page(filepath):
    bboxes = get_recipe_step_bboxes(filepath)
    image = cv2.imread(filepath)
    draw_bboxes(image, bboxes["images"])
    draw_bboxes(image, bboxes["titles"], (255,0,0))
    draw_bboxes(image, bboxes["description"], (255,255,0))
    show_image(image)


@click.command()
@click.option("-f", "--input-file", type=click.Path(exists=True))
@click.option("-d", "--input-dir", type=click.Path(exists=True))
def main(input_file, input_dir):
    if not input_file and not input_dir:
        raise ValueError(
            "either --input-file or --input-dir should be supplied as argument"
        )

    even_files = []
    uneven_files = []

    if input_dir:
        files_glob = glob.glob(f"{input_dir}/*.jpg")
        for filepath in files_glob:
            if is_even_filepath(filepath):
                even_files.append({"back": filepath})
            else:
                uneven_files.append({"front": filepath})
        even_files = sorted(even_files, key=lambda i: i["back"])

        uneven_files = sorted(uneven_files, key=lambda i: i["front"])
        all_files = []
        for x, y in zip(even_files, uneven_files):
            all_files.append(x | y)

        for item in all_files:
            # json = process_front_page(item["front"])
            json = process_back_page(item["back"])

    else:
        if is_even_filepath(input_file):
            process_back_page(input_file)
        # else:
        #     process_front_page(input_file)


if __name__ == "__main__":
    main()
