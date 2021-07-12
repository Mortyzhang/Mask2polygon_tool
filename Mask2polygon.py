from PIL import Image
import numpy as np
from skimage import measure
from shapely.geometry import Polygon, MultiPolygon
import json
import os


def create_sub_masks(mask_image):
    width, height = mask_image.size

    # Initialize a dictionary of sub-masks indexed by RGB colors
    sub_masks = {}
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            pixel = mask_image.getpixel((x, y))[:3]

            # If the pixel is not black...
            if pixel != (0, 0, 0):
                # Check to see if we've created a sub-mask...
                pixel_str = str(pixel)
                sub_mask = sub_masks.get(pixel_str)
                if sub_mask is None:
                   # Create a sub-mask (one bit per pixel) and add to the dictionary
                    # Note: we add 1 pixel of padding in each direction
                    # because the contours module doesn't handle cases
                    # where pixels bleed to the edge of the image
                    sub_masks[pixel_str] = Image.new('1', (width+2, height+2))

                # Set the pixel value to 1 (default is 0), accounting for padding
                sub_masks[pixel_str].putpixel((x+1, y+1), 1)

    return sub_masks


def create_sub_mask_annotation(sub_mask, image_id, category_id, annotation_id, is_crowd):
    # Find contours (boundary lines) around each sub-mask
    # Note: there could be multiple contours if the object
    # is partially occluded. (E.g. an elephant behind a tree)
    contours = measure.find_contours(np.array(sub_mask), 0.5, positive_orientation='low')

    segmentations = []
    polygons = []
    for contour in contours:
        # Flip from (row, col) representation to (x, y)
        # and subtract the padding pixel
        for i in range(len(contour)):
            row, col = contour[i]
            contour[i] = (col - 1, row - 1)

        # Make a polygon and simplify it
        poly = Polygon(contour)
        poly = poly.simplify(1.0, preserve_topology=False)
        polygons.append(poly)
        segmentation = np.array(poly.exterior.coords)
        segmentation = np.maximum(segmentation, 0).ravel().tolist()
        segmentations.append(segmentation)

    # Combine the polygons to calculate the bounding box and area
    multi_poly = MultiPolygon(polygons)
    if multi_poly.bounds == ():
        return "skip"
    x, y, max_x, max_y = multi_poly.bounds
    # x = max(0, x)
    # y = max(0, y)
    width = max_x - x
    height = max_y - y
    bbox = (x, y, width, height)
    area = multi_poly.area

    annotation = {
        'segmentation': segmentations,
        'iscrowd': is_crowd,
        'image_id': image_id,
        'category_id': category_id,
        'id': annotation_id,
        'bbox': bbox,
        'area': area
    }

    return annotation


def get_name(root, mode_folder=True):
    for root, dirs, file in os.walk(root):
        if mode_folder:
            return sorted(dirs)
        else:
            return sorted(file)


def get_annotation(mask_image_root):
    dataset = {"info": {"year": 2021, "version": "2021", "description": "zjx", "contributor": "zjx", "url": "",
                        "date_created": "2021.07.06"},
               "license": {"id": 1, "url": "", "name": "zhangjiaxin"},
               "images": [],
               "annotations": [],
               "categories": []}
    class_index = {1: "building"}
    for s, k in enumerate(list(class_index.keys())):
        dataset["categories"].append({"id": k, "name": class_index[k], "supercategory": "building"})

    is_crowd = 0

    # These ids will be automatically increased as we go
    annotation_id = 0
    image_id = 0

    # Create the annotations
    for i, root in enumerate(mask_image_root):
        print(i)
        mask_image = Image.open(rrr + root)
        print(root)
        weight, height = mask_image.size
        file_name = "rgb_" + root.split("/")[-1].split("_")[-1]
        print(file_name)
        dataset["images"].append({"license": 1,
                                  "file_name": file_name,
                                  "id": i,
                                  "weight": weight,
                                  "height": height})
        sub_masks = create_sub_masks(mask_image)
        for color, sub_mask in sub_masks.items():
            category_id = 1
            annotation = create_sub_mask_annotation(sub_mask, image_id, category_id, annotation_id, is_crowd)
            if annotation == "skip":
                continue
            dataset["annotations"].append(annotation)
            annotation_id += 1
        image_id += 1
    with open("building1.json", "w") as f:
        json.dump(dataset, f)


rrr = "./InstanceSegmentation/"
all_root = get_name(rrr, mode_folder=False)
get_annotation(all_root)