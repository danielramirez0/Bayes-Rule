import sys
import cv2 as cv
from .main import MAP_FILE
from .main import SA1_CORNERS, SA2_CORNERS, SA3_CORNERS


class Search():
    """Bayesian Search & Rescue app with 3 search areas."""

    def __init__(self, name):
        self.name = name
        self.img = cv.read(MAP_FILE, cv.IMREAD_COLOR)
        if self.img is None:
            print(f"Could not open or find file {MAP_FILE}", file=sys.stderr)
            # raise FileNotFoundError(f"Could not open or find file {MAP_FILE}")
            sys.exit(1)

        self.area_actual = 0
        self.sailor_actual = (0, 0)  # As "local" coords within search area

        self.sa1 = self.img[SA1_CORNERS[1]:SA1_CORNERS[3],
                            SA1_CORNERS[0]:SA1_CORNERS[2]]

        self.sa2 = self.img[SA2_CORNERS[1]:SA2_CORNERS[3],
                            SA2_CORNERS[0]:SA2_CORNERS[2]]

        self.sa3 = self.img[SA3_CORNERS[1]:SA3_CORNERS[3],
                            SA3_CORNERS[0]:SA3_CORNERS[2]]

        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0

    def draw_map(self, last_known):
        """Display basemap with scale, last known XY location, and search areas."""
        cv.line(self.img, (20, 370), (70, 370), (0, 0, 0), 2)
        cv.putText(self.img, '0', (8, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, '50 Nautical Miles', (71, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        cv.rectangle(self.img, (SA1_CORNERS[0], SA1_CORNERS[1]),
                     (SA1_CORNERS[2], SA1_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(
            self.img, '1', (SA1_CORNERS[0] + 3, SA1_CORNERS[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, 0)

        cv.rectangle(self.img, (SA2_CORNERS[0], SA2_CORNERS[1]),
                     (SA2_CORNERS[2], SA2_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(
            self.img, '2', (SA2_CORNERS[0] + 3, SA2_CORNERS[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, 0)

        cv.rectangle(self.img, (SA3_CORNERS[0], SA3_CORNERS[1]),
                     (SA3_CORNERS[2], SA3_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(
            self.img, '3', (SA3_CORNERS[0] + 3, SA3_CORNERS[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, 0)

        cv.putText(self.img, '+', (last_known),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.img, '+ = Last Known Position', (274, 355),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.img, '* = Actual Position', (275, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

        cv.imshow('Search Area', self.img)
        cv.moveWindow('Search Area', 750, 10)
        cv.waitKey(500)
