from combine import combine
import yaml


def load_config():
    with open('setting.yml', 'r', encoding="utf-8") as file:
        file_data = file.read()
        c = yaml.full_load_all(file_data)
        for k in c:
            return k


def main():
    c = load_config()
    print(c)
    combine(c)


if __name__ == '__main__':
    main()
