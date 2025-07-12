import json

def clean_dataset(dataset_path, output_path, model, accuracy_threshold=0.3):
    """
    清洗数据集，过滤掉过于简单或噪声数据。

    :param dataset_path: 原始数据集路径
    :param output_path: 清洗后数据集保存路径
    :param model: 使用的模型（如 qwen-7b-instruct 或 qwen-QWQ-32b）
    :param accuracy_threshold: 准确率阈值
    """
    with open(dataset_path, 'r') as f:
        data = json.load(f)

    cleaned_data = []

    for item in data:
        responses_accuracy = item.get('responses_accuracy', 0)
        if 1 > responses_accuracy > accuracy_threshold:
            cleaned_data.append(item)
        elif responses_accuracy <= accuracy_threshold:
            # 使用更强模型重新采样
            responses_accuracy_qwq = item.get('responses_accuracy_qwq', 0)
            if responses_accuracy_qwq > accuracy_threshold:
                cleaned_data.append(item)

    with open(output_path, 'w') as f:
        json.dump(cleaned_data, f, indent=4)

    print(f"清洗完成，共保留 {len(cleaned_data)} 条数据。")

if __name__ == "__main__":
    # 示例调用
    clean_dataset(
        dataset_path="../datasets/raw/dataset.json",
        output_path="../datasets/cleaned/cleaned_dataset.json",
        model="qwen-7b-instruct"
    )
