
import json
import xlrd
from cassandra.cluster import Cluster


MAP = {
    'people': ['CPL_HHM_CHILD_HC', 'CPL_INDM_GEND_S', 'CPL_INDM_MARRC2', 'CPL_INDM_NATI', 'CPL_INDM_AGE_C5', 'CPL_HHM_CHILD_CHLI', 'CPL_INDM_UNDERG', 'CPL_INDM_EDU_LEVEL'],
    'device': ['CID_MODEL', 'CPL_DVM_BRAD', 'CPL_DVM_HF', 'CPL_DVM_ISP', 'CPL_DVM_OS', 'CPL_DVM_PUPR', 'CPL_DVM_RESO', 'CPL_DVM_SCSIZE', 'CPL_DVM_TIME', 'CPL_DVM_TYPE'],
    'normal': ['CPL_INDM_VEIC_VEID', 'FIM_FISM_CONL_CIR', 'FIM_FISM_INCL', 'GBM_BHM_PURB_CONP', 'GBM_BHM_PURB_PREF', 'SOM_OCM_CAREER', 'GBM_HBM_S'],
    'network': ['GBM_BHM_APPP_APPR_S', 'GBM_BHM_PURB_PURW', 'GBM_BHM_PURB_SUPR', 'GBM_BHM_REAB_REAP'],
    'travel': ['APP_HOBY_BUS', 'APP_HOBY_TICKET', 'APP_HOBY_TRAIN', 'APP_HOBY_FLIGHT', 'APP_HOBY_TAXI', 'APP_HOBY_SPECIAL_DRIVE', 'APP_HOBY_HIGH_BUS', 'APP_HOBY_OTHER_DRIVE', 'APP_HOBY_RENT_CAR', 'APP_HOBY_STARS_HOTEL', 'APP_HOBY_YOUNG_HOTEL', 'APP_HOBY_HOME_HOTEL', 'APP_HOBY_CONVERT_HOTEL'],
    'financial': ['APP_HOBY_BANK_UNIN', 'APP_HOBY_ALIPAY', 'APP_HOBY_THIRD_PAY', 'APP_HOBY_INTERNET_BANK', 'APP_HOBY_FOREIGN_BANK', 'APP_HOBY_MIDDLE_BANK', 'APP_HOBY_CREDIT_CARD', 'APP_HOBY_CITY_BANK', 'APP_HOBY_STATE_BANK', 'APP_HOBY_FUTURES', 'APP_HOBY_VIRTUAL_CURRENCY', 'APP_HOBY_FOREX', 'APP_HOBY_NOBLE_METAL', 'APP_HOBY_FUND', 'APP_HOBY_COLLECTION', 'APP_HOBY_STOCK', 'APP_HOBY_ZONGHELICAI', 'APP_HOBY_CAR_LOAN', 'APP_HOBY_DIVIDE_LOAN', 'APP_HOBY_STUDENT_LOAN', 'APP_HOBY_CREDIT_CARD_LOAN', 'APP_HOBY_CASH_LOAN', 'APP_HOBY_HOUSE_LOAN', 'APP_HOBY_P2P', 'APP_HOBY_LOAN_PLATFORM', 'APP_HOBY_SPORT_LOTTERY', 'APP_HOBY_WELFARE_LOTTERY', 'APP_HOBY_DOUBLE_BALL', 'APP_HOBY_LOTTERY', 'APP_HOBY_FOOTBALL_LOTTERY', 'APP_HOBY_MARK_SIX', 'APP_HOBY_WECHAT'],
    'live': ['APP_HOBY_SUMMARY_LIVE', 'APP_HOBY_SHORT_VIDEO', 'APP_HOBY_SOCIAL_LIVE', 'APP_HOBY_TRAVEL_LIVE', 'APP_HOBY_SUMMARY_VIDEO', 'APP_HOBY_SPORTS_VIDEO', 'APP_HOBY_GAME_LIVE', 'APP_HOBY_BEAUTY_LIVE', 'APP_HOBY_COS_LIVE', 'APP_HOBY_SELF_PHOTO', 'APP_HOBY_TV_LIVE', 'APP_HOBY_CULTURE_LIVE', 'APP_HOBY_SHOW_LIVE', 'APP_HOBY_EDU_LIVE', 'APP_HOBY_SPORTS_LIVE', 'APP_HOBY_STARS_LIVE'],
    'read': ['APP_HOBY_READ_LISTEN', 'APP_HOBY_SUNMMARY_NEWS', 'APP_HOBY_WOMEN_HEL_BOOK', 'APP_HOBY_ARMY_NEWS', 'APP_HOBY_CARTON_BOOK', 'APP_HOBY_PHY_NEWS', 'APP_HOBY_FAMOUSE_BOOK', 'APP_HOBY_FINCAL_NEWS', 'APP_HOBY_FINCAL_BOOK', 'APP_HOBY_FUN_NEWS', 'APP_HOBY_EDU_MED', 'APP_HOBY_KONGFU', 'APP_HOBY_TECH_NEWS', 'APP_HOBY_LOOK_FOR_MED', 'APP_HOBY_ENCOURAGE_BOOK', 'APP_HOBY_CAR_INFO_NEWS', 'APP_HOBY_HUMERIOUS'],
    'game': ['APP_HOBY_CARDS_GAME', 'APP_HOBY_SPEED_GAME', 'APP_HOBY_ROLE_GAME', 'APP_HOBY_NET_GAME', 'APP_HOBY_RELAX_GAME', 'APP_HOBY_KONGFU_GAME', 'APP_HOBY_GAME_VIDEO', 'APP_HOBY_TALE_GAME', 'APP_HOBY_DIAMONDS_GAME', 'APP_HOBY_TRAGEDY_GAME'],
    'life': ['APP_HOBY_OUTDOOR', 'APP_HOBY_MOVIE', 'APP_HOBY_CARTON', 'APP_HOBY_BEAUTIFUL', 'APP_HOBY_LOSE_WEIGHT', 'APP_HOBY_PHY_BOOK', 'APP_HOBY_FRESH_SHOPPING', 'APP_HOBY_WIFI', 'APP_HOBY_CAR_PRO', 'APP_HOBY_LIFE_PAY', 'APP_HOBY_PET_MARKET', 'APP_HOBY_OUT_FOOD', 'APP_HOBY_FOOD', 'APP_HOBY_PALM_MARKET', 'APP_HOBY_WOMEN_HEAL', 'APP_HOBY_RECORD', 'APP_HOBY_CONCEIVE', 'APP_HOBY_SHARE', 'APP_HOBY_COOK_BOOK', 'APP_HOBY_BUY_RENT_HOUSE', 'APP_HOBY_CHINESE_MEDICINE', 'APP_HOBY_JOB', 'APP_HOBY_HOME_SERVICE', 'APP_HOBY_KRAYOK', 'APP_HOBY_FAST_SEND'],
    'social': ['APP_HOBY_PEOPLE_RESOUSE', 'APP_HOBY_MAMA_SOCIAL', 'APP_HOBY_GAY_SOCIAL', 'APP_HOBY_HOT_SOCIAL', 'APP_HOBY_MARRY_SOCIAL', 'APP_HOBY_CAMPUS_SOCIAL', 'APP_HOBY_LOVERS_SOCIAL', 'APP_HOBY_ECY', 'APP_HOBY_STRANGER_SOCIAL', 'APP_HOBY_ANONYMOUS_SOCIAL', 'APP_HOBY_CITY_SOCIAL', 'APP_HOBY_FANS'],
    'education': ['APP_HOBY_FIN', 'APP_HOBY_MIDDLE', 'APP_HOBY_IT', 'APP_HOBY_PRIMARY', 'APP_HOBY_BABY', 'APP_HOBY_ONLINE_STUDY', 'APP_HOBY_FOREIGN', 'APP_HOBY_DRIVE', 'APP_HOBY_SERVANTS', 'APP_HOBY_CHILD_EDU', 'APP_HOBY_UNIVERSITY'],
    'shipping': ['APP_HOBY_CAR_SHOPPING', 'APP_HOBY_SECONDHAND_SHOPPING', 'APP_HOBY_ZONGHE_SHOPPING', 'APP_HOBY_PAYBACK', 'APP_HOBY_DISCOUNT_MARKET', 'APP_HOBY_BABY_SHOPPING', 'APP_HOBY_WOMEN_SHOPPING', 'APP_HOBY_REBATE_SHOPPING', 'APP_HOBY_GROUP_BUY', 'APP_HOBY_GLOBAL_SHOPPING', 'APP_HOBY_SHOPPING_GUIDE', 'APP_HOBY_SEX_SHOPPING'],
    'work': ['APP_HOBY_SMOTE_OFFICE'],
}



cluster = Cluster(['106.14.160.252'], 9042)

session = cluster.connect('jg')
# session.set_keyspace('jg')
# session.execute('USE jg')


# session.execute(open('create.cql').read())


book = xlrd.open_workbook('tags.xlsx')
sheet = book.sheets()[1]

columns = sheet.row_values(0)

print(columns)


for i in range(2, sheet.nrows - 1):
    values = sheet.row_values(i)
    imei = values[0]
    jid = values[1]

    print(values)

    if not imei or not jid:
        continue

    r = {}
    for j in range(2, len(columns)):
        column = columns[j]
        if not column:
            continue
        value = values[j].strip()
        if not value:
            continue

        # if column in ['CPL_INDM_EDU_LEVEL']:
        #     value = "%s" % value
        # elif column in ['CPL_HHM_CHILD_HC']:
        #     value = 'true' if value == '有' else 'false'
        # else:
        #     value = "'%s'" % value

        r[column] = value

    for family, sub_columns in MAP.items():

        # insert_columns = []
        # insert_values = []
        insert_data = {}
        for column in sub_columns:
            if column in r:
                # insert_columns.append(column)
                # insert_values.append(r[column])

                value = r[column]
                if column in ['CPL_INDM_EDU_LEVEL']:
                    value = int(value)
                elif column in ['CPL_HHM_CHILD_HC']:
                    value = True if value == '有' else False
                else:
                    value = "%s" % value
                insert_data[column] = value

        # if not insert_columns:
        #     continue

        # assert len(insert_columns) == len(insert_values)
        # cstr = ', '.join(insert_columns)
        # vstr = ', '.join(insert_values)

        # cql = "insert into jg.%s (CID_JID, %s) values ('%s', %s)" % (family, cstr, jid, vstr)

        if not insert_data:
            continue
        insert_data['CID_JID'] = jid
        insert_json = json.dumps(insert_data)

        cql = "insert into jg.%s json $$%s$$" % (family, insert_json)

        print(cql)
        session.execute(cql)


print('finish!')





