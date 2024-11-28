# scoring.py
from datetime import datetime
import pandas as pd

def score_record(row):
    """
    根据完整性、相关性、时效性为单条记录打分。
    """
    completeness_score = row.notna().sum()  # 非空字段数
    key_fields_weight = (
            (5 if row['client_fio_full'] else 0) +
            (3 if row['contact_email'] else 0) +
            (3 if row['contact_phone'] else 0) +
            (2 if row['client_bday'] else 0)
    )

    source_weight = 5 if row['source_cd'] in ['Bank', 'Gov'] else 2

    # 时效性分数计算
    if pd.notnull(row['update_date']):
        update_date = row['update_date']
        days_diff = (datetime.now() - update_date).days
        if days_diff <= 1:
            recency_score = 5
        elif 1 < days_diff <= 7:
            recency_score = 4
        elif 7 < days_diff <= 30:
            recency_score = 3
        elif 30 < days_diff <= 90:
            recency_score = 2
        else:
            recency_score = 1
    else:
        recency_score = 0

    # 计算总分
    total_score = completeness_score + key_fields_weight + source_weight + recency_score
    return total_score
