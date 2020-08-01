#coding:utf-8

# ffmpeg 递归转换小工具
# 20200113

import os, subprocess, re, time

# ffmpeg 执行程序
ffmpeg = 'ffmpeg'

# 处理文件名匹配 支持正则
inFileEnd = '.*.mp4'

# 输出文件名后缀
outFileEnd = '.mp4'

# 使用编码
cv = 'h264_nvenc'

# 码率限制 设置为None则不判断
bitrateLimit = 10000


def doFfmpeg(root, f, fileFullPath):
    tmpFile = os.path.join(root, str(time.time()) + outFileEnd)
    cmd = '{} -i "{}" -c:a copy -c:v {} {}'.format(ffmpeg, fileFullPath, cv, tmpFile)
    print(cmd)
    os.system(cmd)
    # 删除原文件并移动文件
    if os.path.getsize(tmpFile) > 0:
        os.remove(fileFullPath)
        os.rename(tmpFile, fileFullPath)

for root, dirs, files in os.walk('.'):
    for f in files:
        #不区分大小写哦
        if re.match(inFileEnd, f, re.I):
            fileFullPath = os.path.join(root, f)
            print(fileFullPath)
            if bitrateLimit:
                cmd = '{} -i "{}" 2>&1 | {} bitrate'.format(ffmpeg, fileFullPath, 'findstr' if os.name == 'nt' else 'grep')
                print(cmd)
                out = subprocess.getoutput(cmd)
                bitrate = re.search("bitrate: (\\d+)", out)
                # print(bitrate)
                if bitrate:
                    bitrate = bitrate.group(1)
                    if int(bitrate) > bitrateLimit:
                        doFfmpeg(root, f, fileFullPath)
                else:
                    print('NO bitrate: ' + fileFullPath)
            else:
                doFfmpeg(root, f, fileFullPath)