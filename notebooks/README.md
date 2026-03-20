
Project title
Real-Data Drought Risk Mapping for the MENA Region

What this notebook does
This notebook builds a clean GeoAI prototype that turns satellite observations into drought-risk predictions and interactive spatial outputs.

Main outputs
Exploratory charts showing NDVI, rainfall, temperature, and drought patterns
Machine learning outputs including classification results, confusion matrix, and feature importance
Interactive drought map for the latest month in the dataset
Exportable portfolio assets such as HTML maps, figures, and a reusable project structure

Tools used

Google Earth Engine for satellite data access and aggregation
pandas / NumPy for tabular processing
scikit-learn for baseline machine learning
matplotlib for analysis plots
Folium for stakeholder-friendly interactive mapping

Notebook roadmap

Environment setup
Define study area and spatial grid
Load real MODIS, CHIRPS, and LST data from Earth Engine
Build monthly grid-level dataset
Engineer drought features and labels
Train a baseline Random Forest model
Interpret results
Create a polished interactive drought map
Prepare GitHub-ready assets and repo structure