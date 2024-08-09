from camera import Camera
from frame import Frame

camera = Camera()

def test_depth(x, y):
    color_image, depth_image = camera.take_picture()
    print(f'Depth at {x}, {y}: {depth_image[y, x]}')
    print(f'Pixel to point: {Frame.pixel_to_point(Frame, (x, y), depth_image[y, x])}')

test_depth(293, 117)