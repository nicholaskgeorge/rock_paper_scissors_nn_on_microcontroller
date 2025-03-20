import os
import unittest

from transform_data import parse_url, read_gdelt

data_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
        )

self.df1 = read_gdelt(data_folder, "20250212.export.CSV")
self.df2 = read_gdelt(data_folder, "20250213.export.CSV")