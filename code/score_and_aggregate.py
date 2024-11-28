import pandas as pd
from datetime import datetime
import os

# 动态设置工作目录为脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from scoring import score_record  # 从 scoring.py 引用打分函数
from load_and_preprocess import load_and_preprocess

def fill_missing_data(group):
    """
    填充每个分组的缺失数据，选择 score 最高的行作为基准。
    """
    if 'score' not in group.columns:
        print(f"Warning: 'score' column is missing in group with client_fio_full: {group['client_fio_full'].iloc[0]}")
        return pd.DataFrame()  # 返回空的 DataFrame

    base_row = group.loc[group['score'].idxmax()].copy()  # 在分组中选择 score 最高的行，并创建其副本作为基准行。
    for column in group.columns:
        if pd.isna(base_row[column]):
            non_null_value = group.loc[group[column].notna(), column].iloc[0] if not group[column].isna().all() else None
            base_row[column] = non_null_value  # 将非空值填充到基准行中。

    # 重新计算填充后的基准行的 score
    base_row['score'] = score_record(base_row)  # 根据新的填充数据更新 score
    return base_row

def extract_golden_records(df):
    """
    提取每个ID组的“黄金记录”，并按照score降序排列。
    """
    df['score'] = df.apply(score_record, axis=1)  # 为 df 添加 'score' 列

    # 确保 'score' 列已经成功生成
    if 'score' not in df.columns:
        raise ValueError("Error: 'score' column was not successfully generated.")

    grouped = df.groupby('client_fio_full')  # 按 client_fio_full 分组
    final_rows = [fill_missing_data(group) for _, group in grouped if not group.empty]  # 确保分组不为空
    final_df = pd.DataFrame(final_rows)

    # 在聚合完成后，重新计算 score 列
    final_df['score'] = final_df.apply(score_record, axis=1)  # 更新 score 列

    # 只保留 score 大于 55 的行
    final_df = final_df[final_df['score'] > 55]

    return final_df

def save_to_csv(df, output_path):
    """
    将处理后的数据保存到 CSV 文件，同时检查并创建输出目录。
    """
    # 检查并创建输出文件夹
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 保存数据到 CSV 文件
    df.to_csv(output_path, index=False, date_format='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    input_file = os.path.join("..", "data", "input.csv")
    output_file = os.path.join("..", "data", "output", "score_and_aggregate.csv")
    
    # 加载和预处理数据
    df = load_and_preprocess(input_file)
    
    # 提取黄金记录并更新 score
    final_records = extract_golden_records(df)
    
    # 保存处理后的数据
    save_to_csv(final_records, output_file)
    print("数据已处理并保存到输出文件。")
