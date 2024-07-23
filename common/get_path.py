import os


def project_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def api_xlsx():
    return project_path() + "/api/test_data/api_demo.xlsx"


def publish_json_path():
    data_key_json_file_name = project_path() + '/POM/boss/test_data/publish_data.json'
    return data_key_json_file_name


if __name__ == '__main__':
    print(project_path())
