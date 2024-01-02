import requests
import re
import json
import tqdm
import os
import urllib3
urllib3.disable_warnings()

proxies={'http':'192.168.2.125:8118',
    'https':'192.168.2.125:8118'}

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'ua=9c1ce27f08b16479d2e17743062b28ed; platform=pc; bs=oxkksk2usw89dcpqtxl1a5yisbg6nqx8; bsdd=oxkksk2usw89dcpqtxl1a5yisbg6nqx8; ss=197132380640148996; fg_0d2ec4cbd943df07ec161982a603817e=44845.100000; fg_f916a4d27adf4fc066cd2d778b4d388e=62645.100000; fg_fa3f0973fd973fca3dfabc86790b408b=56197.100000; __s=658D8271-42FE722901BB3532BC-7FFA14E2; __l=658D8271-42FE722901BB3532BC-7FFA14E2; tj_UUID=ChCPzDVbfnxFK4x0lJ_hgeF7EgsIh_u1rAYQu-ykBw==; tj_UUID_v2=ChCPzDVbfnxFK4x0lJ_hgeF7EgsIh_u1rAYQu-ykBw==; d_fs=1; d_uidb=37564869-a0af-a0cf-0ad2-35948c9586cf; d_uid=37564869-a0af-a0cf-0ad2-35948c9586cf; d_uidb=37564869-a0af-a0cf-0ad2-35948c9586cf; _gid=GA1.2.234460411.1703772790; RNLBSERVERID=ded4403; accessAgeDisclaimerPH=1; _ga=GA1.1.871306413.1703772790; _ga_B39RFFWGYY=GS1.1.1703772791.1.1.1703773382.60.0.0'
}

def url_get(url):
    res = requests.get(url, headers=header, verify=False, proxies= proxies, allow_redirects=False)
    return res.text
def safeFilename(filename, replace=''):
    return re.sub(re.compile(
        '[/\\\:*?"<>|]')
        , replace,
        filename
    )
#
def download(url: str, path: str):
    if url == "Pass":
        print('Pass')
        return -1
    # 用流stream的方式获取url的数据
    resp = requests.get(url, stream=True, headers=header, verify=False, proxies= proxies)
    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-length', 0))
    # 打开当前目录的fname文件(名字你来传入)
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    with open(path, 'wb') as file, tqdm.tqdm(
        desc=path,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def video_download(url, path = ''):
    '''视频详情页链接，下载地址目录'''

    # 创建目的文件夹
    if not os.path.exists(path):
        os.makedirs(path)

    # 获取含地址信息的Json
    JSObject = re.findall('var flashvars_\d{9} = (.*})', url_get(url))
    try:
        json_content = json.loads(JSObject[0])
    except:
        return

    # 获取video_title
    video_title = json_content['video_title']
    # 规范化windows命名
    video_title = safeFilename(video_title)

    # 找到含有MP4下载详情页的连接
    for item in json_content['mediaDefinitions']:
        if item['format'] == 'mp4':
            down_url_page = item['videoUrl']
    down_url_detal = url_get(down_url_page)
    json_down_url_detal = json.loads(down_url_detal)

    # 找到1080p格式下载地址
    for item in json_down_url_detal:
        if item['quality'] == '1080':
            down_url = item['videoUrl']
        else:
            down_url = "Pass"


    # 文件地址
    file_dir = os.path.join(path,f'{video_title}.mp4')

    # 调用download函数下载
    download(down_url,file_dir)


def main(search_word, page_range, path = ""):

    son_path = search_word
    path = os.path.join(path, son_path)
    for page in range(page_range[0],page_range[1]+1):
        if page == 1:
            current_page_url = f'https://cn.pornhub.com/video/search?search={search_word}&hd=1'
        else:
            current_page_url = f'https://cn.pornhub.com/video/search?search={search_word}&hd=1page={page}'

        current_page_content = url_get(current_page_url)

        oneppage_detal_url_list = re.findall('<a    href="(/view_video.php\?viewkey=[a-zA-Z0-9]{1,30})" title="(.*?)"', current_page_content)
        for item in oneppage_detal_url_list:

            one_video_detal_url = 'https://cn.pornhub.com' + item[0]

            video_download(one_video_detal_url, path)

if __name__ == '__main__':
    main('xxx',(1,3), path = r"")








