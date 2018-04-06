import geojson
import json
import csv
import matplotlib.cm as cm
import matplotlib.colors as colors

MATPLOTLIB_COLOUR_MAP_TYPE = 'inferno'


class RGBColourMapper:

    def __init__(self, norm_min=0, norm_max=1):
        self.norm_min = norm_min
        self.norm_max = norm_max
        self.norm = colors.Normalize(vmin=self.norm_min, vmax=self.norm_max)
        self.mapper = cm.ScalarMappable(norm=self.norm, cmap=cm.get_cmap(MATPLOTLIB_COLOUR_MAP_TYPE))

    def generate_hex_colour(self, value):
        rgb = self.mapper.to_rgba(value)[:3]
        return '#%02x%02x%02x' % tuple([int(255 * colour) for colour in rgb])


class GeoJsonMapper:

    def __init__(self, geojson_file_path, labels_file_path, label_name, region_type):
        self.geojson = self._open_geojson(geojson_file_path)
        self.label_name = label_name
        self.region_type = region_type
        self.unnormalised_labels = self._read_csv(labels_file_path)
        self.normalised_labels = self._normalise_values(self.unnormalised_labels)
        self.rgb_colour_mapper = RGBColourMapper()

    def _read_csv(self, file_location):
        labelling_values = {}
        with open(file_location) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                labelling_values[row[0]] = row[1]
        return labelling_values

    def _open_geojson(self, file_path):
        with open(file_path) as geojson_file:
            geo_json_data = geojson.load(geojson_file)
        return geo_json_data

    def _normalise_values(self, values):
        max_value = max([int(float(i)) for i in values.values()])
        min_value = min([int(float(i)) for i in values.values()])
        for value in values:
            values[value] = (int(values[value]) - min_value)/(max_value - min_value)
        return values

    def _get_label(self, labels, region):
        label = region.properties[self.region_type]
        return labels.get(label, 0)

    def label_geojson(self):
        # update colour based off statistic and append statistic as property
        for region in self.geojson.features:
            normalised_value = self._get_label(self.normalised_labels, region)
            unnormalised_value = self._get_label(self.unnormalised_labels, region)
            self._update_region_colour_and_label(region, normalised_value, unnormalised_value)

    def _update_region_colour_and_label(self, feature, normalised_value, unnormalised_value):
        feature.properties["fill"] = self.rgb_colour_mapper.generate_hex_colour(normalised_value)
        feature.properties[self.label_name] = unnormalised_value

    def print_geo_json(self, output_file_path):
        with open(output_file_path, 'w') as output_json_file:
            json.dump(self.geojson, output_json_file)


