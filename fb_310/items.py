# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FootballItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Football_310_CompetitionItem(scrapy.Item):
    competitiongroups = scrapy.Field()
    competitiongroupc = scrapy.Field()
    competitiongroupe = scrapy.Field()
    continentsid = scrapy.Field()
    leagueId = scrapy.Field()
    leaguegroups = scrapy.Field()
    leaguegroupc = scrapy.Field()
    leaguegroupe = scrapy.Field()
    leaguegroupid = scrapy.Field()
    update_dt = scrapy.Field()

#联赛介绍
class Football_310_LeagueItem(scrapy.Item):
    leagueid = scrapy.Field()
    leaguenames = scrapy.Field()
    leaguenamec = scrapy.Field()
    leaguenameeng = scrapy.Field()
    season = scrapy.Field()
    sumround = scrapy.Field()
    currentround = scrapy.Field()
    leagua = scrapy.Field()
    leaguaeng = scrapy.Field()
    leaguedesc = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()

#球队介绍
class Football_310_TeamItem(scrapy.Item):
    leagueid = scrapy.Field()
    teamid = scrapy.Field()
    teamnames = scrapy.Field()
    teamnamec = scrapy.Field()
    teamnameeng = scrapy.Field()
    unknowid = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()

#比赛Item
class Football_310_MatchItem(scrapy.Item):
    matchid = scrapy.Field()
    leagueid = scrapy.Field()
    unknownid = scrapy.Field()
    season = scrapy.Field()
    roundtime = scrapy.Field()
    matchtime = scrapy.Field()
    hometeamid = scrapy.Field()
    guestteamid = scrapy.Field()
    sorce = scrapy.Field()
    sorce_half = scrapy.Field()
    hometeamlab = scrapy.Field()
    guestteamlab = scrapy.Field()
    rq_all = scrapy.Field()
    rq_half = scrapy.Field()
    dx_all = scrapy.Field()
    dx_half = scrapy.Field()
    update_dt = scrapy.Field()



class Football_310_SeasonItem(scrapy.Item):
    gameId = scrapy.Field()
    season = scrapy.Field()
    gamegroupid = scrapy.Field()
    continentsid = scrapy.Field()

class Football_310_BJDCItem(scrapy.Item):
    cc = scrapy.Field()
    ss = scrapy.Field()
    matchTime = scrapy.Field()
    zdrq = scrapy.Field()
    bf1 = scrapy.Field()
    kd = scrapy.Field()
    rqspf = scrapy.Field()
    jqs = scrapy.Field()
    sxds = scrapy.Field()
    bf2 = scrapy.Field()
    bqcsf = scrapy.Field()
    hgpk = scrapy.Field()
    sj = scrapy.Field()
    matchId = scrapy.Field()
    sp_count = scrapy.Field()

class Football_310_JCZQItem(scrapy.Item):
    cc = scrapy.Field()
    ss = scrapy.Field()
    zdrq = scrapy.Field()
    bf1 = scrapy.Field()
    kd = scrapy.Field()
    bc = scrapy.Field()
    rqspf = scrapy.Field()
    spf = scrapy.Field()
    bf2 = scrapy.Field()
    jqzs = scrapy.Field()
    bqc = scrapy.Field()
    hgpk = scrapy.Field()
    sj = scrapy.Field()
    matchId = scrapy.Field()
    timeInterval = scrapy.Field()

class Football_310_OPDictItem(scrapy.Item):
    GameCompanyId = scrapy.Field()
    Company_OPID = scrapy.Field()
    Company_engName = scrapy.Field()
    Company_chnName = scrapy.Field()
    matchId = scrapy.Field()
    update_dt = scrapy.Field()

class Football_310_OPItem(scrapy.Item):
    Company_OPID = scrapy.Field()
    zs = scrapy.Field()
    h = scrapy.Field()
    ks = scrapy.Field()
    # zsl = scrapy.Field()
    # hl = scrapy.Field()
    # ksl = scrapy.Field()
    # fhl = scrapy.Field()
    klzs1 = scrapy.Field()
    klzs2 = scrapy.Field()
    klzs3 = scrapy.Field()
    bhsj = scrapy.Field()
    matchId = scrapy.Field()
    update_dt = scrapy.Field()

class Football_310_YPDictItem(scrapy.Item):
    bcgs = scrapy.Field()
    zd = scrapy.Field()
    pk = scrapy.Field()
    kd = scrapy.Field()
    zd2 = scrapy.Field()
    pk2 = scrapy.Field()
    kd2 = scrapy.Field()
    bcgsId = scrapy.Field()
    matchId = scrapy.Field()
    update_dt = scrapy.Field()

class Football_310_YPItem(scrapy.Item):
    sj = scrapy.Field()
    bf = scrapy.Field()
    zd = scrapy.Field()
    pk = scrapy.Field()
    kd = scrapy.Field()
    bhsj = scrapy.Field()
    status = scrapy.Field()
    bcgsId = scrapy.Field()
    matchId = scrapy.Field()
    update_dt = scrapy.Field()

class Football_310_select5from11Item(scrapy.Item):
    IssueNum = scrapy.Field()
    Result = scrapy.Field()
    AwardTime = scrapy.Field()
    datadate = scrapy.Field()

#采集失败的matchid专门存储的表
class Football_sporttery_loseMatchId(scrapy.Item):
    matchid = scrapy.Field()
    spidername = scrapy.Field()
    tablename = scrapy.Field()
    url = scrapy.Field()
    losereason = scrapy.Field()