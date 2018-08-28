# shape.py
# definitons of shape characters

import geopandas as gpd
from tqdm import tqdm  # progress bar
import math
import random

'''
form_factor():
    Calculate form factor of each object in given shapefile. It can be used for any
    suitable element (building, block).

    Formula: area/(volume^(2/3))

    Reference: Bourdic, L., Salat, S. and Nowacki, C. (2012) ‘Assessing cities:
               a new system of cross-scale spatial indicators’, Building Research
               & Information, 40(5), pp. 592–605. doi: 10.1080/09613218.2012.703488.

    Attributes: objects = geoDataFrame with objects
                column_name = name of the column to save calculated values
                area_column = name of column where is stored area value
                volume_column = name of the column where is stored volume value

    Missing: Option to calculate without area and volume being calculated beforehand.
'''


def form_factor(objects, column_name, area_column, volume_column):
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating form factor.')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        if row[volume_column] is not 0:
            objects.loc[index, column_name] = row[area_column] / (row[volume_column] ** (2 / 3))

        else:
            objects.loc[index, column_name] = 0

    print('Form factor calculated.')

'''
fractal_dimension():
    Calculate fractal dimension of each object in given shapefile. It can be used for any
    suitable element (building, plot, voronoi cell, block).

    Formula: log(perimeter/4)/log(area)

    Reference: Hermosilla, T. et al. (2014) ‘Using street based metrics to characterize
               urban typologies’, Computers, Environment and Urban Systems, 44,
               pp. 68–79. doi: 10.1016/j.compenvurbsys.2013.12.002.

    Attributes: objects = geoDataFrame with objects
                column_name = name of the column to save calculated values
                area_column = name of column where is stored area value
                perimeter_column = name of the column where is stored perimeter value

    Missing: Option to calculate without area and perimeter being calculated beforehand.
'''


def fractal_dimension(objects, column_name, area_column, perimeter_column):
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating fractal dimension.')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = math.log(row[perimeter_column] / 4) / math.log(row[area_column])

    print('Fractal dimension calculated.')

'''
volume_facade_ratio():
    Calculate volume/facade ratio of each object in given shapefile. It can be used for any
    suitable element (building, block).

    Formula: volume/(perimeter * heigth)

    Reference: Schirmer, P. M. and Axhausen, K. W. (2015) ‘A multiscale classification
               of urban morphology’, Journal of Transport and Land Use, 9(1),
               pp. 101–130. doi: 10.5198/jtlu.2015.667.

    Attributes: objects = geoDataFrame with objects
                column_name = name of the column to save calculated values
                volume_column = name of column where is stored volume value
                perimeter_column = name of the column where is stored perimeter value
                height_column = name of the column where is stored height value

    Missing: Option to calculate without values being calculated beforehand.
'''


def volume_facade_ratio(objects, column_name, volume_column, perimeter_column, height_column):
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating volume/facade ratio.')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = row[volume_column] / (row[perimeter_column] * row[height_column])

    print('Volume/facade ratio calculated.')

'''
compactness_index():
    Calculate compactness index of each object in given shapefile. It can be used for any
    suitable element (building, plot, voronoi cell, block).

    Formula: area/area of enclosing circle

    Reference: Dibble, J. (2016) Urban Morphometrics: Towards a Quantitative
               Science of Urban Form. University of Strathclyde.

    Attributes: objects = geoDataFrame with objects
                column_name = name of the column to save calculated values
                area_column = name of column where is stored area value

    Missing: Option to calculate without values being calculated beforehand.
'''
#
# Smallest enclosing circle - Library (Python)
#
# Copyright (c) 2017 Project Nayuki
# https://www.nayuki.io/page/smallest-enclosing-circle
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program (see COPYING.txt and COPYING.LESSER.txt).
# If not, see <http://www.gnu.org/licenses/>.
#
# Data conventions: A point is a pair of floats (x, y). A circle is a triple of floats (center x, center y, radius).

# Returns the smallest circle that encloses all the given points. Runs in expected O(n) time, randomized.
# Input: A sequence of pairs of floats or ints, e.g. [(0,5), (3.1,-2.7)].
# Output: A triple of floats representing a circle.
# Note: If 0 points are given, None is returned. If 1 point is given, a circle of radius 0 is returned.
#
# Initially: No boundary points known


def make_circle(points):
    # Convert to float and randomize order
    shuffled = [(float(x), float(y)) for (x, y) in points]
    random.shuffle(shuffled)

    # Progressively add points to circle or recompute circle
    c = None
    for (i, p) in enumerate(shuffled):
        if c is None or not is_in_circle(c, p):
            c = _make_circle_one_point(shuffled[: i + 1], p)
    return c


# One boundary point known
def _make_circle_one_point(points, p):
    c = (p[0], p[1], 0.0)
    for (i, q) in enumerate(points):
        if not is_in_circle(c, q):
            if c[2] == 0.0:
                c = make_diameter(p, q)
            else:
                c = _make_circle_two_points(points[: i + 1], p, q)
    return c


# Two boundary points known
def _make_circle_two_points(points, p, q):
    circ = make_diameter(p, q)
    left = None
    right = None
    px, py = p
    qx, qy = q

    # For each point not in the two-point circle
    for r in points:
        if is_in_circle(circ, r):
            continue

        # Form a circumcircle and classify it on left or right side
        cross = _cross_product(px, py, qx, qy, r[0], r[1])
        c = make_circumcircle(p, q, r)
        if c is None:
            continue
        elif cross > 0.0 and (left is None or _cross_product(px, py, qx, qy, c[0], c[1]) > _cross_product(px, py, qx, qy, left[0], left[1])):
            left = c
        elif cross < 0.0 and (right is None or _cross_product(px, py, qx, qy, c[0], c[1]) < _cross_product(px, py, qx, qy, right[0], right[1])):
            right = c

    # Select which circle to return
    if left is None and right is None:
        return circ
    elif left is None:
        return right
    elif right is None:
        return left
    else:
        return left if (left[2] <= right[2]) else right


def make_circumcircle(p0, p1, p2):
    # Mathematical algorithm from Wikipedia: Circumscribed circle
    ax, ay = p0
    bx, by = p1
    cx, cy = p2
    ox = (min(ax, bx, cx) + max(ax, bx, cx)) / 2.0
    oy = (min(ay, by, cy) + max(ay, by, cy)) / 2.0
    ax -= ox
    ay -= oy
    bx -= ox
    by -= oy
    cx -= ox
    cy -= oy
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
    if d == 0.0:
        return None
    x = ox + ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    y = oy + ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    ra = math.hypot(x - p0[0], y - p0[1])
    rb = math.hypot(x - p1[0], y - p1[1])
    rc = math.hypot(x - p2[0], y - p2[1])
    return (x, y, max(ra, rb, rc))


def make_diameter(p0, p1):
    cx = (p0[0] + p1[0]) / 2.0
    cy = (p0[1] + p1[1]) / 2.0
    r0 = math.hypot(cx - p0[0], cy - p0[1])
    r1 = math.hypot(cx - p1[0], cy - p1[1])
    return (cx, cy, max(r0, r1))


_MULTIPLICATIVE_EPSILON = 1 + 1e-14


def is_in_circle(c, p):
    return c is not None and math.hypot(p[0] - c[0], p[1] - c[1]) <= c[2] * _MULTIPLICATIVE_EPSILON


# Returns twice the signed area of the triangle defined by (x0, y0), (x1, y1), (x2, y2).
def _cross_product(x0, y0, x1, y1, x2, y2):
    return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)
# end of Nayuiki script to define the smallest enclosing circle


def compactness_index(objects, column_name, area_column):
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating compactness index.')

    # calculate the area of circumcircle
    def circle_area(points):
        circ = make_circle(points)
        return(math.pi * circ[2] ** 2)

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        objects.loc[index, column_name] = (row[area_column]) / (circle_area(list(row['geometry'].exterior.coords)))

    print('Compactness index calculated.')

'''
compactness_index2():
    Calculate compactness index of each object in given shapefile. It can be used for any
    suitable element (building, plot, voronoi cell, block).

    Formula: area/perimeter ratio of the block divided by the area/perimeter ratio of a squared block having the same area ~ √a/p

    Reference: Feliciotti A (2018) RESILIENCE AND URBAN DESIGN:A SYSTEMS APPROACH TO THE STUDY OF RESILIENCE IN URBAN FORM.
               LEARNING FROM THE CASE OF GORBALS. Glasgow.

    Attributes: objects = geoDataFrame with objects
                column_name = name of the column to save calculated values
                area_column = name of column where is stored area value
                perimeter_column = name of the column where is stored perimeter value

    Missing: Option to calculate without values being calculated beforehand.
'''


def compactness_index2(objects, column_name, area_column, perimeter_column):
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating compactness index.')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        objects.loc[index, column_name] = (math.sqrt(row[area_column])) / (row[perimeter_column])

    print('Compactness index calculated.')

'''
convexeity():
    Calculate convexeity of each object in given shapefile. It can be used for any
    suitable element (building, plot, voronoi cell, block).

    Formula: area/convex hull area

    Reference: Dibble, J. (2016) Urban Morphometrics: Towards a Quantitative
               Science of Urban Form. University of Strathclyde.

    Attributes: objects = geoDataFrame with objects
                column_name = name of the column to save calculated values
                area_column = name of column where is stored area value

    Missing: Option to calculate without values being calculated beforehand.
'''


def convexeity(objects, column_name, area_column):
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating convexeity.')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = row[area_column] / (row['geometry'].convex_hull.area)

    print('Convexeity calculated.')

'''
courtyard_index():
    Calculate courtyard index of each object in given shapefile. It can be used for any
    suitable element (building, block).

    Formula: area/convex hull area

    Reference: Schirmer, P. M. and Axhausen, K. W. (2015) ‘A multiscale classification
               of urban morphology’, Journal of Transport and Land Use, 9(1),
               pp. 101–130. doi: 10.5198/jtlu.2015.667.

    Attributes: objects = geoDataFrame with objects
                column_name = name of the column to save calculated values
                area_column = name of column where is stored area value
                courtyard_column = name of the column where is stored courtyard area

    Missing: Option to calculate without values being calculated beforehand.
'''


def courtyard_index(objects, column_name, area_column, courtyard_column):
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating courtyard index.')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = row[courtyard_column] / row[area_column]

    print('Courtyard index calculated.')


'''
rectangularity():
    Calculate rectangularity of each object in given shapefile. It can be used for any
    suitable element (building, plot, voronoi cell, block).

    Formula: area/minimum bounding rotated rectangle area

    Reference: Dibble, J. (2016) Urban Morphometrics: Towards a Quantitative
               Science of Urban Form. University of Strathclyde.

    Attributes: objects = geoDataFrame with objects
                column_name = name of the column to save calculated values
                area_column = name of column where is stored area value

    Missing: Option to calculate without values being calculated beforehand.
'''


def rectangularity(objects, column_name, area_column):
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating rectangularity.')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = row[area_column] / (row['geometry'].minimum_rotated_rectangle.area)

    print('Rectangularity calculated.')


# to be deleted, keep at the end

# path = "/Users/martin/Strathcloud/Personal Folders/Test data/Royston/buildings.shp"
# objects = gpd.read_file(path)
#
# convexeity(objects, 'conv', 'pdbAre')
#
# objects.head
# objects.to_file(path)
