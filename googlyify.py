import math
from typing import BinaryIO, Optional, Tuple

import boto3
import typer
from PIL import Image, ImageColor, ImageDraw


def _get_landmark(
    which: str, landmarks: dict, width: int, height: int
) -> Tuple[Optional[int], Optional[int]]:
    """Get the coordinates for a type of landmark"""
    for landmark in landmarks:
        if landmark["Type"] == which:
            return (landmark["X"] * width, landmark["Y"] * height)
    return (None, None)


def process_image(in_file: BinaryIO, out_file: BinaryIO, face_details: dict):
    """Draw eyes on an image based on Rekognition results"""
    image = Image.open(in_file)

    width, height = image.size
    draw = ImageDraw.Draw(image)
    count = 0
    for face in face_details:
        count += 1
        left_eye = _get_landmark("eyeLeft", face["Landmarks"], width, height)
        right_eye = _get_landmark("eyeRight", face["Landmarks"], width, height)
        if left_eye[0] is None or left_eye[1] is None:
            continue
        if right_eye[0] is None or right_eye[1] is None:
            continue
        dist = (
            math.sqrt(
                ((right_eye[0] - left_eye[0]) ** 2)
                + ((right_eye[1] - left_eye[1]) ** 2)
            )
            / 2
        )
        print("l, r: ", left_eye, right_eye)
        print("dist: ", dist)
        print("brightness: ", face["Quality"]["Brightness"])
        print("sharpness: ", face["Quality"]["Sharpness"])
        print()
        for eye in [left_eye, right_eye]:
            (x, y) = eye
            if x is None or y is None:
                # already guarded against above, but need to convince the type checker
                continue
            draw.ellipse(
                [x - dist, y - dist, x + dist, y + dist], ImageColor.getrgb("white")
            )
            draw.ellipse(
                [x - (dist / 2), y, x + (dist / 2), y + dist],
                ImageColor.getrgb("black"),
            )
    if count:
        print(f"Drew eyes on {count} face(s)")
    image.save(out_file)


def main(infile: str, outfile: str):
    """Draw googly eyes on faces in an image"""

    with open(infile, "rb") as in_file_handle:
        rekognition = boto3.client("rekognition")
        result = rekognition.detect_faces(
            Image={"Bytes": in_file_handle.read()}
        )
        in_file_handle.seek(0)
        with open(outfile, "wb") as out_file_handle:
            process_image(in_file_handle, out_file_handle, result["FaceDetails"])
            print(f"Save to {outfile}")


if __name__ == "__main__":
    typer.run(main)
