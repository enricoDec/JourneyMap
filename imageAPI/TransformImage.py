from PIL import Image


class TransformImage:

    def __init__(self, path):
        self.image = None
        self.width = None
        self.height = None
        self.image_path = path
        self.load_image()

    def load_image(self):
        """Don't call"""
        self.image = Image.open(self.image_path)
        self.width = self.image.width
        self.height = self.image.height

    def crop(self, left, upper, right, lower):
        """Crops an image

        :param self:
        :param left: left corner
        :param upper: upper corner
        :param right: right corner
        :param lower: lower corner
        :return cropped image
        """
        box = (left, upper, right, lower)
        self.image = self.image.crop(box)
        return self.image

    def save(self, path):
        """Saves the image to a given path

        :param path: path
        """
        self.image = self.image.save(path)

    def resize(self, width, height):
        """Resize an image to the given width and height
        :param width: width
        :param height: height
        """
        self.image.thumbnail((width, height))

    def rotate(self, degrees):
        """Rotate image, and resize if necessary (degrees not 180)
        """
        self.image = self.image.rotate(degrees, expand=True)
