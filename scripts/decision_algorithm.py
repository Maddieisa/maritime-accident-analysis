import pandas as pd

# 读取CSV文件
def read_and_rename(file_path, suffix):
    df = pd.read_csv(file_path)
    df.rename(columns={
        'Major Category Abbreviation': f'Major Category Abbreviation_{suffix}',
        'Subclass Abbreviation': f'Subclass Abbreviation_{suffix}'
    }, inplace=True)
    return df

# 文件路径
file1 = 'C://Users//ZhengQianqian//Desktop//HFACS_PRO//AC_results//2023_output_results.csv'
file2 = 'C://Users//ZhengQianqian//Desktop//HFACS_PRO//AC_results//2023_output_results1.csv'
file3 = 'C://Users//ZhengQianqian//Desktop//HFACS_PRO//AC_results//2023_output_results2.csv'

# 读取并重命名列
df1 = read_and_rename(file1, 1)
df2 = read_and_rename(file2, 2)
df3 = read_and_rename(file3, 3)

# 合并数据
merged_df = df1.merge(df2, on='ID').merge(df3, on='ID')

# 分类逻辑
result = []
xiaolei = []
dalei = []

for _, row in merged_df.iterrows():
    majors = [
        row['Major Category Abbreviation_1'],
        row['Major Category Abbreviation_2'],
        row['Major Category Abbreviation_3']
    ]
    subclasses = [
        row['Subclass Abbreviation_1'],
        row['Subclass Abbreviation_2'],
        row['Subclass Abbreviation_3']
    ]

    # Count occurrences of each major category
    major_counts = pd.Series(majors).value_counts()

    if major_counts.max() == 3:
        # All three major categories are the same
        major = major_counts.idxmax()
        subclass_counts = pd.Series(subclasses).value_counts()
        if subclass_counts.max() >= 2:
            subclass = subclass_counts.idxmax()
            result.append([row['ID'], major, subclass])
        else:
            xiaolei.append(row.tolist())
    elif major_counts.max() == 2:
        # Two major categories are the same
        major = major_counts.idxmax()
        indices = [i for i, x in enumerate(majors) if x == major]
        relevant_subclasses = [subclasses[i] for i in indices]
        subclass_counts = pd.Series(relevant_subclasses).value_counts()
        if subclass_counts.max() == 1:
            xiaolei.append(row.tolist())
        else:
            subclass = subclass_counts.idxmax()
            result.append([row['ID'], major, subclass])
    else:
        # All three major categories are different
        dalei.append(row.tolist())

# 保存结果
result_df = pd.DataFrame(result, columns=['ID', 'Major Category', 'Subclass'])
xiaolei_df = pd.DataFrame(xiaolei, columns=merged_df.columns)
dalei_df = pd.DataFrame(dalei, columns=merged_df.columns)

result_df.to_csv('result.csv', index=False)
xiaolei_df.to_csv('spe_dif.csv', index=False)
dalei_df.to_csv('pri_dif.csv', index=False)

print("处理完成，结果已保存到 result.csv, xiaolei.csv 和 dalei.csv 文件中。")
