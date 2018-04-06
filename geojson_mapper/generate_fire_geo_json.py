from geojson_mapper import GeoJsonMapper

geojson_file_path = "geojson/london.geojson"
fire_data_file_path = "fire_data/fires_by_postcode.csv"
output_geojson_path = "../data_visualisations/london_fires.geojson"

geojson_mapper = GeoJsonMapper(geojson_file_path, fire_data_file_path, "Number of Fires", "Name")

geojson_mapper.label_geojson()

geojson_mapper.print_geo_json(output_geojson_path)
