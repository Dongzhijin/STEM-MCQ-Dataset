import json

def evaluate_model(dataset_path, model):
    """
    评估模型在数据集上的表现。

    :param dataset_path: 数据集路径
    :param model: 使用的模型
    """
    with open(dataset_path, 'r') as f:
        data = json.load(f)

    correct = 0
    total = len(data)

    for item in data:
        # 模拟模型预测
        prediction = model.predict(item['question'])
        if prediction == item['correct_answer']:
            correct += 1

    accuracy = correct / total
    print(f"模型准确率: {accuracy:.2%}")

if __name__ == "__main__":
    class MockModel:
        def predict(self, question):
            return "A"  # 模拟预测

    # 示例调用
    evaluate_model(
        dataset_path="../datasets/cleaned/cleaned_dataset.json",
        model=MockModel()
    )
