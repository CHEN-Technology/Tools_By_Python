import os
import shutil
import subprocess

import_path = input(r"请输入文件夹路径：")
# print(import_path)

print("创建临时目录")

temp_folder = os.path.join(import_path, 'temp')

if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

print("转换为mts")

# 获取文件夹中所有 .mp4 文件的路径
mp4_files = [os.path.join(import_path, f)
             for f in os.listdir(import_path) if f.endswith('.mp4')]


# 对每一个 .mp4 文件执行 ffmpeg 命令
for file in mp4_files:
    filename, ext = os.path.splitext(file)
    relative_path = os.path.relpath(filename, start=import_path)
    print(relative_path)
    cmd = [
        "ffmpeg", "-i", file, "-q", "0", import_path + "/temp/" + relative_path + ".mts"
    ]
    subprocess.run(cmd)

print("转换完成")
print("获取转换后的文件名")

path_list = os.listdir(import_path + "/temp")
# print(path_list)

mts_files = [f for f in path_list if f.endswith('.mts')]
# print(mts_files)

print("开始合并")

with open(import_path + '/temp/ffmpeg.txt', 'w') as f:
    for path in mts_files:
        f.writelines(f"file '{path}'\n")
    print("写入txt")

proc = subprocess.Popen(
    f"ffmpeg -f concat -vsync vfr -safe 0 -i {import_path}/temp/ffmpeg.txt -c copy {import_path}/temp/temp.mp4", stdin=None, shell=True
)
outinfo, errinfo = proc.communicate()
print(outinfo, errinfo)
print("合并完成")

print("开始压制")

proc = subprocess.Popen(
    f"ffmpeg -i {import_path}/temp/temp.mp4 -c:v hevc_nvenc -x265-params crf=18:preset=placebo {import_path}/output.mp4", stdin=None, shell=True
)
outinfo, errinfo = proc.communicate()
print(outinfo, errinfo)
print("压制完成")

print("删除临时文件")

folder_path = import_path + "/temp"

items_in_folder = os.listdir(folder_path)

# 删除文件夹中的所有文件
for item_in_folder in items_in_folder:
    item_path = os.path.join(folder_path, item_in_folder)
    if os.path.isfile(item_path):
        os.remove(item_path)
    else:
        shutil.rmtree(item_path)

# 删除文件夹
os.rmdir(folder_path)


print("删除完成")
