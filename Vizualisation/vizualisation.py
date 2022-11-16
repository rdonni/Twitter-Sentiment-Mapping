# Imports
import pandas as pd
import geopandas as gpd
import sys
import pickle 
import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import cascaded_union
import cv2
sys.path.append('/Users/rayanedonni/Documents/Projets_persos/News_by_ai')
#from sentiment_analysis.tools import COUNTRIES

sys.path.remove('/Users/rayanedonni/Documents/Projets_persos/News_by_ai')

def plot(negativity_score_by_countries):
    
    shapefile = '/Users/rayanedonni/Downloads/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp'
    #Read shapefile using Geopandas
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    #Rename columns.
    gdf.columns = ['country', 'country_code', 'geometry']

    # Transform country shape to remove overseas territories
    # France
    array = np.array(gdf[gdf.country == 'France']['geometry'])
    gdf.loc[43,'geometry'] = array[0][1]
    # Russia
    shape_to_change = gdf.loc[18,'geometry'][-2]
    shape_to_change_2 = gdf.loc[18,'geometry'][-3]
    x, y = shape_to_change.exterior.coords.xy
    x2, y2 = shape_to_change_2.exterior.coords.xy
    for i in range (len(x)):
        x[i] = x[i] + 360
    for i in range (len(x2)):
        x2[i] = x2[i] + 360
    new_multipolygon = []
    for i in range (len(gdf.loc[18,'geometry'])) :
        if i == len(gdf.loc[18,'geometry']) - 3:
            pass
        
        elif i == len(gdf.loc[18,'geometry']) - 2:
            pass
            
        elif i == 1 :
            new_multipolygon.append(cascaded_union([gdf.loc[18,'geometry'][i], Polygon([[x2[i], y2[i]] for i in range(len(x2))])]))

        elif i == 0 :
            new_multipolygon.append(cascaded_union([gdf.loc[18,'geometry'][i], Polygon([[x[i], y[i]] for i in range(len(x))])]))
        
        else : 
            new_multipolygon.append(gdf.loc[18,'geometry'][i])          

    new_multipolygon = MultiPolygon(new_multipolygon)
    gdf['geometry'][18] = new_multipolygon

    # Remove useless rows of gdf        
    for row in range(len(gdf)):
        if gdf.loc[row, 'country'] not in negativity_score_by_countries.keys():
            gdf.drop(row, axis = 0, inplace = True)
    gdf.index = [i for i in range(len(gdf))]

    # Merge the two dataframes
    neg_scores = []
    for row in range (len(gdf)) :
        country = gdf.loc[row,'country'] 
        neg_scores.append(negativity_score_by_countries[country])
    merged = gdf.copy()
    merged["score"] = pd.DataFrame(data = neg_scores)


    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1) #figsize = (5,10)    
    
    #ax.annotate("Created from X tweets from each country collected between X and X",
    #            xy=(0.085, 0.15),  
     #           xycoords="figure fraction", 
     #           horizontalalignment="left", 
     #           verticalalignment="top", 
     #           fontstyle = "italic",
     #           fontsize=4, 
     #           color="#555555")
    
    
    merged.plot(column='score',
                ax=ax,
                cmap = 'RdYlGn',
                figsize = (4,8),  
                edgecolor = 'olive',
                linewidth = 0.3,
                missing_kwds={
                "color": "lightgrey",
                "label": "Missing values"}
                        )
    ax.set_axis_off()
    
    plt.savefig('/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/sentiment_map.png', bbox_inches='tight', dpi=1800)
    plt.show()
    
    
    



