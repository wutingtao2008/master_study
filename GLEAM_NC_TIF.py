# -*- coding:utf-8 -*-
import arcpy
import pandas as pd
import netCDF4 as nc
import os
from arcpy.sa import *
import numpy as np
def deletefile(Path):
    for root, dirs, files in os.walk(Path):
        for name in files:
            if name.endswith(".tfw"):
                os.remove(os.path.join(root, name))
            if name.endswith(".xml"):
                os.remove(os.path.join(root, name))
            if name.endswith(".ovr"):
                os.remove(os.path.join(root, name))
            if name.endswith(".cpg"):
                os.remove(os.path.join(root, name))
            if name.endswith(".dbf"):
                os.remove(os.path.join(root, name))

inPath = r"E:\RS_datasets\GLEAM\PET3.3a\NC"

data025Path = "E:/RS_datasets/GLEAM/PET3.3a/025Raster"
data05Path = "E:/RS_datasets/GLEAM\PET3.3a/05Raster"

OutPath = "E:/RS_datasets/GLEAM\PET3.3a/OutPath"
# 0.25度的参考栅格图像
# ref_Raster_025 = "D:/Drought/GRACE_data/GLDAS_NOAH025.tif"
ref_Raster_05 = "D:/Drought/GRACE_data/CSR_GRACE_0.5.tif"



# 提取nc文件中需要的参数至tif格式
arcpy.env.workspace = inPath
arcpy.CheckOutExtension("Spatial")
 # 按名称和栅格类型返回工作空间中的栅格列表
filelist = os.listdir(inPath)
for ncfile in filelist:
    file_dir = os.path.join(inPath, ncfile)
    print file_dir
    nc_fid = nc.Dataset(file_dir)
    time_length = nc_fid.variables['time'][:].shape[0]
    out_partName = ncfile[0:-8]
    arcpy.MakeNetCDFRasterLayer_md(ncfile, 'Ep', 'lon', 'lat',out_partName,'time')
    for j in range(1, time_length+1):
        arcpy.MakeRasterLayer_management(Raster(out_partName), out_partName + str(j), "#", "#", str(j))
        Raster(out_partName+str(j)).save(data025Path + os.sep + out_partName+str(j) + '.tif')
        print out_partName + str(j)
deletefile(data025Path)
print "提取完成"

# 从0.25度重采样到0.5度

arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace = data025Path
# 设置参考栅格图像
arcpy.env.snapRaster = ref_Raster_05
i =1
for raster05 in arcpy.ListRasters("*", "tif"):
    # print raster005
    outName = data05Path + "/" + str(i) + ".tif"
    OutRas = arcpy.Resample_management(raster05, outName, "0.5", "NEAREST")
    i = i + 1
print "重采样完成"
deletefile(data05Path)

# 创建多波段栅格数据集
arcpy.env.workspace = data05Path
rasterlist = os.listdir(data05Path)
rasterlist.sort(key= lambda x:int(x[:-4]))
arcpy.CompositeBands_management(rasterlist, OutPath + os.sep +'GLEAM_05_all.tif')

# # 创建NC
# arcpy.env.workspace = OutPath
# # Set local variables
# inRaster = OutPath + os.sep +'GLEAM_05_all.tif'
# outNetCDFFile = OutPath + '/' + 'GLEAM_netcdf_notime2.nc'
# variable = "referencePotET"
# units = ""
# XDimension = "lon"
# YDimension = "lat"
# bandDimension = "time"
# # Process: RasterToNetCDF
# arcpy.RasterToNetCDF_md(inRaster, outNetCDFFile, variable, units,
#                         XDimension, YDimension, bandDimension)
#
# # 修改时间
# time_begin = 36159
# time_end = 43098
# # "days since 1901-01-01 00:00:00"
# relative_time = np.arange(time_begin, time_end + 1, 1)
# notime_nc_file = nc.Dataset(outNetCDFFile)
# variable = "referencePotET"
# ncfile = nc.Dataset(OutPath + os.sep + 'GLEAM_2000_2018221.nc', 'w', format='NETCDF4')
# ncfile.createDimension('longitude', None)
# ncfile.createDimension('latitude', None)
# ncfile.createDimension('time', None)
#
# ncfile.createVariable('lon', 'f4', dimensions='longitude')
# ncfile.createVariable('lat', 'f4', dimensions='latitude')
# ncfile.createVariable('time', 'f4', dimensions='time')
# ncfile.createVariable(variable, 'f4', dimensions=('time', 'latitude', 'longitude'))
# ncfile.variables['lat'][:] = notime_nc_file.variables['lat'][:]
# ncfile.variables['lon'][:] = notime_nc_file.variables['lon'][:]
# ncfile.variables[variable][:] = notime_nc_file.variables['referencePotET'][:]
# ncfile.variables['time'][:] = relative_time
#
# ncfile.close()
