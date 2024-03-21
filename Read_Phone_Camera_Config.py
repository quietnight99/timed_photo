import yaml

def Read_Phone_Camera_Config():
    with open('./Phone_Camera_Config.yaml', mode='r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        f.close()
        return data



