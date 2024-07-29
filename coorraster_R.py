from osgeo import gdal
import pandas as pd
import numpy as np

dataset = gdal.Open("file location of the DSM")

# get the geospatial info from the DSM
width = dataset.RasterXSize
height = dataset.RasterYSize
nbands = dataset.RasterCount
gt = dataset.GetGeoTransform()
pr = dataset.GetProjection()

# read the raster data as a numpy array
data = dataset.GetRasterBand(1).ReadAsArray()
band = dataset.GetRasterBand(1)

# create ararays to store the pixel coordinate of x and y
a = np.arange(width)
x = np.tile(a,(height,1))
b = np.arange(height)
c = np.repeat(b[np.newaxis, :], width, axis=0)
y = c.T

# Create a new gdal dataset with the same dimensions, data type, geotransform and projection as original DSM
driver = gdal.GetDriverByName("GTiff")
output_x = driver.Create("output_x.tif", dataset.RasterXSize, dataset.RasterYSize, 1, band.DataType)
output_x.SetGeoTransform(gt)
output_x.SetProjection(pr)

# Write the "x" array to the new dataset
output_x_band = output_x.GetRasterBand(1)
output_x_band.WriteArray(x)
# Save and close the dataset
output_x_band.FlushCache()
output_x = None

output_y = driver.Create("output_y.tif", dataset.RasterXSize, dataset.RasterYSize, 1, band.DataType)
output_y.SetGeoTransform(gt)
output_y.SetProjection(pr)

output_y_band = output_y.GetRasterBand(1)
output_y_band.WriteArray(y)
output_y_band.FlushCache()
output_y = None