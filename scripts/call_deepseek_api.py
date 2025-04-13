import pandas as pd
import chardet
from openai import OpenAI

# 1. 设置DeepSeek API的客户端
client = OpenAI(api_key="-----------", base_url="https://api.deepseek.com")

# 2. 定义生成函数
def generate_output(id, probable_cause):
    prompt = f"""
       You are an expert in maritime safety analysis, specifically in the area of human factors contributing to maritime accidents. You will be provided with an ID and a corresponding Probable Cause text from NTSB maritime accident reports. Your task is to identify the most important human factor based on the HFACS framework and output both the major category abbreviation and the subclass abbreviation of the most relevant human factor.

        The HFACS framework, widely used in safety and accident investigation, consists of the following major categories and subclasses:
        1.Organizational Influences(OI)
        Organizational Climate (OC): Prevailing atmosphere/vision within the organization including such things as policies, command structure, and culture. 
        Operational Process (OP): Formal process by which the vision of an organization is carried out including operations, procedures, and oversight among others. 
        Resource Management (RM): This category describes how human, monetary, and equipment resources necessary to carry out the vision are managed.
        2.Unsafe Supervision(US)
        Inadequate Supervision (IS): Oversight and management of personnel and resources including training, professional guidance, and operational leadership among other aspects. 
        Planned Inappropriate Operations (PIO): Management and assignment of work including aspects of risk management, crew pairing, operational tempo, etc. 
        Failed to Correct Known Problems (FCP): Those instances when deficiencies among individuals, equipment, training, or other related safety areas are “known” to the supervisor, yet are allowed to continue uncorrected. 
        Supervisory Violations (SV): The willful disregard for existing rules, regulations, instructions, or standard operating procedures by management during the course of their duties.
        3.Preconditions for Unsafe Acts(PUA)
        Environmental Factors
        Technological Environment (TE): This category encompasses a variety of issues including the design of equipment and controls, display/interface characteristics, checklist layouts, task factors and automation.
        Physical Environment (PhyE): The category includes both the operational setting (e.g., weather, altitude, terrain) and the ambient environment, such as heat, vibration, lighting, toxins, etc. 
        Condition of the Operator
        Adverse Mental States (AMS): Acute psychological and/or mental conditions that negatively affect performance such as mental fatigue, pernicious attitudes, and misplaced motivation. 
        Adverse Physiological States (APS): Acute medical and/or physiological conditions that preclude safe operations such as illness, intoxication, and the myriad of pharmacological and medical abnormalities known to affect performance. 
        Physical/Mental Limitations (PML): Permanent physical/mental disabilities that may adversely impact performance such as poor vision, lack of physical strength, mental aptitude, general knowledge, and a variety of other chronic mental illnesses. 
        Personnel Factors Communication, Coordination, & Planning (CC): Includes a variety of communication, coordination, and teamwork issues that impact performance. 
        Fitness for Duty (PR): Off-duty activities required to perform optimally on the job such as adhering to crew rest requirements, alcohol restrictions, and other off-duty mandates.
        4.Unsafe Acts(UA)
        Errors
        Decision Errors (DE): These “thinking” errors represent conscious, goal-intended behavior that proceeds as designed, yet the plan proves inadequate or inappropriate for the situation. These errors typically manifest as poorly executed procedures, improper choices, or simply the misinterpretation and/or misuse of relevant information. 
        Skill-based Errors (SBE): Highly practiced behavior that occurs with little or no conscious thought. These “doing” errors frequently appear as breakdown in visual scan patterns, inadvertent activation/deactivation of switches, forgotten intentions, and omitted items in checklists often appear. Even the manner or technique with which one performs a task is included. 
        Perceptual Errors (PE): These errors arise when sensory input is degraded as is often the case when flying at night, in poor weather, or in otherwise visually impoverished environments. Faced with acting on imperfect or incomplete information, aircrew run the risk of misjudging distances, altitude, and decent rates, as well as responding incorrectly to a variety of visual/vestibular illusions. 
        Violations
        Routine Violations (RV): Often referred to as “bending the rules” this type of violation tends to be habitual by nature and is often enabled by a system of supervision and management that tolerates such departures from the rules. 
        Exceptional Violations (EV): Isolated departures from authority, neither typical of the individual nor condoned by management.

        Task:
        Input:
        ID: {id}
        Probable Cause: {probable_cause}
        ###Your output should be:
        Major Category Abbreviation: [Output Major Category Abbreviation]
        Subclass Abbreviation: [Output Subclass Abbreviation]
    """
    
    # 3. 调用API生成输出
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are a helpful assistant"},
                  {"role": "user", "content": prompt}],
        stream=False
    )

    # 4. 返回生成的结果
    output = response.choices[0].message.content
    return output

# 5. 自动识别并转换文件编码为UTF-8
def convert_to_utf8(input_file_path):
    # 检测文件的编码格式
    with open(input_file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        file_encoding = result['encoding']
    
    # 如果文件编码不是UTF-8，则转换为UTF-8
    if file_encoding.lower() != 'utf-8':
        print(f"检测到文件编码为 {file_encoding}，正在转换为UTF-8...")
        with open(input_file_path, 'r', encoding=file_encoding) as file:
            content = file.read()
        
        # 将内容写入一个新文件并转换为UTF-8编码
        utf8_file_path = input_file_path.replace('.csv', '_utf8.csv')
        with open(utf8_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return utf8_file_path
    return input_file_path

# 6. 读取CSV文件并确保编码为UTF-8
input_csv_path = "input.csv"  # 输入CSV文件路径
input_csv_path_utf8 = convert_to_utf8(input_csv_path)
df = pd.read_csv(input_csv_path_utf8)

# 7. 处理每一行数据，生成分类结果
results = []
for index, row in df.iterrows():
    # 调用API生成分类结果
    generated_text = generate_output(row['ID'], row['Probable_cause'])
    
    # 提取Major Category Abbreviation和Subclass Abbreviation
    try:
        major_category = generated_text.split("Major Category Abbreviation:")[1].split("\n")[0].strip()
        subclass_abbreviation = generated_text.split("Subclass Abbreviation:")[1].split("\n")[0].strip()
    except IndexError:
        major_category, subclass_abbreviation = "Unknown", "Unknown"
    
    # 将结果保存到列表中
    results.append({
        "ID": row["ID"],
        "Major Category Abbreviation": major_category,
        "Subclass Abbreviation": subclass_abbreviation
    })

# 8. 保存结果到新的CSV文件
output_df = pd.DataFrame(results)
output_csv_path = "output.csv"  # 输出的CSV文件路径
output_df.to_csv(output_csv_path, index=False)

print(f"结果已保存到 {output_csv_path}")
