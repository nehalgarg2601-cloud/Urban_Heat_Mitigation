import ee
import os
import requests

def authenticate_gee():
    print("--- Google Earth Engine Authentication (V5 Elite Architecture) ---")
    project_id = "mediq-app-a3a52"
    try:
        ee.Initialize(project=project_id)
    except Exception:
        ee.Authenticate()
        ee.Initialize(project=project_id)
    print("Earth Engine Initialized Successfully!")

def get_landsat_lst(aoi, start_date, end_date):
    """
    Fetch Landsat 8 Collection 2 Level 2 Surface Temperature.
    Applies scaling factors to convert to Kelvin directly.
    """
    collection = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2") \
        .filterBounds(aoi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUD_COVER', 10))

    def apply_scale_factors(image):
        lst_kelvin = image.select('ST_B10').multiply(0.00341802).add(149.0).rename('LST_Kelvin')
        return image.addBands(lst_kelvin)

    scaled_collection = collection.map(apply_scale_factors)
    median_image = scaled_collection.select('LST_Kelvin').median()
    return median_image.clip(aoi)

def get_sentinel2_features(aoi, start_date, end_date):
    """
    Fetch Sentinel-2 Harmonized Surface Reflectance to compute
    NDVI, 5-band Liang (2001) Albedo, and empirical NDWI (B3/B11).
    """
    collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(aoi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))

    def compute_indices(image):
        img_scaled = image.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']).multiply(0.0001)

        # NDVI: (NIR - RED) / (NIR + RED)
        ndvi = img_scaled.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # NDWI: (GREEN - SWIR) / (GREEN + SWIR) -> using B3 (Green) and B11 (SWIR1)
        ndwi = img_scaled.normalizedDifference(['B3', 'B11']).rename('NDWI')
        
        # Albedo: Liang (2001) 5-band formula
        albedo = img_scaled.expression(
            '0.356 * B2 + 0.130 * B4 + 0.373 * B8 + 0.085 * B11 + 0.072 * B12 - 0.0018',
            {
                'B2': img_scaled.select('B2'),
                'B4': img_scaled.select('B4'),
                'B8': img_scaled.select('B8'),
                'B11': img_scaled.select('B11'),
                'B12': img_scaled.select('B12')
            }
        ).rename('Albedo')
        
        return image.addBands([ndvi, albedo, ndwi])

    processed_collection = collection.map(compute_indices)
    median_image = processed_collection.select(['NDVI', 'Albedo', 'NDWI']).median()
    return median_image.clip(aoi)

def download_image(image, aoi, scale, filename, output_dir):
    print(f"Generating download URL for {filename}...")
    try:
        url = image.getDownloadURL({
            'scale': scale,
            'crs': 'EPSG:32643', # UTM Zone 43N (Delhi)
            'region': aoi,
            'format': 'GEO_TIFF'
        })
        print(f"Downloading from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        file_path = os.path.join(output_dir, f"{filename}.tif")
        with open(file_path, 'wb') as fd:
            fd.write(response.content)
            
        print(f"Successfully downloaded to {file_path}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

def main():
    authenticate_gee()
    
    # Target AOI: Delhi-NCR
    min_lon, min_lat = 77.00, 28.40
    max_lon, max_lat = 77.35, 28.75
    aoi = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])
    
    # Multi-temporal window: Peak Summer (May 2023) and Monsoon (August 2023)
    windows = {
        'Summer_2023': ('2023-05-01', '2023-05-31'),
        'Monsoon_2023': ('2023-08-01', '2023-08-31')
    }
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'raw')
    os.makedirs(output_dir, exist_ok=True)
    
    for season, (start_date, end_date) in windows.items():
        print(f"\nFetching Landsat 8 LST and Sentinel-2 features for {season} ({start_date} to {end_date})...")
        lst_image = get_landsat_lst(aoi, start_date, end_date)
        s2_image = get_sentinel2_features(aoi, start_date, end_date)
        
        download_image(lst_image, aoi, scale=30, filename=f"LST_Kelvin_{season}", output_dir=output_dir)
        download_image(s2_image, aoi, scale=30, filename=f"Sentinel2_Features_{season}", output_dir=output_dir)
        
    print("\n✅ V5 Elite GEE Extraction Complete! Real NDWI and Multi-Temporal rasters acquired.")

if __name__ == "__main__":
    main()
