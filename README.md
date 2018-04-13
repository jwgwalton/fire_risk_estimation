# Fire estimation

## Overview
The aim of this project is to estimate fire risk by area and property for London.

This repo used data released by the London Fire brigade of their responses from 1 January 2009 to 31 Aug 2015,
this is available at https://datahub.io/dataset/london-fire-brigade-incident-records/resource/7cd05a70-1e84-433b-847e-4e13a7f12610
The raw data is in the files:

LFB incident data 1 Jan 2009 to 31 Dec 2011.csv

LFB incident data 1 Jan 2012 to 31 Aug 2015.csv

The jupyter notebook Exploratory Data Analysis - London Fire Brigade.ipynb,
performs an analysis of the data to look at the risk of fire in residential properties by different postcodes in london.

## Visualisations
A visualisation of the number of fires for residential properties by postcode district is in data_visualisations/london_fires.geojson.
The geojson is annotated with the results of the analysis from Exploratory Data Analysis - London Fire Brigade.ipynb
using the code in geojson_mapper and is rendered by github, which uses leaflet.js and openStreetMap data to render geoJson and topJson files.


## geojson_mapper
This code is still in rough shape but i originally came up with it during an ONS x Barclaycard hackathon.
It annotates geojson/topojson with metadata & sets the colours for a heatmap visualisation,
at some point i'm intending to package it up and put it on pypi and extend it for more usecases of metadata tagging.