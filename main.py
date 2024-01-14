from PIL import Image, ImageFilter

colors = [(217, 30, 24),(230, 126, 35), (249, 191, 59), (47, 204, 113), (27, 181, 254), (31, 58, 147), (246, 36, 150), (154, 19, 179), 
          (149, 65, 27), (174, 184, 184), (255, 255, 255)]

def eroziya(cycles, image):
    for _ in range(cycles):
        image = image.filter(ImageFilter.MinFilter(3))
    return image
 
def dilatatsiya(cycles, image):
    for _ in range(cycles):
        image = image.filter(ImageFilter.MaxFilter(3))
    return image

def isSemiColor(color1, color2):
    return (abs(color1[0] - color2[0]) <= 30 and
                abs(color1[1] - color2[1]) <= 30 and
                abs(color1[2] - color2[2]) <= 30)

def inColorScheme(color, colorScheme):
    for i in range(len(colorScheme)):
        if(isSemiColor(color, colorScheme[i])):
            return i
    return False

def pixelate(image, pixel_size=9, draw_margin=True):
    margin_color = (0, 0, 0)

    image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST)
    image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST)
    pixel = image.load()

    # Draw black margin between pixels
    if draw_margin:
        for i in range(0, image.size[0], pixel_size):
            for j in range(0, image.size[1], pixel_size):
                for r in range(pixel_size):
                    pixel[i+r, j] = margin_color
                    pixel[i, j+r] = margin_color

    return image

def changeColors(image, colorScheme = []):
    pixel = image.load()
    for i in range(0, image.size[0]):
        for j in range(0, image.size[1]):
            indexColor = inColorScheme(pixel[i,j], colorScheme)
            if(indexColor != False):
                pixel[i, j] = colorScheme[indexColor]

    return image


def getChangedColors(image, pixel_size=9):
    img = image.load()
    image_colors = []
    for i in range(0, image.size[0], pixel_size):
        for j in range(0, image.size[1], pixel_size):
            if(not img[i,j] in image_colors):
                image_colors.append(img[i,j])
    
    # combine colors
    deleted_indexes = []
    for i in range(len(image_colors)):
        for j in range(i+1, len(image_colors)):
            if (isSemiColor(image_colors[i], image_colors[j])):
                image_colors[i] = image_colors[j]
                if(not i in deleted_indexes):
                    deleted_indexes.append(i)

    for i in range(len(deleted_indexes)-1, -1, -1):
        image_colors.pop(deleted_indexes[i])
    
    return image_colors


filename = "static/images/tema.jpg"

with Image.open(filename) as img:
    img.load()

    shag_1 = eroziya(5, img)
    shag_2 = dilatatsiya(4, shag_1)

    filtered_image = pixelate(shag_2, 12)
    colors = getChangedColors(filtered_image)
    simple_image = changeColors(filtered_image, colors)
    print(colors)
    simple_image.save('static/formatted_images/example1.jpeg')
    simple_image.show()
