# see: https://fastkml.readthedocs.org/en/latest/usage_guide.html#read-a-kml-file
# and: https://github.com/python-visualization/folium

from fastkml import kml
import pandas as pd
import folium

UNCLASSIFIED = '#808080'
EASY = '#00FF00'
INTERMEDIATE = '#FFFF00'
DIFFICULT = '#FF0000'

difficulties = { 'u' : UNCLASSIFIED,
                 'e' : EASY,
                 'i' : INTERMEDIATE,
                 'd' : DIFFICULT }

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
                        'difficulty' : [],
                        'difficulty_code' : []
                    }
    
    for layer in layers:
        print("Layer: %s" % (layer.name))
        try:
            segments = layer.features()
        except:
            continue

        for segment in segments:
            print "Segment: %s" % (segment.name)
            try:
                polyline = [(g.y, g.x) for g in segment.geometry.geoms]
                segment_records['name'].append(segment.name)
                segment_records['polyline'].append(polyline)
                segment_records['district'].append(layer.name)
                segment_records['difficulty'].append(UNCLASSIFIED)
                segment_records['difficulty_code'].append('u')
            except:
                print "no geometry"
                
    segment_df = pd.DataFrame(segment_records)
    
    return segment_df
    

def draw_lines(folium_map, segment_df):
    for (index, polyline, difficulty) in segment_df[['polyline', 'difficulty']].itertuples():
        folium_map.line(polyline, line_color=difficulty, line_weight=5)

    
def segments_to_map(coords, segment_df):
    map_osm = folium.Map(location=coords,tiles='Stamen Toner')    
    
    # Copy this by hand to greenways_edited.csv, edit in Open Office, fill in the difficulty codes.
    # Then re-run the script.
    segment_df.to_csv('greenways.csv',
                      columns=['name', 'difficulty_code', 'district', 'difficulty', 'polyline'])
        
    draw_lines(map_osm, segment_df)

    map_osm.create_map(path='osm.html')

def kmls_to_segments(kml_files):
    first = True
    
    for kml_file in kml_files:
        k = kml.KML()
        k.from_string(read_kml(kml_file))
        
        if first:
            segment_df = process_kml(k)
            first = False
        else:
            segment_df = segment_df.append(process_kml(k)).reset_index(drop=True)
            
    return segment_df

def csv_to_map(coords, segment_df, csv_file, output_html):
    edited_segment_df = pd.read_csv(csv_file, "\t")
    edited_segment_df['difficulty'] = edited_segment_df['difficulty_code'].map(lambda d: difficulties[d.lower()])
    segment_df = segment_df.reindex()
    edited_segment_df[['polyline']] = segment_df[['polyline']]
    
    map_osm = folium.Map(location=coords, tiles='Stamen Toner')
    draw_lines(map_osm, edited_segment_df)
    
    map_osm.create_map(path=output_html)

if __name__ == '__main__':
    coords = [47.6131746,-122.4878834] # Seattle
    # coords = [45.5236, -122.6750] # Portland

    # from http://seattlegreenways.org/neighborhoods/
    # Download the KML for the maps
    # Copy the .kmz file to kmz/
    # unzip <neighborhood>.kmz; mv doc.kml <neighborhood>.kml
    # eastlake and montlake weren't found on the page
    kml_files = ['kmz/beacon_hill.kml',
                 'kmz/central_seattle.kml',
                 'kmz/west_seattle.kml',
                 'kmz/rainier_valley.kml',
                 'kmz/ballard.kml',
                 'kmz/fremont.kml',
                 'kmz/queen_anne.kml',
                 'kmz/wallingford.kml',
                 'kmz/green_lake.kml',
                 'kmz/u_district.kml',
                 'kmz/maple_leaf.kml',
                 'kmz/ne_seattle.kml',
                 'kmz/montlake.kml',
                 'kmz/lake_city.kml',
                 'kmz/timf_meadowbrook.kml',
                 # from http://www.seattleoutdoorsinfo.com/hiking-and-biking/seattle-biking/seattle-bike-trails
                 'kmz/trails/alki_trail.kml',
                 'kmz/trails/green_river_interurban.kml',
                 'kmz/trails/burke_gilman.kml',
                 'kmz/trails/sodo_trail.kml',
                 'kmz/trails/west_seattle_bridge.kml',
                 'kmz/trails/duwamish_trail.kml',
                 'kmz/trails/cedar_lake.kml',
                 'kmz/trails/lake_wilderness.kml',
                 'kmz/trails/soos_creek.kml',
                 'kmz/trails/i_90_1.kml',
                 'kmz/trails/i_90_2.kml',
                 'kmz/trails/interurban_north_1.kml',
                 'kmz/trails/interurban_north_2.kml']
    
    segments_df = kmls_to_segments(kml_files)

    segments_to_map(coords, segments_df)
    
    csv_to_map(coords, segments_df, 'greenways_edited.csv', 'osm2.html')
