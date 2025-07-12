def generate_mcq_prompt(question: str, answer: str) -> dict:
    """
    将开放式问题转换为选择题。

    :param question: 原始问题
    :param answer: 正确答案
    :return: 生成的选择题
    """
    return {
        "question": f"{question}",
        "options": {
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D",
            "E": "Option E"  # 可选额外选项
        },
        "correct_answer": "A"  # 正确选项
    }

if __name__ == "__main__":
    # 示例调用
    question = "What is the capital of France?"
    answer = "Paris"
    mcq = generate_mcq_prompt(question, answer)
    print(mcq)
