from PIL import Image
from pathlib import Path
import numpy as np 
from feature_extract import FeatureExtractor

import os
import psycopg2


if __name__ == "__main__":
    fe = FeatureExtractor()
    for img_path in Path("image").glob("*.jpg"):
        print(img_path)

        feature = fe.extract(img=Image.open(img_path))
        print(type(feature), feature.shape)

        feature_path = Path("feature") / (img_path.stem + ".npy")
        np.save(feature_path, feature)
        # print(feature_path)
