import arcpy,os
import json
from urllib import request
from urllib import parse
from contextlib import closing
from urllib.parse import urlencode

#server域名
hostname="portal.arcgis.com"
#更新的服务名称
service_name="bm_688w"
#存放原始数据的pg库连接
pgsde=r"C:\Users\Administrator\Documents\ArcGIS\Projects\jm_test\234.sde"
#目标数据名称
target="db_hfbiu.sde.bm_gz_300w"
#待追加的数据源
updateData=r"C:\Users\Administrator\Documents\ArcGIS\Projects\jm_test\jm_test.gdb\bm_688w"
#映射字段
fieldMap="gobalid"

generateTokenUrl="https://portal.arcgis.com/arcgis/sharing/rest/generateToken"
portal_user="portaladmin"
portal_psw="portaladmin123"

def getToken():
    print("获取portal资源访问的token！")
    params = {'username': portal_user, 'password':portal_psw,'client':'referer','referer':'https://{}/'.format(hostname),'f':'pjson'}
    #将str类型转换为bytes类型
    data = parse.urlencode(params).encode("utf-8")
    #print(urllib.request.urlopen(request).read().decode("utf-8"))
    requestP = request.Request(generateTokenUrl, data=data)
    with closing(request.urlopen(requestP)) as response:
        content = response.read()
        content_decoded = content.decode("utf-8")
        result = json.loads(content_decoded)
        print(result)
        return result['token']


def appendData():
    #追加数据参数schema_type
    schema_type = "NO_TEST"
    #创建映射关系
    fieldMappings = arcpy.FieldMappings()
    fieldMap = arcpy.FieldMap()
    #fieldMap.addInputField(updateData, fieldMap)
    fieldMap.mergeRule="First"
    #fieldMappings.addFieldMap(fieldMap)
    #执行追加数据操作
    arcpy.management.Append([updateData],os.path.join(pgsde,target),"NO_TEST",'','','')
    print(arcpy.GetMessages())
    print("追加数据成功！")
    
def updateServiceCache():
    _referer_url = "https://{}".format(hostname)
    #更新缓存的工具
    submit_url = "https://{}/server/rest/services/System/SceneCachingControllers/GPServer/Manage%20Scene%20Cache/submitJob?".format(hostname)
    service_url = '{}/server/rest/services/Hosted/{}/SceneServer'.format(_referer_url, service_name)
    #访问portal服务的token
    token=getToken()

    #请求发送的参数
    params = {'service_url': service_url, 'num_of_caching_service_instances': 2, 'layer': {}, 'update_mode': 'PARTIAL_UPDATE_NODES', 'update_extent': 'DEFAULT',
'area_of_interest': {"displayFieldName": "", "geometryType": "esriGeometryPolygon", "spatialReference": {"wkid": 54051, "latestWkid": 54051}, "fields": [{"name": "OID", "type": "esriFieldTypeOID", "alias": "OID"}, {"name": "updateGeom_Length", "type": "esriFieldTypeDouble","alias": "updateGeom_Length"}, {"name": "updateGeom_Area", "type": "esriFieldTypeDouble", "alias": "updateGeom_Area"}], "features": [], "exceededTransferLimit": False}, 'f': 'json', 'token': token}

    headers = {"Referer": _referer_url}
    data = parse.urlencode(params).encode("utf-8")
    requestP =request.Request(submit_url, data=data, headers=headers)
    with closing(request.urlopen(requestP)) as response:
        content = response.read()
        content_decoded = content.decode("utf-8")
        result = json.loads(content_decoded)
        result = json.loads(content_decoded)
        print(result)
        print("提交更新缓存成功！")


if __name__ == '__main__':
    #实现数据的追加
    appendData()
    #更新服务的缓存
    updateServiceCache()
	



