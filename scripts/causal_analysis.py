import pandas as pd
import dowhy
from dowhy import CausalModel
import itertools
import numpy as np
from scipy.stats import norm
import os   

# 读取CSV文件
file_path = "input.csv"  # 替换为你的CSV文件路径
df = pd.read_csv(file_path)

# 选择 HFACS-S 和事故类型变量
hfacs_cols = [col for col in df.columns if col.startswith("HFACS-S_")]
accident_cols = [col for col in df.columns if col.startswith("Accident type_")]

# 选择可能的环境因素（排除事故类别和HFACS-S）
potential_factors = [col for col in df.columns if col not in hfacs_cols + accident_cols]

# 结果存储
results = []
save_interval = 500  # 每500条数据保存一次
output_file = "D://paper//all_causal_results.csv"

# 如果文件不存在，创建文件并写入表头
if not os.path.exists(output_file):
    pd.DataFrame(columns=["事故类别", "HFACS-S", "属性组合", "因果效应", "p值（Stouffer 组合）"]).to_csv(output_file, index=False)

# 遍历所有事故类型
for accident_type in accident_cols:
    
    # 遍历所有 HFACS-S 变量
    for hfacs_s in hfacs_cols:

        # 遍历最多3个其他因素的组合
        for num_factors in range(1, 4):  # 1, 2, 3 个组合
            for factor_combination in itertools.combinations(potential_factors, num_factors):

                # 设定自变量（HFACS-S + 其他因素）
                treatment_vars = [hfacs_s] + list(factor_combination)
                
                # 只保留相关数据
                df_filtered = df[treatment_vars + [accident_type]].dropna()
                
                if df_filtered.empty:
                    continue  # 跳过空数据集

                # **不使用 Graphviz，直接建立 DoWhy 模型**
                model = CausalModel(
                    data=df_filtered,
                    treatment=treatment_vars,
                    outcome=accident_type
                )

                # 识别因果关系
                identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)

                # 估计因果效应 (回归)
                try:
                    estimate = model.estimate_effect(identified_estimand,
                                                     method_name="backdoor.linear_regression")
                except Exception:
                    estimate = None  # 失败时跳过
                
                # 计算 P 值（Stouffer 组合）
                try:
                    p_values = [norm.cdf(abs(estimate.value)) if estimate else np.nan for var in treatment_vars]
                    combined_p_stouffer = norm.sf(sum(norm.ppf(p) for p in p_values) / np.sqrt(len(p_values)))
                except:
                    combined_p_stouffer = np.nan

                # 记录结果
                results.append({
                    "事故类别": accident_type.replace("Accident type_", ""),
                    "HFACS-S": hfacs_s.replace("HFACS-S_", ""),
                    "属性组合": ", ".join(treatment_vars),
                    "因果效应": estimate.value if estimate else np.nan,
                    "p值（Stouffer 组合）": combined_p_stouffer
                })

                # **每500条数据累计保存一次**
                if len(results) >= save_interval:
                    df_results = pd.DataFrame(results)
                    df_results.to_csv(output_file, mode="a", header=False, index=False)  # 追加模式
                    print(f"Saved {len(results)} new entries to {output_file}.")
                    results = []  # 清空缓存

# **保存剩余数据**
if results:
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_file, mode="a", header=False, index=False)
    print(f"Final save: {len(results)} entries to {output_file}.")
