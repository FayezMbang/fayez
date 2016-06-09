
##import modules
import arcpy
from arcpy import sa
from arcpy import env

##Environment Parameter
env.overwriteOutput = True
arcpy.CheckOutExtension("spatial")

GDB = arcpy.GetParameterAsText(0)
arcpy.CreateFileGDB_management(GDB, "AWD.gdb", "10.0")
env.workspace = GDB + "\AWD.gdb"
inputdem = arcpy.GetParameterAsText(1)
threshold = arcpy.GetParameterAsText(2)
snapdis = arcpy.GetParameterAsText(3)

arcpy.AddMessage("Automated Watershed Delineation Begin!")

##Geoprocessing
arcpy.AddMessage("Filling Dem")
fill = sa.Fill(inputdem)

arcpy.AddMessage("Processing Flowdirection")
flowdir = sa.FlowDirection(fill)

arcpy.AddMessage("Processing Flowaccumulation")
flowacc = sa.FlowAccumulation(flowdir)

if threshold == "":
    arcpy.AddMessage("Default Threshold Value")
    threshold = "2000"
arcpy.AddMessage("Building Stream Network")
con = sa.Con(flowacc, "1", "", "Value > " +threshold,)

arcpy.AddMessage("Creating StreamLink")
streamlin = sa.StreamLink(con,flowdir)

arcpy.AddMessage("Creating StreamOrder")
streamord = sa.StreamOrder(con,flowdir,"STRAHLER")

arcpy.AddMessage("Converting Raster Streams to Vector Streams")
streamtf = sa.StreamToFeature(streamlin,flowdir, "streamtofeature", "NO_SIMPLIFY")

arcpy.AddMessage("Generating Pour Point")
pourp = arcpy.FeatureVerticesToPoints_management(streamtf, "pourpoint", "END")

if snapdis == "":
    arcpy.AddMessage("Default Snap Distance")
    snapdis = "0"
arcpy.AddMessage("Snapping Pour Point")
snappp = sa.SnapPourPoint(pourp, flowacc, snapdis, "ORIG_FID")

arcpy.AddMessage("Generating Watershed")
watersh = arcpy.gp.Watershed_sa(flowdir, snappp, "watershed", "Value")

arcpy.AddMessage("Converting Raster Watershed to Vector Watershed")
arcpy.RasterToPolygon_conversion(watersh, "rastertopolygon", "NO_SIMPLIFY", "Value")

arcpy.AddMessage("Processing almost done!")



fill.save('fill')
flowdir.save('flowdirection')
flowacc.save('flowaccmulation')
con.save('condtion')
streamlin.save('streamlink')
streamord.save('streamorder')
snappp.save('snappourpoint')
arcpy.AddMessage("All processed files have been saved/n")



