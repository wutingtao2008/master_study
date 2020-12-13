# -*-coding:utf-8-*-
# Author: Wu Tingtao
# Email: wutingtao2008@163.com
# CreatDate: 2020/10/15 17:22

import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import rasterio
import datetime
inPath = r'E:\RS_datasets\GLEAM\PET3.3a\05Raster'
GLEAM_05 = np.zeros(shape=(6940, 360, 720), dtype='float16')
# 经纬度
lon = np.linspace(-179.75, 179.75, 720)
lat = np.linspace(89.75, -89.75, 360)
# 从19010101为起点的天数
time_since = datetime.date(1901, 1, 1)
time_begin = datetime.date(2000, 1, 1) - time_since
time_end = datetime.date(2018, 12, 31) - time_since
time_all = np.arange(time_begin,time_end+1 ,1)

filelist = os.listdir(inPath)
filelist.sort(key=lambda x: int(x[:-4]))
i = 0
for files in filelist:
    file_dir = os.path.join(inPath, files)
    print(file_dir)
    file = rasterio.open(file_dir, 'r')
    data = pd.DataFrame(file.read(1))
    data[data == -999.0] = np.nan
    GLEAM_05[i,:,:] = data
GLEAM_05 = GLEAM_05/1000.0
GLEAM_05[GLEAM_05== -0.999] = np.nan
# 创建NC文件
ncfile = nc.Dataset(r'E:\RS_datasets\GLEAM' +os.sep+'GLEAM_3.3_05'+ '.nc', 'w', format='NETCDF4')
ncfile.createDimension('lon', None)
ncfile.createDimension('lat', None)
ncfile.createDimension('time', None)

ncfile.createVariable('lon', 'f4', dimensions='lon')
ncfile.createVariable('lat', 'f4', dimensions='lat')
ncfile.createVariable('time', 'f4', dimensions='time')
ncfile.createVariable('referencePotET', 'f4', dimensions=('time', 'lat', 'lon'))

ncfile.variables['lat'][:]= lat
ncfile.variables['lon'][:] = lon

ncfile.variables['referencePotET'][:] = GLEAM_05
ncfile.variables['time'][:] = time_all

ncfile.close()
