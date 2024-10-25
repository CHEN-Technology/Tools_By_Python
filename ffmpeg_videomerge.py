import os
import shutil
import subprocess

import_path = input(r"请输入文件夹路径：")
# print(import_path)

print("创建临时目录")

temp_folder = os.path.join(import_path, 'temp')

if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# 获取文件夹中所有 .mkv 文件的路径
mkv_files = [os.path.join(import_path, f)
             for f in os.listdir(import_path) if f.endswith('.mkv')]

# print(mkv_files)

print("开始合并")

with open(import_path + '/temp/ffmpeg.txt', 'w') as f:
    for path in mkv_files:
        f.writelines(f"file '{path}'\n")
    print("写入txt")

proc = subprocess.Popen(
    f"ffmpeg -f concat -vsync vfr -safe 0 -i {import_path}/temp/ffmpeg.txt -c copy {import_path}/temp/temp.mkv", stdin=None, shell=True
)
outinfo, errinfo = proc.communicate()
print(outinfo, errinfo)
print("合并完成")