
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import geopandas as gpd
from os.path import expanduser

def bsw_builder():
    importdir = f"{expanduser('~')}/Google Drive/Shared Drives/Analytics COE/Data Sources"

    # # Initialize geolocator
    # geolocator = Nominatim(user_agent="tagbswfacilites")
    # # Create a rate-limiter to avoid exceeding the API's usage limits
    # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)
    
    # #### BSW Facility builder ####
    # df = pd.read_excel(f"{importdir}/FacilityList 1023.xlsx", header=1)
    # ## Apply any filtering
    # df = df[df['Region'] == 'Greater Austin'].drop(columns=['Region'])
    # ## Geocode the filtered data
    # df['State'] = 'TX'
    # df['MAPPABLE_ADDRESS'] = df['Address 1'].str.strip() + ', ' + df['City'].str.strip() + ', ' + df['State'].str.strip() + ' ' + df['Zip Code'].astype(str).str.strip()
    # df['Latitude'], df['Longitude'] = zip(*df['MAPPABLE_ADDRESS'].apply(lambda x: get_lat_lon(x, geocode)))
    # ## Export the data
    # print( df )
    # df.to_csv('bsw_atx_facilities_geocode.csv', index=False)

    ## create geojson of the data
    df = pd.read_csv('bsw_atx_facilities_geocode.csv')
    df = df.groupby(['Latitude', 'Longitude', 'Access Point Type'], as_index=False).agg({'Access Point Name':'max'})
    geojson_builder(df, 'bsw_atx_facilities.geojson')


    #### Competitor Facility builder #### 

def get_lat_lon(address, geocode):
    try:
        location = geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        return None, None
    

def geojson_builder(df, filename):
    
    # Create a GeoDataFrame with the coordinate data
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

    # Set the CRS (Coordinate Reference System) to WGS84 (EPSG:4326)
    gdf.crs = "EPSG:4326"

    # Drop unnecessary columns for confidentiality
    # gdf.drop(columns=df.columns.difference(['Latitude', 'Longitude', 'geometry']), inplace=True)
    # print( gdf )

    # Save as GeoJSON file
    # # geojson_file_path = 'geocoded_atx_mover_sample.geojson'
    gdf.to_file(filename, driver='GeoJSON')



if __name__ == "__main__":
    bsw_builder()