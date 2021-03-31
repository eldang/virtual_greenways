import fiona
import shapefile
import pandas as pd
import pyproj
from functools import partial
from shapely.geometry import Point
from shapely.ops import transform
import folium_test
from folium_test import UNCLASSIFIED, INTERMEDIATE, DIFFICULT, ALL_ABILITIES,\
    segments_to_map
import os


# see http://pandas.pydata.org/pandas-docs/stable/indexing.html
def select_segments(segment_df):
    selected_df = segment_df.query('Existing == "Y"')
    return selected_df


def street_network_database_to_folium(segment_df):
    folium_df = pd.DataFrame(
        segment_df.loc[:,[
            'ORD_STNAME', 'F_INTR_ID', 'points']])
    folium_df.rename(columns={
        'ORD_STNAME': 'name',
        'F_INTR_ID': 'description',
        'points': 'polyline'
    }, inplace=True)
    folium_df['district'] = 'Current'
    folium_df['difficulty'] = ALL_ABILITIES
    folium_df['difficulty_code'] = 'e'
    return folium_df

def bicycle_facilities_to_folium(segment_df):
    folium_df = pd.DataFrame(
        segment_df.loc[:,[
            'STREET_NAM', 'EXISTING_F', 'points']])
    folium_df.rename(columns={
        'STREET_NAM': 'name',
        'EXISTING_F': 'description',
        'points': 'polyline'
    }, inplace=True)
    folium_df['district'] = 'Current'
    folium_df['difficulty'] = UNCLASSIFIED
    folium_df['difficulty_code'] = 'u'

    return folium_df


def classify_segments(folium_df):
    folium_df.loc[
        folium_df.description.isin([
            'Neighborhood Greenway',
            'Multi-use Trail',
            'In Street, Major Separation']),
        ['difficulty',
         'difficulty_code']] = (ALL_ABILITIES, 'e')

    folium_df.loc[
        folium_df.description.isin([
            'In Street, Minor Separation']),
        ['difficulty',
         'difficulty_code']] = (INTERMEDIATE, 'i')

    folium_df.loc[
        folium_df.description.isin([
            'In Street, Minor Separation']),
        ['difficulty',
         'difficulty_code']] = (DIFFICULT, 'd')

    folium_df.loc[
        folium_df.description.isin([
            'Sharow', 'Sharrow', 'sharrow']),
        ['difficulty',
         'difficulty_code']] = (UNCLASSIFIED, 'u')

