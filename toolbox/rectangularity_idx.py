'''
Calculate rectangularity index of each object in given shapefile.

Formula described by Dibble (2016).

rectangularity_idx = Area/(Area of the rotated bounding rectangle)
'''

import geopandas as gpd
from tqdm import tqdm  # progress bar


# set path to shapefile
path = "/Users/martin/Strathcloud/Personal Folders/Test data/Royston/buildings.shp"


def object_rectangularity_idx(path, column_name):
    print('Calculating rectangularity index.')
    objects = gpd.read_file(path)  # load file into geopandas
    print('Shapefile loaded.')

    # define new column called 'area'
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Column ready. Calculating')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        objects.loc[index, column_name] = (row['geometry'].area)/(row['geometry'].minimum_rotated_rectangle.area)

    print('Rectangularity index calculated. Saving file.')

    # save dataframe back to file
    objects.to_file(path)
    print('File saved.')
