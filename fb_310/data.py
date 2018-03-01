from spiderlib.data import DataStorage
import PyDB


class ImportFootball_CompetitionStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_310_COMPETITION'
        self.db.set_metadata(self.table_name, [
            PyDB.IntField("gameId", is_key=True),
            PyDB.StringField("competitiongroups"),
            PyDB.StringField("competitiongroupc"),
            PyDB.StringField("competitiongroupe"),
            PyDB.IntField("continentsid"),
            PyDB.StringField("leaguegroups"),
            PyDB.StringField("leaguegroupc"),
            PyDB.StringField("leaguegroupe"),
            PyDB.IntField("leaguegroupid"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportFootball_LeagueStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_310_LEAGUE1'
        self.db.set_metadata(self.table_name, [
            PyDB.IntField("leagueid", is_key=True),
            PyDB.StringField("leaguenames"),
            PyDB.StringField("leaguenamec"),
            PyDB.StringField("leaguenameeng"),
            PyDB.StringField("season"),
            PyDB.IntField("sumround"),
            PyDB.IntField("currentround"),
            PyDB.StringField("leagua"),
            PyDB.StringField("leaguaeng"),
            PyDB.StringField("leaguedesc"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("source"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportFootball_TeamStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_310_Team'
        self.db.set_metadata(self.table_name, [
            PyDB.IntField("leagueid", is_key=True),
            PyDB.IntField("teamid", is_key=True),
            PyDB.StringField("teamnames"),
            PyDB.StringField("teamnamec"),
            PyDB.StringField("teamnameeng"),
            PyDB.IntField("unknowid"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("source"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportFootball_MatchStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_310_MATCH1'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("matchid", is_key=True),
            PyDB.StringField("leagueid"),
            PyDB.StringField("unknownid"),
            PyDB.StringField("season"),
            PyDB.StringField("roundtime"),
            PyDB.DateField("matchtime"),
            PyDB.StringField("hometeamid"),
            PyDB.StringField("guestteamid"),
            PyDB.StringField("sorce"),
            PyDB.StringField("sorce_half"),
            PyDB.StringField("hometeamlab"),
            PyDB.StringField("guestteamlab"),
            PyDB.StringField("rq_all"),
            PyDB.StringField("rq_half"),
            PyDB.StringField("dx_all"),
            PyDB.StringField("dx_half"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("source"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()



class ImportFootball_BjdcKjjgStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 't_310_bjdc_kjjg'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("cc"),
            PyDB.StringField("ss"),
            PyDB.StringField("matchTime"),
            PyDB.StringField("zdrq"),
            PyDB.StringField("bf1"),
            PyDB.StringField("kd"),
            PyDB.StringField("rqspf"),
            PyDB.StringField("jqs"),
            PyDB.StringField("sxds"),
            PyDB.StringField("bf2"),
            PyDB.StringField("bqcsf"),
            PyDB.StringField("hgpk"),
            PyDB.StringField("sj"),
            PyDB.StringField("sp_count"),
            PyDB.StringField("matchId", is_key=True),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportFootball_JczqKjjgStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 't_310_jczq_kjjg'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("cc"),
            PyDB.StringField("ss"),
            PyDB.StringField("zdrq"),
            PyDB.StringField("bf1"),
            PyDB.StringField("kd"),
            PyDB.StringField("bc"),
            PyDB.StringField("rqspf"),
            PyDB.StringField("spf"),
            PyDB.StringField("bf2"),
            PyDB.StringField("jqzs"),
            PyDB.StringField("bqc"),
            PyDB.StringField("hgpk"),
            PyDB.StringField("sj"),
            PyDB.StringField("matchId", is_key=True),
            PyDB.DateField("timeInterval"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()

class ImportFootball_OPDictStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_310_OPDict'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("GameCompanyId"),
            PyDB.StringField("Company_OPID",is_key=True),
            PyDB.StringField("matchId",is_key=True),
            PyDB.StringField("Company_engName"),
            PyDB.StringField("Company_chnName"),
            PyDB.DateField("update_dt"),
        ])

    def save_or_update(self, item):
        # self.db.save_or_update(self.table_name, item)
        self.db.save(self.table_name, item)
        self.db.commit()


class ImportFootball_OPStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_310_OP'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("Company_OPID", is_key=True),
            PyDB.StringField("zs"),
            PyDB.StringField("h"),
            PyDB.StringField("ks"),
            PyDB.StringField("klzs1"),
            PyDB.StringField("klzs2"),
            PyDB.StringField("klzs3"),
            PyDB.StringField("bhsj", is_key=True),
            PyDB.StringField("matchId"),
            PyDB.DateField("update_dt"),
        ])

    def save_or_update(self, item):
        # self.db.save_or_update(self.table_name, item)
        self.db.save(self.table_name, item)
        self.db.commit()


class ImportFootball_YPDictStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 't_310_ypdict'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("bcgs"),
            PyDB.StringField("zd"),
            PyDB.StringField("pk"),
            PyDB.StringField("kd"),
            PyDB.StringField("zd2"),
            PyDB.StringField("pk2"),
            PyDB.StringField("kd2"),
            PyDB.StringField("bcgsId",is_key=True),
            PyDB.StringField("matchId",is_key=True),
            PyDB.DateField("update_dt"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportFootball_YPStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 't_310_yp'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("sj"),
            PyDB.StringField("bf"),
            PyDB.StringField("zd"),
            PyDB.StringField("pk"),
            PyDB.StringField("kd"),
            PyDB.StringField("bhsj",is_key=True),
            PyDB.StringField("status"),
            PyDB.StringField("bcgsId",is_key=True),
            PyDB.StringField("matchId",is_key=True),
            PyDB.DateField("update_dt"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportFootball_YPStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 't_310_yp'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("sj"),
            PyDB.StringField("bf"),
            PyDB.StringField("zd"),
            PyDB.StringField("pk"),
            PyDB.StringField("kd"),
            PyDB.StringField("bhsj",is_key=True),
            PyDB.StringField("status"),
            PyDB.StringField("bcgsId",is_key=True),
            PyDB.StringField("matchId",is_key=True),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportFootball_Select5from11Storage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 't_310_select5from11'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("IssueNum",is_key=True),
            PyDB.StringField("Result"),
            PyDB.DateField("AwardTime"),
            PyDB.DateField("datadate"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportFootball_SportloseMatchId(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_SPORTTERY_LOSEMATCHID'
        self.db.set_metadata(self.table_name, [
            PyDB.IntField("matchid"),
            PyDB.StringField("spidername"),
            PyDB.StringField("tablename"),
            PyDB.StringField("url",is_key=True),
            PyDB.StringField("losereason"),
        ])

    def save_or_update(self, item):
        self.db.save(self.table_name, item)
        self.db.commit()