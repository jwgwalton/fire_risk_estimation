from geojson_mapper import GeoJsonMapper

geojson_file_path = "data/london.geojson"
fire_data_file_path = "data/fires_by_postcode.csv"
output_geojson_path = "../data_visualisations/london_fires.geojson"

geojson_mapper = GeoJsonMapper("Number of Fires")

geojson_mapper.label_geojson(geojson_file_path, fire_data_file_path, region_identifier="Name")

geojson_mapper.print_geo_json(output_geojson_path)
