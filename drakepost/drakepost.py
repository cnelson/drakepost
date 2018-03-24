import argparse
from io import BytesIO
import os.path
import sys

from PIL import Image
import requests


def resize_square(img, size):
    """Resize an image to be square.

    Image will be enlarged or shrunk as needed

    Args:
        image (PIL.Image): The image to resize
        size (int): Resize to size x size px

    Returns:
        PIL.Image: The resized image
    """

    # already that size? bail
    if img.size == (size, size):
        return img

    # scale up so our smallest dimension equales the request size
    if img.size[0] < img.size[1]:
        target_width = size
        target_height = int(size * img.size[1] / img.size[0])
    else:
        target_height = size
        target_width = int(size * img.size[0] / img.size[1])

    img = img.resize((target_width, target_height), Image.ANTIALIAS)

    # return the square result cropped from the upper left corner
    return img.crop((0, 0, size, size))


def drakepost(no_query, yes_query, search_engine_id, google_key=""):
    """Generate a do like / like drake meme

    Args:
        no_query (str): Drake doens't like this.
        yes_query (str): Drake lists this
        search_engine_id (str): Search engine id from https://cse.google.com
        google_key(str): Key from
                https://console.developers.google.com/apis/credentials

    Raises:
        RuntimeError: Couldn't make memes

    Returns:
        PIL.Image: The image
    """

    basedir = os.path.dirname(__file__)

    no = Image.open(os.path.join(basedir, "data/drake/no.png"))
    yes = Image.open(os.path.join(basedir, "data/drake/yes.png"))

    meme = Image.new('RGB', [x * 2 for x in no.size])
    meme.paste(no, (0, 0))
    meme.paste(yes, (0,  no.size[1]))

    no_json = requests.get(
        "https://www.googleapis.com/customsearch/v1",
        params={
            "key": google_key,
            "cx": search_engine_id,
            "q": no_query,
            "imgSize": "xxlarge",
            "safe": "off",
            "searchType": "image"
        }
    ).json()

    try:
        no_image = Image.open(BytesIO(
            requests.get(no_json['items'][0]['link']).content
        ))
        meme.paste(resize_square(no_image, no.size[0]), (no.size[0], 0))
    except KeyError:
        raise RuntimeError(no_json['error']['message'])

    try:
        yes_json = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": google_key,
                "cx": search_engine_id,
                "q": yes_query,
                "imgSize": "xxlarge",
                "safe": "off",
                "searchType": "image"
            }
        ).json()

        yes_image = Image.open(BytesIO(
            requests.get(yes_json['items'][0]['link']).content
        ))
    except KeyError:
        raise RuntimeError(yes_json['error']['message'])

    meme.paste(resize_square(yes_image, no.size[0]), no.size)

    return meme


def main():
    parser = argparse.ArgumentParser(
        description="Drakepost via AI BLOCKCHAIN"
    )
    parser.add_argument("dont_like", help="Drake doesn't like this")
    parser.add_argument("like", help="Drake likes this")
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="meme filename, stdout if not provided"
    )
    parser.add_argument(
        "-s",
        "--search-engine-id",
        default="008843026399724955227:wkjgzvekqio",
        help="Search engine id from https://cse.google.com"
    )
    parser.add_argument(
        "-k",
        "--key",
        default="",
        help="Key from https://console.developers.google.com/apis/credentials"
        "' use if you get 'Bad Request' errors"
    )

    args = parser.parse_args()

    try:
        meme = drakepost(
            args.dont_like,
            args.like,
            args.search_engine_id,
            args.key
        )

        if args.output is None:
            meme.save(sys.stdout.buffer, format="PNG")
        else:
            meme.save(args.output)
    except RuntimeError as exc:
        parser.error("Failed to make meme: {}".format(exc))


if __name__ == "__main__":
    main()
