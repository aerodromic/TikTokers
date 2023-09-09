import pandas as pd
import datetime

def clean_ads(ads: pd.DataFrame):
    ads['avg_ad_revenue'].isna().sum()
    ads['p_date_new'] = pd.to_datetime(ads['p_date'], format='%Y%m%d')

    ads.ad_revenue = ads['ad_revenue'].fillna(0)
    ads = ads.loc[ads['ad_revenue'] != 0] # remove ads that have 0 ad revenue

    # identify advertisers based on the average ad revenue they receive
    groups = ads.groupby('avg_ad_revenue')

    # where all the rows within a group is NaN
    all_na = groups['punish_num'].transform(lambda x: x.isna().all())

    # for fill global mode
    ads.loc[all_na, 'punish_num'] = ads['punish_num'].mode()[0]

    # fill with local mode
    mode_by_group = groups['punish_num'].transform(lambda x: x.mode()[0])
    ads['punish_num'] = ads['punish_num'].fillna(mode_by_group)
    ads['start_time'] = ads['start_time'].fillna(datetime.datetime(2000, 1, 1, 0))


    # Feature Engineering
    ads['days_since_last_penalty'] = (
        ads['p_date_new'] - ads['latest_punish_begin_date']).dt.days
    ads['days_since_start_time'] = (ads['p_date_new'] - ads['start_time']).dt.days
    ads['revenue_ratio'] = (ads['ad_revenue'] / (ads['avg_ad_revenue'])).fillna(0)

    ads = ads[ads['avg_ad_revenue'] != 0]

    return ads# [['ad_id', 'delivery_country', 'queue_market', 'baseline_st', 'punish_num', 'ad_revenue', 'avg_ad_revenue', 'revenue_ratio', 'days_since_last_penalty', 'days_since_start_time']]