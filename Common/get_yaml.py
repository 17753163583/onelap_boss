import yaml


def get_yaml():
    file_path = '../Conf/boss_element.yaml'
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


if __name__ == '__main__':
    yaml_data = get_yaml()
    print(yaml_data)
