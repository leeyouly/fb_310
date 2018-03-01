# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from fb_310.data import ImportFootball_CompetitionStorage,ImportFootball_LeagueStorage,ImportFootball_TeamStorage,\
    ImportFootball_MatchStorage,ImportFootball_BjdcKjjgStorage,ImportFootball_JczqKjjgStorage,ImportFootball_OPDictStorage,\
    ImportFootball_OPStorage,ImportFootball_YPDictStorage,ImportFootball_YPStorage,ImportFootball_Select5from11Storage
from fb_310.items import Football_310_CompetitionItem,Football_310_LeagueItem,Football_310_TeamItem,\
    Football_310_MatchItem, Football_310_BJDCItem,Football_310_JCZQItem,Football_310_OPItem,Football_310_OPDictItem,\
    Football_310_YPDictItem,Football_310_YPItem,Football_310_select5from11Item
from scrapy.utils.project import get_project_settings

class FootballPipeline(object):
    def process_item(self, item, spider):
        return item


class ImportFootball_CompetitionSave(object):
    def __init__(self):
        self.storage = ImportFootball_CompetitionStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_CompetitionItem):
            if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ImportFootball_LeagueSave(object):
    def __init__(self):
        self.storage = ImportFootball_LeagueStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_LeagueItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ImportFootball_TeamSave(object):
    def __init__(self):
        self.storage = ImportFootball_TeamStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_TeamItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ImportFootball_MatchSave(object):
    def __init__(self):
        self.storage = ImportFootball_MatchStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_MatchItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item











class ImportFootball_BjdcKjjgSave(object):
    def __init__(self):
        self.storage = ImportFootball_BjdcKjjgStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_BJDCItem):
            if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ImportFootball_JczqKjjgSave(object):
    def __init__(self):
        self.storage = ImportFootball_JczqKjjgStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_JCZQItem):
            if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ImportFootball_OPSave(object):
    def __init__(self):
        self.storage = ImportFootball_OPStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_OPItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ImportFootball_OPDictSave(object):
    def __init__(self):
        self.storage = ImportFootball_OPDictStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_OPDictItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ImportFootball_YPDictSave(object):
    def __init__(self):
        self.storage = ImportFootball_YPDictStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_YPDictItem):
            if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ImportFootball_YPSave(object):
    def __init__(self):
        self.storage = ImportFootball_YPStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_YPItem):
            if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ImportFootball_Select5from11Save(object):
    def __init__(self):
        self.storage = ImportFootball_Select5from11Storage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Football_310_select5from11Item):
            if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

