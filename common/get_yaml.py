import yaml
from common.get_path import project_path


class GetYamlData:
    @staticmethod
    def get_boss_element_data():
        file_path = project_path() + '/conf/boss_element.yaml'
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)

    @staticmethod
    def get_onelap_element_data():
        file_path = project_path() + '/conf/onelap_element.yaml'
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)

    @staticmethod
    def get_boss_api_param_data():
        file_path = project_path() + '/conf/boss_api_param.yaml'
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)

    @staticmethod
    def get_onelap_api_param_data():
        file_path = project_path() + '/conf/onelap_api_param.yaml'
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)


if __name__ == '__main__':
    yaml_data = GetYamlData.get_onelap_api_param_data()['add_report']
    # {'type': 'class name', 'key': 'glyphicon glyphicon-envelope form-control-feedback'}
    print(yaml_data)
