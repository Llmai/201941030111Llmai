from selenium import webdriver


if __name__ == '__main__':
    try:
        pages = int(input('请输入爬取的页'))
    except Exception:
        print('请输入一个大于0的数')
    driver = webdriver.Chrome()
    url = 'https://www.kan302.com/mh/china/{}.shtml'.format(pages)
    driver.get(url)
    videos_dl = driver.find_element_by_id('cont_pub')
    video_list = videos_dl.find_elements_by_tag_name('dl')
    videos = []
    for video in video_list:
        info = {'title': video.find_element_by_class_name('tit').text,
                'episodes': video.find_element_by_class_name('zx').text,
                'update_date': video.find_element_by_tag_name('i').text,
                'introduction': video.find_element_by_class_name('gray').text,
                'img': video.find_element_by_tag_name('img').get_attribute('src')
                }
        videos.append(info)
    for i in range(len(videos)):
        print(videos[i])
    driver.close()
