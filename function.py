import requests
import time
import yagmail

now = time.localtime(time.time())

def get_bvids_by_keyword(keyword, pages):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com",
        'Cookie': "buvid3=72AD3B0B-8DE2-8177-DE10-DD3A53EAF7D935618infoc; b_nut=1740628735; _uuid=9A645D24-E1CD-76C5-91038-E75B1A6293CA35782infoc; enable_web_push=DISABLE; buvid4=93811E2B-00EB-FC83-6D3D-D403D0DFA88536173-025022703-fi7X5tJQCNPvV%2BeKoVnoGQ%3D%3D; buvid_fp=ea652ec7ba30027ef24be3828e114b15; DedeUserID=488981315; DedeUserID__ckMd5=c1e2dcbefbc73b6c; rpdid=|(J|~Ju)umk|0J'u~R|Yk)~)k; header_theme_version=CLOSE; enable_feed_channel=ENABLE; CURRENT_QUALITY=80; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDg4NzM1NTUsImlhdCI6MTc0ODYxNDI5NSwicGx0IjotMX0.SqPePuLvt8SEv93AQWFP-Y18dlNl_01k2SE_ovyqrsM; bili_ticket_expires=1748873495; SESSDATA=e468fcf1%2C1764166356%2C31de1%2A51CjC1UJcqaLRH_HlPUB2lFfZ-OjO-rhECW7ipFFXPX4SH-IaLvj2Gcz3y25eSNO4nukkSVkJZNWdKYjl1eDR1OS03V3dzNGJOR01paExlVE1GZnRwUlhTN3p1Y2h4ZFBFUTdIbzlzb0V0Sk90bk5qeXc3MFh6RU1DUGx0RkF4eDh5VDdfSmJ4V0NBIIEC; bili_jct=f240ebdf305eab43da2bbb304bf00d4e; bp_t_offset_488981315=1072795123013648384; b_lsid=2310E172B_1972A2325CE; sid=8hkf67br; CURRENT_FNVAL=2000; home_feed_column=4; browser_resolution=150-695"
    }
    bvid_list = []
    for page in range(1, pages + 1):
        params = {
            "search_type": "video",
            "keyword": keyword,
            "page": page
        }
        url = "https://api.bilibili.com/x/web-interface/search/type"
        response = requests.get(url, headers=headers, params=params,timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get("data", {}).get("result", [])
            for item in results:
                bvid = item.get("bvid")
                if bvid:
                    bvid_list.append(bvid)
                    # print(f"{item['title']} -> https://www.bilibili.com/video/{bvid}")
        else:
            print("请求搜索结果失败，状态码：", response.status_code)

    return bvid_list

def get_url_information(bvid):

    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    link = f'https://www.bilibili.com/video/{bvid}'
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://www.bilibili.com/video/{bvid}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()["data"]
        # print("标题：", data["title"])
        # print("播放：", data["stat"]["view"])
        # print("点赞：", data["stat"]["like"])
        # print("投币：", data["stat"]["coin"])
        # print("收藏：", data["stat"]["favorite"])
        # print("UP主：", data["owner"]["name"])
        # print("发布时间：", data["pubdate"])
        k=int(data['stat']['view'])
        if k <2000:
            k = 0.0002*pow(k-2000,2)+2000
        elif k > 100000:
            k = k * 2

        hot = ((int(data["stat"]["like"]) * 0.8)+(int(data["stat"]["coin"])*4)+(int(data["stat"]["coin"]*2)))/(0.4*k)

        dik = {
            "title" : data["title"],
            "link" : link,
            "hot" : hot,
            'time' : data["pubdate"],
            "view": data["stat"]["view"],
            "like" : data["stat"]["like"],
            "coin" : data["stat"]["coin"],
            "up" : data["owner"]["name"],
        }

        return dik
    else:
        print(f'获取数据失败!,状态码{response.status_code}')
        return False

def main_work(keyword="东方PROJECT",pages=5):
    a = get_bvids_by_keyword(keyword,pages)
    rep = f"""
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{keyword}近期视频推送-{time.strftime('%Y-%m-%d-%H:%M', now)}</title>
    """
    rep += """    <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #aaa;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #eee;
            }
            a {
                color: #1a0dab;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    """
    rep += f"""</head>
    <body>
        <h1>{keyword}视频推送    {time.strftime('%Y-%m-%d', now)}版</h1>
        <table>
            <tbody>
    """
    for i in a:
        data = get_url_information(i)
        detime = int(time.time()) - data.get("time")
        if 10518912 > detime > 14400 and 0.02 <= data["hot"] <= 0.8:
            # print(data['title'])
            # print(data['hot'])
            # print(data['link'])
            rep += f"""
                <tr>
                    <td><a href="{data['link']}" target="_blank">{data['title']}</a></td>
                    <td>UP主:{data["up"]}</td>
                    <td>播放量{data["view"]} 点赞{data["like"]} 投币 {data["coin"]}</td>
                </tr>
    """
    rep += """
            </tbody>
        </table>
    </body>
    </html>
    """
    file = f'report/result_in{time.strftime('%Y%m%d_%H%M%S', now)}.html'
    with open(file, 'w', encoding='utf-8') as f:
        f.write(rep)
    print(f"已将文件保存至{file}")
    return file

def email_send(keyword,from_email, password,file,to_email,host="smtp.qq.com"):
    email_user = from_email
    email_password = password
    email_host = host
    email_recipients = f"{to_email}"
    yag = yagmail.SMTP(email_user, email_password, email_host)
    subject = f"{keyword}视频-{time.strftime('%Y年%m月%d日')}"
    contents = [
                f'{keyword}视频推送',
                file
            ]
    yag.send(to=email_recipients, subject=subject, contents=contents)
    print(f'已成功发送至{to_email}')
    yag.close()