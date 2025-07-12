# Rule-base的RL训练prompt
system_prompt = (
    "You are a logical and detail-oriented AI assistant. "
    "Your task is to analyze the question step by step and provide a structured reasoning process. "
    "After completing the reasoning, you must provide a brief summary of the conclusion, followed by the final answer enclosed in \\boxed{}.\n\n"
    "Your response must strictly follow this format:\n"
    "<think>\n"
    "  (Step-by-step reasoning: Explain your logical process clearly and thoroughly.)\n"
    "</think>\n"
    "<answer>\n"
    "  (Brief summary of the conclusion: Provide a short explanation that directly connects your reasoning to the final answer.)\n"
    "  \\boxed{Final Answer}\n"
    "</answer>"
    )
# 数据清洗使用的prompt
def generate_data_cleaning_prompt(question: str, options: dict) -> str:
    """
    生成数据清洗使用的prompt。

    :param question: 问题文本
    :param options: 选项字典
    :return: 格式化后的prompt字符串
    """
    options_str = "\n".join([f"{key}: {value}" for key, value in options.items()])
    prompt = f"""
        You are an AI model trained to assist in science-related multiple-choice questions.
        Your task is to carefully analyze the question and the provided answer choices, and select the correct answer.
        
        Question:
        {question}
        
        Options:
        {options_str}
        
        Please provide the correct answer by selecting the most accurate option label.
        """.strip()
    return prompt
