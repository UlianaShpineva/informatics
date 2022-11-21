import json
import xmltodict
import time

if __name__ == '__main__':
    start_time = time.time()
    for i in range(100):
        with open("myxml.xml", "r",  encoding="utf-8") as xml_file:
            dict_file = xmltodict.parse(xml_file.read())
            with open("myjson_libs.json", "w",  encoding="utf-8") as json_file:
                json_file.write(json.dumps(dict_file, indent=4, ensure_ascii=False))
    print(time.time() - start_time)
# 0.21877264976501465
