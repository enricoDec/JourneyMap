from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS


class ImageAnalysis:

    def __init__(self, path):
        self.image = None
        self.exif = None
        self.image_path = path
        self.load_image(path)

    def load_image(self, image_path):
        """Get exif data from a JPG image

        :parameter self
        :parameter image_path path to the image
        """

        self.image = Image.open(image_path)
        self.exif = self.image.getexif()

    def get_labeled_exif(self):
        """Get all labeled exif data from exif data

        :parameter self
        :return labeled exif data
        """
        labeled = {}
        for (key, val) in self.exif.items():
            labeled[TAGS.get(key)] = val

        return labeled

    def get_decimal_from_dms(self, dms, ref):
        """Converts dms format into lat and long"""
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0

        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds

        return round(degrees + minutes + seconds, 5)

    def get_coordinates(self):
        """Get latitude and longitude from geo tags

        :param self:
        :return: latitude and longitude
        """
        if not self.exif:
            raise ValueError('No EXIF metadata found for ' + self.image_path)

        geotagging = {}
        for (idx, tags) in TAGS.items():
            if tags == 'GPSInfo':
                if idx not in self.exif:
                    raise ValueError('No EXIF geotagging found for ' + self.image_path)

                for (key, val) in GPSTAGS.items():
                    if key in self.exif[idx]:
                        geotagging[val] = self.exif[idx][key]

        lat = self.get_decimal_from_dms(geotagging['GPSLatitude'], geotagging['GPSLatitudeRef'])

        lon = self.get_decimal_from_dms(geotagging['GPSLongitude'], geotagging['GPSLongitudeRef'])

        return lat, lon

    def get_metadata_from_exit_tag(self, tag_to_find):
        """

        :param self:
        :param tag_to_find: hex Value of exif tag to return
        :return: exif tag
        """
        int(tag_to_find.__str__(), 0)
        for tag, value in self.exif.items():
            if tag == tag_to_find:
                return value
        raise ValueError('Image does not contain ' + TAGS.get(tag))

    def get_time_created(self):
        """Get time of creation

        :param self:
        :return: Date
        """
        return self.get_metadata_from_exit_tag(0x9003)

    def get_camera_model(self):
        """Get Model of Camera"""
        return self.get_metadata_from_exit_tag(0x010F) + self.get_metadata_from_exit_tag(0x0110)

    def get_minial_exif_label(self):
        """Get a minial list of exif data"""
        # Format to Django date convention
        location = 0.0000, 0.0000
        try:
            location = self.get_coordinates()
        except Exception:
            pass

        date = self.get_time_created()
        year, time = date.split()
        year = year.replace(':', '-')
        exif_dict = {
            'lat': location[0],
            'long': location[1],
            'date': year,
            'time': time
        }
        return exif_dict
