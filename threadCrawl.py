import threading
from queue import Queue
from selenium import webdriver

CRAW_EXIT = False


class ThreadCrawl(threading.Thread):
    def __init__(self, thread_name, page_queue, data_queue):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.page_queue = page_queue
        self.data_queue = data_queue

    def run(self):
        print('启动' + self.thread_name)
        try:  # 连接线程成功进入BS4查找内容
            page = self.page_queue.get(False)
            url = 'https://www.kan302.com/mh/china/{}.shtml'.format(page)
            print(url)
            self.data_queue.put(url)
        except Exception:
            print('采集线程错误')
        print('结束：' + self.thread_name)


PARSE_EXIT = False  # 解析队列标识，如果为True, 表示数据队列为空，全部数据被解析


class ThreadParse(threading.Thread):
    def __init__(self, thread_name, data_queue, video_s, lock):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.data_queue = data_queue
        self.videos = video_s
        self.lock = lock

    def run(self):
        print('启动：' + self.thread_name)
        try:
            content = self.data_queue.get(False)
            self.parse(content)
        except Exception as e:
            print('线程解析失败', e)

    def parse(self, content):
        driver = webdriver.Chrome()
        driver.get(content)
        videos_dl = driver.find_element_by_id('cont_pub')
        video_list = videos_dl.find_elements_by_tag_name('dl')
        for video in video_list:
            info = {'title': video.find_element_by_class_name('tit').text,
                    'episodes': video.find_element_by_class_name('zx').text,
                    'update_date': video.find_element_by_tag_name('i').text,
                    'introduction': video.find_element_by_class_name('gray').text,
                    'img': video.find_element_by_tag_name('img').get_attribute('src')
                    }
            with self.lock:
                self.videos.append(info)
        for i in range(len(self.videos)):
            print(self.videos[i])
        driver.close()


def main(Pages):
    page_queue = Queue(Pages)
    for i in range(1, Pages + 1):
        page_queue.put(i)
    videos = []
    data_queue = Queue()
    lock = threading.Lock()
    # 采集线程的名字列表
    crawNames = ['采集1#', '采集2#', '采集3#', '采集4#', '采集5#', '采集6#']
    threadCrawls = []
    for threadName in crawNames:
        crawl = ThreadCrawl(threadName, page_queue, data_queue)
        crawl.start()
        threadCrawls.append(crawl)
    parseNames = ['解析1#', '解析2#', '解析3#', '解析4#', '解析5#', '解析6#']
    ThreadParses = []
    for parseName in parseNames:
        parse = ThreadParse(parseName, data_queue, videos, lock)
        parse.start()
        ThreadParses.append(parse)

    while not page_queue.empty():
        pass

    global PARSE_EXIT
    PARSE_EXIT = True
    print('数据队列dataQueue为空')
    for thread in ThreadParses:
        thread.join()


if __name__ == '__main__':
    try:
        pages = int(input('请输入爬取多少页'))
    except Exception:
        print('请输入一个大于0的数')
    main(pages)
