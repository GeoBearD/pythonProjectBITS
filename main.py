from sort import sort_in_files
from statistics import print_numbers, print_yob, print_namesakes
from file import download_file, read_content, delete


def main():
    download_file()
    content = read_content()
    sort_in_files(content)
    print_numbers(content)
    print_yob(content)
    print_namesakes(content)
    delete()


if __name__ == '__main__':
    main()
