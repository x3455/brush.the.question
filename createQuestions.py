import pandas as pd
import json
import os

error_log = []  # 添加这一行以创建 error_log 列表

def process_sheet(sheet, file_name, sheet_name):
    questions = []

    try:
        for i in range(len(sheet)):
            question_type = sheet.iloc[i, 0]
            question_text = sheet.iloc[i, 1]
            correct_answer = sheet.iloc[i, 10]

            if pd.isna(question_text):  # 如果题目为空值，记录到异常日志
                error_log.append(f"文件: {file_name}, Sheet: {sheet_name}, 行: {i + 1} - 题目为空值")
                continue

            if pd.isna(correct_answer):  # 如果答案为空值，记录到异常日志
                error_log.append(f"文件: {file_name}, Sheet: {sheet_name}, 行: {i + 1} - 答案为空值")
                continue

            if '单' in question_type:  # 如果类型中包含'单'，则是单选题
                options = [sheet.iloc[i, 3], sheet.iloc[i, 5], sheet.iloc[i, 7], sheet.iloc[i, 9]]
                options = [opt for opt in options if pd.notna(opt)]

                question = {
                    'question': question_text,
                    'type': 'singleChoice',
                    'options': options,
                    'correctAnswer': correct_answer
                }

            elif '多' in question_type:  # 如果类型中包含'多'，则是多选题
                options = [sheet.iloc[i, 3], sheet.iloc[i, 5], sheet.iloc[i, 7], sheet.iloc[i, 9]]
                options = [opt for opt in options if pd.notna(opt)]
                correct_answer = list(correct_answer)  # 将拼接的字符串转成列表

                question = {
                    'question': question_text,
                    'type': 'multiple',
                    'options': options,
                    'correctAnswer': correct_answer
                }

            else:  # 否则是判断题

                question = {
                    'question': question_text,
                    'type': 'trueFalse',
                    'correctAnswer': correct_answer
                }

            questions.append(question)

            # 打印处理结果
            print(f"处理结果 - 文件: {file_name}, Sheet: {sheet_name}, 行: {i + 1}, 题目: {question}")

    except Exception as e:
        print(f"在处理文件 {file_name} 的 sheet {sheet_name} 时发生异常：")
        print(f"行: {i + 1}, 错误信息: {e}")
        error_log.append(f"处理文件 {file_name} 的 sheet {sheet_name} 时发生异常：行 {i + 1} - {e}")

    return questions


# 然后，遍历所有的 Excel 文件和 sheet
base_dir = 'F:\\分享\\test\\excel'
json_data = []

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.xlsx'):
            file_path = os.path.join(root, file)

            xls = pd.ExcelFile(file_path)

            for sheet_name in xls.sheet_names:
                sheet = xls.parse(sheet_name, header=None)
                sheet_data = process_sheet(sheet, file, sheet_name)
                json_data.extend(sheet_data)

output_file = 'F:\\分享\\test\\excel\\output.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False)

# 在处理完所有文件后，保存处理失败信息到日志文件
error_log_file = 'F:\\分享\\test\\excel\\error_log.txt'
with open(error_log_file, 'w', encoding='utf-8') as log_file:
    for error_msg in error_log:
        log_file.write(error_msg + '\n')

print(f'处理失败信息已保存到 {error_log_file}')
print(f'JSON 数据已保存到 {output_file}')
