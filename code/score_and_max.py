import pandas as pd
from datetime import datetime
import os

# 动态设置工作目录为脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from scoring import score_record  # 从 scoring.py 引用打分函数
from load_and_preprocess import load_and_preprocess

def extract_golden_records(df):
    """
    提取每个ID组的“黄金记录”，并按照score降序排列。
    """
    # 为数据打分
    df['score'] = df.apply(score_record, axis=1)

    # 删除 score 低于 55 的行
    df_filtered = df[df['score'] >= 55]

    # 按 'client_fio_full' 分组，并选择每组中 score 最大的记录
    df_sorted = df_filtered.loc[df_filtered.groupby('client_fio_full')['score'].idxmax()]

    # 按 'client_fio_full' 分组后，按 'score' 降序排列
    df_sorted = df_sorted.sort_values(by=['client_fio_full', 'score'], ascending=[True, False])

    # 返回最终的数据
    return df_sorted

def save_to_csv(df, output_path):
    """
    将排序后的数据保存到CSV文件。
    """
    # 检查并创建输出文件夹
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 保存数据到 CSV 文件
    df.to_csv(output_path, index=False, date_format='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    # 定义相对路径
    input_file = os.path.join("..", "data", "input.csv")
    output_file = os.path.join("..", "data", "output", "score_and_max.csv")

    # 1. 加载并预处理数据
    df = load_and_preprocess(input_file)

    # 2. 提取并排序记录（保留每个 client_fio_full 组内 score 最高的记录）
    sorted_records = extract_golden_records(df)

    # 3. 保存结果
    save_to_csv(sorted_records, output_file)
    print("数据已根据 client_fio_full 和 score 排序，并保存到输出文件。")
