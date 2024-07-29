from osgeo import gdal
import pandas as pd
from scipy import optimize
import numpy as np
from sklearn.linear_model import LinearRegression

#open newly created x and y coordinates and read them into arrays
xdata = gdal.Open("file location of the x-coordinate raster")
x = xdata.GetRasterBand(1).ReadAsArray()
ydata = gdal.Open("file location of the x-coordinate raster")
y = ydata.GetRasterBand(1).ReadAsArray()

# open the pre-fire and post-fire DSM into arrays
jun = gdal.Open("file location of the pre-fire DSM")
z = jun.GetRasterBand(1).ReadAsArray()
nov = gdal.Open("file location of the post-fire DSM")
g_Nov = nov.GetRasterBand(1).ReadAsArray()

# read in the tie points data and flatten the data
'''
The tie points data contains 4 columns: 
x, is the x-coordinates of tie point; 
y, is the y-coordinates of tie point; 
z, is the true elevation;
gnor, is the post-fire DSM needs to be verified
'''
dt = pd.read_csv("file location of the *.csv file of tie points data")
xtie = dt['x'].to_numpy()
ytie = dt['y'].to_numpy()
ztie = dt['z'].to_numpy()
gnovtie = dt['gnov'].to_numpy()

Xtie = np.stack((xtie,ytie,gnovtie), axis = 1)
Xtie.shape

# Create a linear regression model and fit it with X and z-gnovtie
reg_Nov = LinearRegression().fit(Xtie, ztie)
ab = reg_Nov.coef_
c = reg_Nov.intercept_

#stack x and y arrays to fit into the regression model to predict the elevation
x_flat = x.flatten()
y_flat = y.flatten()
g_Nov_flat = g_Nov.flatten()
print(x_flat.shape, y_flat.shape)
X = np.stack((x_flat,y_flat,g_Nov_flat), axis = 1)
H_Nov = reg_Nov.predict(X)

H_Nov_re = np.reshape(H_Nov, x.shape)

# Create a new gdal dataset and assign the same dimensions, data type, geotransform and projection as original raster
gt = xdata.GetGeoTransform()
pr = xdata.GetProjection()
data_type = gdal.GDT_Float32
driver = gdal.GetDriverByName("GTiff")
output_Nov = driver.Create("output_Nov.tif", xdata.RasterXSize, xdata.RasterYSize, 1, data_type)
output_Nov.SetGeoTransform(gt)
output_Nov.SetProjection(pr)

# Write the elevation array to the new dataset.
output_Nov_band = output_Nov.GetRasterBand(1)
output_Nov_band.WriteArray(H_Nov_re)
output_Nov_band.FlushCache()
output_Nov = None