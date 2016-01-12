# see: https://fastkml.readthedocs.org/en/latest/usage_guide.html#read-a-kml-file
# and: https://github.com/python-visualization/folium

from fastkml import kml
import pandas as pd
import folium

UNCLASSIFIED = '#808080'
EASY = '#00FF00'
INTERMEDIATE = '#FFFF00'
DIFFICULT = '#FF0000'

def read_kml(filename):
    f = open(filename, 'r')
    return f.read()


def process_kml(kml):
    the_map = kml.features().next()
    print "Map: %s" % (the_map.name)
    
    layers = the_map.features()

    segment_records = { 'name' : [],
                        'polyline': [],
                        'district' : [],
                        'difficulty' : []
                    }
    
    for layer in layers:
        print("Layer: %s" % (layer.name))
        segments = layer.features()

        for segment in segments:
            print "Segment: %s" % (segment.name)
            try:
                polyline = [(g.y, g.x) for g in segment.geometry.geoms]
                segment_records['name'].append(segment.name)
                segment_records['polyline'].append(polyline)
                segment_records['district'].append(layer.name)
                segment_records['difficulty'].append(UNCLASSIFIED)
            except:
                print "no geometry"
                
    segment_df = pd.DataFrame(segment_records)
    
    return segment_df

def draw_lines(folium_map, segment_df):
    for (index, polyline, difficulty) in segment_df[['polyline', 'difficulty']].itertuples():
        folium_map.line(polyline, line_color=difficulty, line_weight=5)

    
def kml_to_map(coords, kml_file):
    kml_string = read_kml('doc.kml')
    print(kml_string)

    k = kml.KML()

    k.from_string(kml_string)

    map_osm = folium.Map(location=coords)    
    
    segment_df = process_kml(k)
    segment_df.to_csv('greenways.csv')
    
    draw_lines(map_osm, segment_df)

    map_osm.create_map(path='osm.html')

if __name__ == '__main__':
    coords = [47.6131746,-122.4878834] # Seattle
    # coords = [45.5236, -122.6750] # Portland

    kml_to_map(coords, 'doc.kml')
