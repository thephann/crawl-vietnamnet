import json
import scrapy
from datetime import datetime

OUTPUT_FILENAME = 'D:/ExampleCode/ExampleCode/output/vtc/vtc_{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))


class VtcnewsSpider(scrapy.Spider):
    name = 'vtc'
    allowed_domains = ['vtc.vn']
    start_urls = ['https://vtc.vn/']
    CRAWLED_COUNT = 0

    def parse(self, response):
        if response.status == 200 and response.css('body[class="load-news-detail ads"]::attr("data-page")').get() == 'detail':
            print('Crawling from:', response.url)
            data = {
                'link': response.url,
                'title': response.css('h1.font28.bold.lh-1-3::text').get(),
                'category':response.css('div.mb15.gray-91.font12 a::attr(title)').get(),
                'date': response.css('span.time-update.mr10::text').get(),
                'related news': '\n'.join([
                    k.strip() for k in response.css('h3.borbot-e0-doted.pb5.mb5.font14.pl15.relative a::attr(title)').get().split(',')
                ]),
                'description':response.css('h4.font16.bold.mb15::text').get(),

                'content': '\n'.join([
                    ''.join(c.css('*::text').getall())
                    for c in response.css('div.edittor-content.box-cont.clearfix p')
                ]),

                'tags': '\n'.join([
                    k.strip() for k in response.css('li.inline.mr5.mb5 > div > a::attr("title")').get().split(',')
                ]),
            }

            with open(OUTPUT_FILENAME, 'a', encoding='utf8') as f:
                f.write('\n')
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.CRAWLED_COUNT += 1
                self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
                print('SUCCESS:', response.url)

        yield from response.follow_all(css='a[href^="https://vtc.vn/"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)
