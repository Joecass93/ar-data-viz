from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import geopandas as gpd
from os.path import expanduser

workdir = f"{expanduser('~')}/Downloads"

# Initialize geolocator
geolocator = Nominatim(user_agent="tagbswfacilites")

# Create a rate-limiter to avoid exceeding the API's usage limits
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)


def facility():
    ## Load the data
    # bsw_data = pd.read_excel(f'{workdir}/ATX Facility List_0725.xlsx')
    competitor_data = pd.read_excel(f'{workdir}/GAR_THCIC_Facilities.20230906.xlsx')

    # ## Geocode BSW facilities
    # bsw_data['Full_Address'] = bsw_data['Address 1'] + ', ' + bsw_data['City'] + ', ' + bsw_data['State'] + ' ' + bsw_data['Zip'].astype(str)
    # bsw_data['Latitude'], bsw_data['Longitude'] = zip(*bsw_data['Full_Address'].apply(lambda x: get_lat_lon(x)))
    # print( bsw_data )
    # bsw_data.to_excel('Geocoded_ATX_Facility_List_0725.xlsx', index=False)

    ## Geocode competitor facilities
    competitor_data['Latitude'], competitor_data['Longitude'] = zip(*competitor_data['MAPPABLE_ADDRESS'].apply(lambda x: get_lat_lon(x)))
    print( competitor_data )
    competitor_data.to_excel('Geocoded_GAR_THCIC_Facilities.20230906.xlsx', index=False)

    print("Geocoding complete. Data has been saved to Excel files.")

def mover():
    ## Load the data
    mover_data = pd.read_csv(f'{workdir}/atx_mover_sample.csv')
    mover_data['Full_Address'] = mover_data['TD_CASS_ADDRESS1'] + ', ' + mover_data['TD_CASS_CITY'] + ', ' + mover_data['TD_CASS_STATE'] + ' ' + mover_data['TD_CASS_ZIP'].astype(str)

    ## Geocode the addresses
    mover_data['Latitude'], mover_data['Longitude'] = zip(*mover_data['Full_Address'].apply(lambda x: get_lat_lon(x)))
    print( mover_data )
    mover_data.to_csv('geocoded_atx_mover_sample.csv', index=False)

    print("Geocoding complete. Data has been saved.")


def geojson_builder():
    ## load the geocoded csv/excel file 
    df = pd.read_csv('geocoded_atx_mover_sample.csv')
    
    # Create a GeoDataFrame with the coordinate data
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

    # Set the CRS (Coordinate Reference System) to WGS84 (EPSG:4326)
    gdf.crs = "EPSG:4326"

    # Drop unnecessary columns for confidentiality
    gdf.drop(columns=df.columns.difference(['Latitude', 'Longitude', 'geometry']), inplace=True)

    # Save as GeoJSON file
    geojson_file_path = 'geocoded_atx_mover_sample.geojson'
    gdf.to_file(geojson_file_path, driver='GeoJSON')


# Function to geocode addresses
def get_lat_lon(address):
    try:
        location = geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        return None, None


if __name__ == "__main__":
    geojson_builder()