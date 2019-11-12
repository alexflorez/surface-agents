import functools
import numpy as np
from skimage import io


class Surface:
    def __init__(self):
        self.level = None    
        self.x_idxs, self.y_idxs = (None, None)

    def from_file(self, filename):
        """
        Create a surface level by reading an image file.
        The image is converted into grayscale.
        """
        self.level = io.imread(filename, as_gray=True)
        self.level = self.level * 255
        self.level = self.level.astype(int)
        self.x_idxs, self.y_idxs = self.idxs_region()

    def from_data(self, filedata):
        """
        Create a surface level by reading numpy data. 
        The data is stored as numpy format ".npy".
        """
        self.level = np.load(filedata)
        self.x_idxs, self.y_idxs = self.idxs_region()

    def reduce_to(self, percentage):
        """
        Change the surface level according to the 
        specified percentage.
        """
        self.level = np.array(self.level * percentage // 100,
                              dtype=int)
    
    def idxs_region(self):
        rows, columns = self.level.shape
        xs = [rows - 1] + list(range(rows)) + [0]
        ys = [columns - 1] + list(range(columns)) + [0]
        x_idxs, y_idxs = np.meshgrid(xs, ys, indexing='ij')
        return x_idxs, y_idxs

    @functools.lru_cache(maxsize=None)
    def region_idxs(self, x, y):
        """
        Extract a n x n region from the surface level 
        according to the current x and y positions.
        Return the indexes of the region.
        """
        # for a 3x3 region
        n = 3
        ixs = self.x_idxs[x: x + n, x: x + n]
        jys = self.y_idxs[y: y + n, y: y + n]
        return ixs, jys

    def __repr__(self):
        class_name = type(self).__name__
        return f'{class_name}\n<{self.level!r}>'
