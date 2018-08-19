# Googlyify

Draw googly eyes on people using Amazon Rekognition.

## Prerequisites

* Have AWS credentials configured
* Have an S3 bucket which can be used by the script (to upload the image to, then point Rekognition at)

## Usage

```
export GOOGLYIFY_BUCKET=my.bucket.name
export GOOGLYIFY_PREFIX=googlyify
```

`pipenv run googlyify.py source.jpg`

Will output `output.jpg`. Also outputs `output.json` which is the response from Rekognition. You can pass a JSON file name as a 2nd parameter to skip the upload to S3/call to Rekognition (e.g. for testing the rendering logic)

