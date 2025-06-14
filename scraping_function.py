import requests
from bs4 import BeautifulSoup as bs

def scraping_blog(keyword, top_n):
    url =  f'https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query={keyword}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    post_list = [] # 블로그 포스팅 주소를 저장하는 리스트

    try: # 키워드로 검색해서 블로그 포스팅 주소를 리스트에 저장
        res = requests.get(url, headers)
        soup = bs(res.text, features="html.parser")
        box_list = soup.find('div', class_='api_subject_bx').find_all('div','detail_box')
        post_count = 0
        while True:
            post = box_list[post_count].find('div', 'title_area') # 포스팅 박스 찾아서
            post_link = post.find('a').get('href') # 링크 따고
            post_count += 1
            if post_link.find('ader') != -1:
                continue
            post_list.append(post_link.replace('blog', 'm.blog')) # blog 주소를 m.blog로 바꿈 ( 모바일 버전에서 크롤링해야 어려움없이 가져올 수 있음 )
            if len(post_list) == top_n:
                break
    except Exception as e:
        print(e)

    text_list = [] # 포스팅을 str로 저장하는 리스트
    try:
        for post_url in post_list:
            post_res = requests.get(post_url, headers = headers)
            post_soup = bs(post_res.text, features="html.parser")
            text_list.append('\n'.join([i.text.strip().replace('\u200b', '') for i in post_soup.find_all('p')])) # 특수공백 제거, 좌우 공백 제거
    except Exception as e:
        print(e)
    return text_list