from sort import sort_in_files
from statistics import after_read_statistic
from file import download_file, read_content, delete


def main():
    download_file()
    content = read_content()
    sort_in_files(content)
    after_read_statistic(content)
    delete()


if __name__ == '__main__':
    main()
