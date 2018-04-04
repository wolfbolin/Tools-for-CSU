# -*- coding: utf-8 -*-
import os
import re
import time
import json


def read_json():
    json_path = input("请输入学生信息数据路径：")
    if os.path.exists(json_path) is False:
        print("该文件不存在..程序自动退出")
        time.sleep(3)
        exit(0)
    json_file = open(json_path, "r", encoding="UTF-8")
    json_str = json_file.read()
    data = json.loads(json_str.encode("UTF-8"))
    return data


def rename(path, file_name, glossary, pattern):
    print("正在修改", file_name)
    (name, extension) = os.path.splitext(file_name)
    for item in glossary:
        if re.search(item, name) is not None:
            new_file_name = pattern.replace("dd", glossary[item])
            new_file_name = new_file_name.replace("ss", item)
            os.rename(os.path.join(path, file_name), os.path.join(path, new_file_name + extension))
            break


if __name__ == "__main__":
    json_data = read_json()
    folder_path = input("请输入需要纠正命名的文件夹路径：")
    if os.path.exists(folder_path) is False:
        print("该文件夹不存在..程序自动退出")
        time.sleep(3)
        exit(0)

    name_pattern = input("请输入命名格式（用dd代表学号，用ss代表姓名）")
    name_pattern = name_pattern.strip()
    file_list = os.listdir(folder_path)
    for file in file_list:
        rename(folder_path, file, json_data, name_pattern)
