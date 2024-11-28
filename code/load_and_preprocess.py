import pandas as pd
from datetime import datetime
import os

def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)
    
    # 确保 'create_date' 和 'update_date' 列被转换为 datetime 类型
    df['create_date'] = pd.to_datetime(df['create_date'], errors='coerce')
    df['update_date'] = pd.to_datetime(df['update_date'], errors='coerce')  # 处理转换错误，非法日期会变为 NaT
    
    # 填充缺失值
    df.fillna({'client_fio_full': '', 'contact_email': '', 'contact_phone': '', 'client_bday': '', 'source_cd': '', 'update_date': pd.NaT}, inplace=True)
    
    # 删除重复行
    df.drop_duplicates(inplace=True)

    # 过滤掉 'client_fio_full' 列中包含数字或为空的行
    df_filtered = df[
        ~df['client_fio_full'].str.contains(r'\d', na=False, regex=True) &
        df['client_fio_full'].str.strip().astype(bool)
    ]
    
    # 筛选高可信度的数据
    trusted_sources = ['Bank', 'Gov']
    df_filtered = df_filtered[df_filtered['source_cd'].isin(trusted_sources)]
    print(f"过滤 source_cd 后数据行数: {df_filtered.shape[0]}")

    # 删除不合法的生日记录
    df_filtered = df_filtered[df_filtered['client_bday'].str.contains(r'-', na=False)]
    df_filtered['client_bday'] = pd.to_datetime(df_filtered['client_bday'], errors='coerce')
    df_filtered = df_filtered[df_filtered['client_bday'].dt.year <= 2024]
    df_filtered = df_filtered[df_filtered['client_bday'].dt.year.astype(str).str[:2].isin(['19', '20'])]

    return df_filtered  # 返回经过预处理后的 DataFrame
