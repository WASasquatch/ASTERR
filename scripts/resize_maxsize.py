# Inside functions, we must import our modules as they are scoped from the main script
# tensor2pil() and pil2tensor() are built-in methods to help with `IMAGE` input

# a = image (tensor batched image)
# b = max size (INT)

def resizeImage(image, max_size):
    import PIL
    width, height = image.size
    new_width, new_height = width, height

    if width > max_size or height > max_size:
        ratio = min(max_size / width, max_size / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

    elif max_size > max(width, height):
        ratio = max_size / max(width, height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

    resized_image = image.resize((new_width, new_height))
    return resized_image


# We define the result to return to the node with the `asterr_result` var
asterr_result = pil2tensor(resizeImage(tensor2pil(a), b))
