import geopandas as gpd
import numpy as np
import pandas as pd
import plotly.express as px
from shapely.geometry import MultiPolygon
import os


def generate_map(
        negativity_score_by_countries,
        output_path,
        shapefile_path=os.path.join(os.path.dirname(__file__), 'countries_shapefile', 'ne_110m_admin_0_countries.shp')
) -> None:

    gdf = gpd.read_file(shapefile_path)[['ADMIN', 'ADM0_A3', 'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']
    gdf = customize_shapefile(gdf)

    gdf = remove_unused_columns(gdf, negativity_score_by_countries)

    neg_scores = [negativity_score_by_countries[gdf.loc[row, 'country']] for row in gdf.index]
    gdf["score"] = pd.DataFrame(data=neg_scores)
    gdf = gdf.set_index("country")

    fig = generate_choropleth_map(gdf)

    fig.write_image(output_path)
    fig.show()


def reduce_multipolygons_by_length(polygon_shape, nb_polygon_to_keep):
    polygons_in_shape = list(polygon_shape)

    if len(polygons_in_shape) <= nb_polygon_to_keep:
        return polygon_shape
    else:
        polygons_length = [polygon.length for polygon in polygons_in_shape]
        polygons_indices_to_keep = arg_of_n_max(polygons_length, nb_polygon_to_keep)
        print("polygons_indices_to_keep =", polygons_indices_to_keep)

        if nb_polygon_to_keep == 1:
            return polygons_in_shape[polygons_indices_to_keep[0]]
        else:
            reduced_polygon = MultiPolygon([polygons_in_shape[i] for i in polygons_indices_to_keep])
            return reduced_polygon


def arg_of_n_max(lst, n):
    ind = np.argpartition(lst, -n)[-n:]
    return ind


def customize_shapefile(gdf):
    gdf.at[43, 'geometry'] = reduce_multipolygons_by_length(gdf.at[43, 'geometry'], 1)
    gdf.at[18, 'geometry'] = reduce_multipolygons_by_length(gdf.at[18, 'geometry'], 2)

    return gdf


def remove_unused_columns(gdf, negativity_score_by_countries):
    gdf.drop([row for row in range(len(gdf)) if gdf.loc[row, 'country'] not in negativity_score_by_countries.keys()],
             axis=0,
             inplace=True)
    gdf.index = [i for i in range(len(gdf))]
    return gdf


def generate_choropleth_map(gdf):
    fig = px.choropleth(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        projection='mercator',
        color_continuous_scale='rdylgn',
        color="score",
        width=3200, height=1600
    )

    fig.update_geos(fitbounds="locations", visible=False)

    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        coloraxis_showscale=False,
    )

    return fig
