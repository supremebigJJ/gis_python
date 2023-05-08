# -*- coding: utf-8 -*-
import arcpy
import os
# Sign in to portal
arcpy.SignInToPortal('https://zhao.geoenterprise.cn/geoscene', 'siteadmin', 'zhao1234')
# Set output file names
outdir = r"D:\myarcgispro\protest"
service = "Sharemapservice"
sddraft_filename = service + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)
print (sddraft_output_filename)
# 注册文件夹
wrkspcs="D:\myarcgispro\protest"
server_conn = "MY_HOSTED_SERVICES"
if wrkspcs not in [i[2] for i in arcpy.ListDataStoreItems(server_conn, "FOLDER")]:
     dsStatus = arcpy.AddDataStoreItem(server_conn, "FOLDER", "promapzc", wrkspcs, wrkspcs)
print("注册: " + str(dsStatus))
# Reference map to publish
aprx = arcpy.mp.ArcGISProject(r"D:\myarcgispro\protest\protest.aprx")
draft_value = aprx.listMaps("Map1")[0]
# Create TileSharingDraft and set service properties
sharing_draft = draft_value.getWebLayerSharingDraft("FEDERATED_SERVER", "MAP_IMAGE", service)
sharing_draft.federatedServerUrl = "https://zhao.geoenterprise.cn/server"
sharing_draft.summary = "testpublish"
sharing_draft.tags = "testpublish"
sharing_draft.description = "credits"
sharing_draft.credits = "testpublish"
sharing_draft.useLimitations = "Limitation"
print("description")
# Create Service Definition Draft file
sharing_draft.exportToSDDraft(sddraft_output_filename)
print("to sd")
# Stage Service
try:
    sd_filename = service + ".sd"
    sd_output_filename = os.path.join(outdir, sd_filename)
    print(sd_output_filename)
    print(sddraft_output_filename)
    arcpy.StageService_server(sddraft_output_filename, sd_output_filename)
    warnings = arcpy.GetMessages(1)
    print(warnings)
except Exception as stage_exception:
    print("Sddraft not staged. Analyzer errors - {}".format(str(stage_exception)))
# Share to portal
print("Uploading Service Definition")
arcpy.UploadServiceDefinition_server(sd_output_filename, "https://zhao.geoenterprise.cn/server")
print("Successfully")
