from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler
from icrawler import ImageDownloader

from ReadData import getListNames


class PrefixNameDownloaderGoogle(ImageDownloader):
    prefix = 'google'

    def get_filename(self, task, default_ext):
        filename = super(PrefixNameDownloaderGoogle, self).get_filename(
            task, default_ext)
        return self.prefix + '_' + filename


class PrefixNameDownloaderBing(ImageDownloader):
    prefix = 'bing'

    def get_filename(self, task, default_ext):
        filename = super(PrefixNameDownloaderBing, self).get_filename(
            task, default_ext)
        return self.prefix + '_' + filename


list_names = getListNames()
print(list_names)
for name in list_names:
    google_crawler = GoogleImageCrawler(
        downloader_cls=PrefixNameDownloaderGoogle,
        feeder_threads=1,
        parser_threads=1,
        downloader_threads=4,
        storage={'root_dir': 'images/' + name})

    google_crawler.crawl(keyword=name, offset=0, max_num=1000,
                         min_size=(200, 200), max_size=None, file_idx_offset=0)

    bing_crawler = BingImageCrawler(downloader_cls=PrefixNameDownloaderBing,
                                    downloader_threads=4,
                                    storage={'root_dir': 'images/' + name})
    bing_crawler.crawl(keyword=name, filters=None, offset=0, max_num=1000)
