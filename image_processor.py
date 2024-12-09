from PIL import Image, ImageDraw, ImageFont
import os
from tqdm import tqdm

def open_image(image_or_image_path):
    if isinstance(image_or_image_path, Image.Image):
        return image_or_image_path
    elif isinstance(image_or_image_path, str):
        return Image.open(image_or_image_path)
    else:
        raise ValueError("Unsupported input type!")

def dot_matrix_two_dimensional(image_or_image_path, save_path = None, dots_size_w = 6, dots_size_h = 6, save_img = False, font_path = 'fonts/arial.tff'):
    """
    takes an original image as input, save the processed image to save_path. Each dot is labeled with two-dimensional Cartesian coordinates (x,y). Suitable for single-image tasks.
    control args:
    1. dots_size_w: the number of columns of the dots matrix
    2. dots_size_h: the number of rows of the dots matrix
    """
    with open_image(image_or_image_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        draw = ImageDraw.Draw(img, 'RGB')

        width, height = img.size
        grid_size_w = dots_size_w + 1
        grid_size_h = dots_size_h + 1
        cell_width = width / grid_size_w
        cell_height = height / grid_size_h

        font = ImageFont.truetype(font_path, width // 40)  # Adjust font size if needed; default == width // 40

        count = 0
        for j in range(1, grid_size_h):
            for i in range(1, grid_size_w):
                x = int(i * cell_width)
                y = int(j * cell_height)

                pixel_color = img.getpixel((x, y))
                # choose a more contrasting color from black and white
                if pixel_color[0] + pixel_color[1] + pixel_color[2] >= 255 * 3 / 2:
                    opposite_color = (0,0,0)
                else:
                    opposite_color = (255,255,255)

                circle_radius = width // 240  # Adjust dot size if needed; default == width // 240
                draw.ellipse([(x - circle_radius, y - circle_radius), (x + circle_radius, y + circle_radius)], fill=opposite_color)

                text_x, text_y = x + 3, y
                count_w = count // dots_size_w
                count_h = count % dots_size_w
                label_str = f"({count_w+1},{count_h+1})"
                draw.text((text_x, text_y), label_str, fill=opposite_color, font=font)
                count += 1
        if save_img:
            print(">>> dots overlaid image processed, stored in", save_path)
            img.save(save_path)
        return img

def dot_matrix_three_dimensional_single(image_or_image_path, save_path = None, dots_size_w = 6, dots_size_h = 6, first_index = 0, save_img = False):
    """
    takes an original image as input, save the processed image to save_path. Each dot is labeled with three-dimensional Cartesian coordinates (t,x,y). Suitable for image-sequence tasks.
    control args:
    1. dots_size_w: the number of columns of the dots matrix
    2. dots_size_h: the number of rows of the dots matrix
    3. first_index: the value of t-coordinate within this image
    """
    with open_image(image_or_image_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        draw = ImageDraw.Draw(img, 'RGB')

        width, height = img.size
        grid_size_w = dots_size_w + 1
        grid_size_h = dots_size_h + 1
        cell_width = width / grid_size_w
        cell_height = height / grid_size_h

        font = ImageFont.truetype("fonts/arial.ttf", width // 40)  # Adjust font size if needed; default == width // 40

        count = 0
        for j in range(1, grid_size_h):
            for i in range(1, grid_size_w):
                x = i * cell_width
                y = j * cell_height

                pixel_color = img.getpixel((x, y))
                # choose a more contrasting color from black and white
                if pixel_color[0] + pixel_color[1] + pixel_color[2] >= 255 * 3 / 2:
                    opposite_color = (0,0,0)
                else:
                    opposite_color = (255,255,255)

                circle_radius = width // 240  # Adjust dot size if needed; default == width // 240
                draw.ellipse([(x - circle_radius, y - circle_radius), (x + circle_radius, y + circle_radius)], fill=opposite_color)

                text_x, text_y = x + 3, y
                count_w = count // dots_size_w
                count_h = count % dots_size_w
                label_str = f"({first_index},{count_w+1},{count_h+1})"
                draw.text((text_x, text_y), label_str, fill=opposite_color, font=font)
                count += 1

        if save_img:
            print(">>> dots overlaid image processed, stored in", save_path)
            img.save(save_path)
        return img

def dot_matrix_three_dimensional(image_paths, save_paths, dots_size_w, dots_size_h):
    """
    takes original images as input, save dots overlaid images to save_path. apply dot_matrix_three_dimensional_single function to each image sequentially.
    """

    for i, (image_path, save_path) in enumerate(zip(image_paths, save_paths)):
        dot_matrix_three_dimensional_single(image_path, save_path, dots_size_w, dots_size_h, i+1, save_img = True)

def crop_image_coordinates(image_or_image_path, save_path, dots_size_w, dots_size_h, x, y, radius=2, save_img = False):
    """
    crop an local region around the target coordinate (x,y)
    control args:
    1. dots_size_w, dots_size_h: the matrix size of the entire dot matrix
    2. x, y: the target coordinate of the local region
    3. radius: control the size of the cropped region
    """
    with open_image(image_or_image_path) as img:
        width, height = img.size
        grid_size_w = dots_size_w + 1
        grid_size_h = dots_size_h + 1
        cell_width = width / grid_size_w
        cell_height = height / grid_size_h

        x_pixel = cell_height * x
        y_pixel = cell_width * y
        x_pixel_min = max(0, x_pixel - radius * cell_height)
        y_pixel_min = max(0, y_pixel - radius * cell_width)
        x_pixel_max = min(height-1, x_pixel + radius * cell_height)
        y_pixel_max = min(width-1, y_pixel + radius * cell_width)

        cropped_image = img.crop([y_pixel_min, x_pixel_min, y_pixel_max, x_pixel_max])
        if save_img:
            cropped_image.save(save_path)
        return cropped_image

def get_img_files(dir_):
    """
    output the file paths of all the jpg files contained in the target directory
    """
    img_files = []
    for root, _, files in os.walk(dir_):
        for file in files:
            if file.endswith(".jpg"):
                img_files.append(os.path.join(root, file))
    return img_files

def process_imgs_dir(dir_, font_path = 'fonts/arial.tff'):
    """
    process all the images in the target directory: generate all the dots overlaid images
    """
    imgs = get_img_files(dir_)
    imgs = [file for file in imgs if file.endswith(".jpg") and "dots" not in file] # avoid regenerate dots images
    print(">>> find", len(imgs), "images in total.")
    for img_path in tqdm(imgs):
        save_path = img_path.replace(".jpg", f"_dots.jpg")
        grid_size_w, grid_size_h = 6, 6
        try:
            dot_matrix_two_dimensional(img_path, save_path, grid_size_w, grid_size_h, save_img = True, font_path = font_path)
        except Exception as e:
            print(f">>> encountered exceptions: ", e, "when processing image", img_path)
            continue

if __name__=="__main__":
    # TODO process your images here before querying the LMM, an example is as follow.
    process_imgs_dir("data/examples")
