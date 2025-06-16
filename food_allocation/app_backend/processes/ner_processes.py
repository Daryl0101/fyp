from rest_framework import serializers
import json
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os
import google.generativeai as genai

# region Gemini Configs
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 300,
    "response_mime_type": "application/json",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction='serving size, carbohydrate, protein, fat, sugar, fiber and saturated fat in grams\ncalorie in kcal\ncholesterol and sodium in mg\nOnly return the input into the fields below strictly by following the units:\n{\n"serving_size": {float only},\n"calorie": {float only},\n"carbohydrate": {float only},\n"protein": {float only},\n"fat": {float only},\n"sugar": {float only},\n"fiber": {float only},\n"saturated_fat": {float only},\n"cholesterol": {float only},\n"sodium": {float only},\n}',
)


def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


# region Crop Function
def crop(image_obj, coords, saved_location, extend_ratio=0, SAVE=False):
    """
    @param image_path: The image object to be cropped
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    @param extend_ratio: The value by which the bounding boxes to be extended to accomodate the text that has been cut
    @param SAVE: whether to save the cropped image or not
    """
    nx = image_obj.shape[1]
    ny = image_obj.shape[0]

    modified_coords = (
        int(coords[0] - extend_ratio * nx) if coords[0] - extend_ratio * nx > 0 else 0,
        int(coords[1] - extend_ratio * ny) if coords[1] - extend_ratio * ny > 0 else 0,
        (
            int(coords[2] + extend_ratio * nx)
            if coords[2] + extend_ratio * nx < nx
            else nx
        ),
        (
            int(coords[3] + extend_ratio * ny)
            if coords[3] + extend_ratio * ny < ny
            else ny
        ),
    )
    # cropped_image = image_obj.crop(modified_coords)
    cropped_image = image_obj[
        modified_coords[1] : modified_coords[3], modified_coords[0] : modified_coords[2]
    ]

    if SAVE:
        try:
            cv2.imwrite(saved_location, cropped_image)
        except Exception as e:
            print(e)

    return cropped_image


# endregion


# region OCR Functions
def preprocess_for_ocr(img, enhance=1):
    """
    @param img: image to which the pre-processing steps being applied
    """
    if enhance > 1:
        img = Image.fromarray(img)

        contrast = ImageEnhance.Contrast(img)

        img = contrast.enhance(enhance)

        img = np.asarray(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # img = cv2.GaussianBlur(img, (5,5), 0)

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    return img


# endregion


# region Text Detection Functions
def resize_image(im, scale, max_scale=None):
    f = float(scale) / min(im.shape[0], im.shape[1])
    if max_scale != None and f * max(im.shape[0], im.shape[1]) > max_scale:
        f = float(max_scale) / max(im.shape[0], im.shape[1])
    return cv2.resize(im, None, None, fx=f, fy=f, interpolation=cv2.INTER_LINEAR), f


def draw_boxes(img, image_name, boxes, scale):
    base_name = image_name.split("/")[-1]
    with open("data/results/" + "res_{}.txt".format(base_name.split(".")[0]), "w") as f:
        for box in boxes:
            if (
                np.linalg.norm(box[0] - box[1]) < 5
                or np.linalg.norm(box[3] - box[0]) < 5
            ):
                continue
            if box[8] >= 0.9:
                color = (0, 255, 0)
            elif box[8] >= 0.8:
                color = (255, 0, 0)
            cv2.line(
                img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2
            )
            cv2.line(
                img, (int(box[0]), int(box[1])), (int(box[4]), int(box[5])), color, 2
            )
            cv2.line(
                img, (int(box[6]), int(box[7])), (int(box[2]), int(box[3])), color, 2
            )
            cv2.line(
                img, (int(box[4]), int(box[5])), (int(box[6]), int(box[7])), color, 2
            )

            min_x = min(
                int(box[0] / scale),
                int(box[2] / scale),
                int(box[4] / scale),
                int(box[6] / scale),
            )
            min_y = min(
                int(box[1] / scale),
                int(box[3] / scale),
                int(box[5] / scale),
                int(box[7] / scale),
            )
            max_x = max(
                int(box[0] / scale),
                int(box[2] / scale),
                int(box[4] / scale),
                int(box[6] / scale),
            )
            max_y = max(
                int(box[1] / scale),
                int(box[3] / scale),
                int(box[5] / scale),
                int(box[7] / scale),
            )

            line = ",".join([str(min_x), str(min_y), str(max_x), str(max_y)]) + "\r\n"
            f.write(line)

    img = cv2.resize(
        img, None, None, fx=1.0 / scale, fy=1.0 / scale, interpolation=cv2.INTER_LINEAR
    )
    cv2.imwrite(os.path.join("app_backend/lib/data/results", base_name), img)


# endregion


def detect_advanced(img_obj: Image):
    """
    This function uses Gemini API to extract the nutrient labels and their values from the image
    @param img_path: Pathto the image for which labels to be extracted
    """
    image = cv2.cvtColor(np.array(img_obj), cv2.COLOR_RGB2BGR)

    response = model.generate_content(Image.fromarray(image))
    nutrient_dict = json.loads(response.text)

    # Throw error if Gemini returns invalid keys
    if list(nutrient_dict.keys()) != [
        "serving_size",
        "calorie",
        "carbohydrate",
        "protein",
        "fat",
        "sugar",
        "fiber",
        "saturated_fat",
        "cholesterol",
        "sodium",
    ]:
        raise serializers.ValidationError("Invalid keys returned by Gemini!")

    # Convert the values to float & type guard if Gemini returns invalid values
    for i in nutrient_dict.keys():
        try:
            nutrient_dict[i] = float(nutrient_dict[i])
        except:
            nutrient_dict[i] = 0

    return nutrient_dict
