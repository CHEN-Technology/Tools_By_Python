import os
import shutil
import subprocess

import_path = input(r"请输入文件夹路径：")
# print(import_path)

print("创建输出目录")

temp_folder = os.path.join(import_path, 'output')

if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

print("转换中")

# 获取文件夹中所有 .mp4 文件的路径
mp4_files = [os.path.join(import_path, f)
             for f in os.listdir(import_path) if f.endswith('.mp3')]


# 对每一个 .mp3 文件执行 ffmpeg 命令
for file in mp4_files:
    filename, ext = os.path.splitext(file)
    relative_path = os.path.relpath(filename, start=import_path)
    print(relative_path)
    cmd = [
        "ffmpeg", "-i", file, import_path + "/output/" + relative_path + ".wav"
    ]
    subprocess.run(cmd)

print("转换完成")