# -*- coding: utf-8 -*-
from scrapy import Request, Spider


class QuestionsPerTopicSpider(Spider):
    name = 'questions_per_topic'
    allowed_domains = ['quora.com']
    start_urls = ['https://quora.com/topic/Scrapy']

    def parse(self, response):
        questions = response.xpath('//*[@class="paged_list_wrapper"]/div')
        for q in questions:
            url = q.xpath('.//*[@class="question_link"]/@href').extract_first()
            absolute_url = response.urljoin(url)
            yield Request(absolute_url, callback=self.parse_question)

    def parse_question(self, response):
        topics = response.xpath('//*[@class="name_text"]/span/span/text()').extract()
        question_title = response.xpath('//*[@class="question_text_edit"]/h1/span/span/span/text()').extract_first()
        answers_count = response.xpath('//*[@class="answer_count"]/text()').extract_first().split()[0]
        # Question always be the first pagedlist_item.extract_first
        question = response.xpath('.//*[@class="pagedlist_item"]')[0]
        author_name = question.xpath('.//*[@class="user"]/text()').extract_first()
        author_url = question.xpath('.//*[@class="user"]/@href').extract_first()
        author_intro = question.xpath('.//*[@class="feed_item_answer_user"]/span/span[2]/text()').extract_first().split(' ',1)[1]
        question_views = question.xpath('.//*[@class="meta_num"]/text()').extract_first()
        question_created = question.xpath('.//*[@class="datetime"]/text()').extract_first()
        #question_text = ''.join(question.xpath('.//*[@class="ui_qtext_rendered_qtext"]/text()').extract())
        yield {'Topics': topics,
               'Question Title': question_title,
               'Answer Count': answers_count,
               'Author': author_name,
               'Author Profile': author_url,
               'Author Brief Intro': author_intro,
               'Question Views': question_views,
               'Question CreatedAt': question_created}
