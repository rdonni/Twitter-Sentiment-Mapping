import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

shapefile_path='/Users/rayanedonni/Downloads/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp'
gdf = gpd.read_file(shapefile_path)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf.columns = ['country', 'country_code', 'geometry']

gdf = gdf[gdf['country'] == 'France']

#print(type(gdf))




#print(*polygons)
#print(len(polygons))


def reduce_by_length(polygon_shape, nb_polygon_to_keep):
    polygons_in_shape = list(polygon_shape)
    
    if len(polygons_in_shape) <= nb_polygon_to_keep:
        return polygon_shape
    else :
        polygons_length = [polygon.length for polygon in polygons_in_shape]
        polygons_indices_to_keep = arg_of_n_max(polygons_length, nb_polygon_to_keep)
        print("polygons_indices_to_keep =", polygons_indices_to_keep)
        reduced_polygon = [polygons_in_shape[i] for i in polygons_indices_to_keep]
        return reduced_polygon
        
     

def arg_of_n_max(lst, n):
    ind = np.argpartition(lst, -n)[-n:]
    return ind


multipolygon = gdf.loc[43,'geometry']
polygon_reduced = reduce_by_length(multipolygon, 1)
print(polygon_reduced)

gdf.at[43, 'geometry'] = polygon_reduced[0]

gdf.plot()
plt.show()

#print(*polygons)
print(len(polygon_reduced))