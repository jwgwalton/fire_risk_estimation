import geojson
import json
import csv
import matplotlib.cm as cm
import matplotlib.colors as colors


class RGBColourMapper:

    def __init__(self, colour_mapper_type='inferno', norm_min=0, norm_max=1):
        self.norm_min = norm_min
        self.norm_max = norm_max
        self.norm = colors.Normalize(vmin=self.norm_min, vmax=self.norm_max)
        self.mapper = cm.ScalarMappable(norm=self.norm, cmap=cm.get_cmap(colour_mapper_type))

    def generate_hex_colour(self, value):
        rgb = self.mapper.to_rgba(value)[:3]
        return '#%02x%02x%02x' % tuple([int(255 * colour) for colour in rgb])


class GeoJsonMapper:

    def __init__(self, label_name, colour_mapper_type='inferno'):
        self.geojson = None
        self.label_name = label_name
        self.rgb_colour_mapper = RGBColourMapper(colour_mapper_type)

    def _read_csv(self, file_location):
        labelling_values = {}
        with open(file_location) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                labelling_values[row[0]] = row[1]
        return labelling_values

    def _open_geojson(self, file_path):
        with open(file_path) as geojson_file:
            self.geojson = geojson.load(geojson_file)

    def _normalise_values(self, values):
        max_value = max([int(i) for i in values.values()])
        min_value = min([int(i) for i in values.values()])
        for value in values:
            values[value] = (int(values[value]) - min_value)/(max_value - min_value)
        return values

    def _get_label(self, region_map, region, region_identifier_type):
        region_name = region.properties[region_identifier_type]
        return region_map.get(region_name, 0)

    def label_geojson(self, geojson_file_path, labels_file_path, region_identifier):
        # update colour based off statistic and append statistic as property
        self._open_geojson(geojson_file_path)
        unnormalised_values = self._read_csv(labels_file_path)
        normalised_values = self._normalise_values(unnormalised_values.copy())
        for region in self.geojson.features:
            normalised_value = self._get_label(normalised_values, region, region_identifier)
            unnormalised_value = self._get_label(unnormalised_values, region, region_identifier)
            self._update_region_colour_and_label(region, normalised_value, unnormalised_value)

    def _update_region_colour_and_label(self, feature, normalised_value, unnormalised_value):
        feature.properties["fill"] = self.rgb_colour_mapper.generate_hex_colour(normalised_value)
        feature.properties[self.label_name] = unnormalised_value

    def print_geo_json(self, output_file_path):
        with open(output_file_path, 'w') as output_json_file:
            json.dump(self.geojson, output_json_file)


