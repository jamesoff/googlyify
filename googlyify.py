import json
import math
import os
import sys
import boto3
from PIL import Image, ImageDraw, ImageColor


def get_landmark(which, landmarks, width, height):
    for landmark in landmarks:
        if landmark['Type'] == which:
            return (landmark['X'] * width, landmark['Y'] * height)
    return (None, None)


BUCKET = os.environ['GOOGLYIFY_BUCKET']
PREFIX = os.environ['GOOGLYIFY_PREFIX']

filename = sys.argv[1]
try:
    json_filename = sys.argv[2]
except:
    json_filename = None

if not json_filename:
    s3 = boto3.client("s3")
    print("Uploading to S3...")
    with open(filename, "rb") as fh:
        s3.put_object(
            Body=fh,
            Bucket=BUCKET,
            Key="{}/{}".format(PREFIX, filename)
        )

    print("Processing with rekognition...")
    rekognition = boto3.client("rekognition")
    result = rekognition.detect_faces(
        Image={
            "S3Object": {
                'Bucket': BUCKET,
                'Name': '{}/{}'.format(PREFIX, filename)
            }
        }
    )
    fh = open('output.json', 'w')
    json.dump(result, fh)
    fh.close()
else:
    fh = open(json_filename, 'r')
    result = json.load(fh)
    fh.close()

im = Image.open(filename)

width, height = im.size
draw = ImageDraw.Draw(im)
count = 0
for face in result['FaceDetails']:
    count += 1
    left_eye = get_landmark('eyeLeft', face['Landmarks'], width, height)
    right_eye = get_landmark('eyeRight', face['Landmarks'], width, height)
    dist = math.sqrt(((right_eye[0] - left_eye[0])**2)
                     + ((right_eye[1] - left_eye[1])**2)) / 2
    print("l, r: ", left_eye, right_eye)
    print("dist: ", dist)
    print("brightness: ", face['Quality']['Brightness'])
    print("sharpness: ", face['Quality']['Sharpness'])
    print()
    for l in ['eyeLeft', 'eyeRight']:
        (x, y) = get_landmark(l, face['Landmarks'], width, height)
        draw.ellipse([
            x - dist,
            y - dist,
            x + dist,
            y + dist
        ], ImageColor.getrgb("white"))
        draw.ellipse([
            x - (dist / 2),
            y,
            x + (dist / 2),
            y + dist
        ], ImageColor.getrgb("black"))

if count:
    print("Drew eyes on {} face(s)".format(count))

im.save("output.jpg")
