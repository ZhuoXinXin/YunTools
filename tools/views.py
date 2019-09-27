# coding=utf-8
from django.shortcuts import render
import time
from aip import AipOcr
import json
from django.http import FileResponse


# 菜单
def Menu(request):
    return render(request, 'Menu.html')


# 公积金
def Acc(request):
    return render(request, 'Acc.html')


# 文字识别
def CharRec(request):
    if request.method == 'POST':
        img = request.FILES.get('img')
        # 定义常量
        APP_ID = '15760884'
        API_KEY = 'vO2shV4ihdpsPtO9iu73IUEe'
        SECRET_KEY = 'XdLOkaf7bmBGdMG1SN8hjqjOOZg92sX0'
        aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        error = '0'
        try:
            # 上传图片
            url = 'tools/static/CharRecResult/' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.jpg'
            with open(url, 'wb') as f:
                # pic.chunks()循环读取图片内容，每次只从本地磁盘读取一部分图片内容，加载到内存中，并将这一部分内容写入到目录下，写完以后，内存清空；下一次再从本地磁盘读取一部分数据放入内存。就是为了节省内存空间。
                for data in img.chunks():
                    f.write(data)

            # 识别图片文字
            def get_file_content(url):
                with open(url, 'rb') as fp:
                    return fp.read()

            options = {
                'detect_direction': 'true',
                'language_type': 'CHN_ENG',
            }

            # 调用通用文字识别接口
            result = aipOcr.basicGeneral(get_file_content(url), options)
            result = (eval(json.dumps(result, ensure_ascii=False)))['words_result']
            realresult = []
            for i in result:
                realresult.append(i['words'])
            return render(request, 'CharRec.html', {'realresult': realresult,
                                                    'error': error})

        except Exception as e:
            error = '图片转换异常，异常信息为：{0}'.format(e)
            return render(request, 'CharRec.html', {'error': error})

    return render(request, 'CharRec.html')


def file_down(request):
    file = open('/home/amarsoft/download/example.tar.gz', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
    return response
