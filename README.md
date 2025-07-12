# 🧠 项目名称

## 构建与清洗高质量 STEM 多选题数据集以提升大模型的科学推理能力

---

## 🎯 项目目标

- 构建一个**覆盖中高难度、多样化题型**的 STEM 多选题数据集；
- 清洗现有开源数据（多为 noisy/open-answer）并转换为**结构化、多选、rule-based**的数据；
- 利用 **Qwen 系列模型（7B-32B）** 进行 Zero-RL 训练，提升模型科学推理能力与反思能力。

---

## 📦 数据来源与处理

### 原始数据来源

| **数据集名** | **简介** | **数量** | **处理方式** | **链接** |
| --- | --- | --- | --- | --- |
| ScienceQA | 多模态/多学科，选取10k无图题 | 10k | 原始多选 | [ScienceQA](https://huggingface.co/datasets/derek-thomas/ScienceQA) |
| OpenBookQA | 小样本，含常识推理 | 6k | 多选保留 | [OpenBookQA](https://huggingface.co/datasets/allenai/openbookqa) |
| AGIEval | 多任务评估集 | 6k | 精选高质量题目 | [AGIEval](https://huggingface.co/datasets/PrimeIntellect/SYNTHETIC-1?row=0) |
| SCP-116K | 高教领域 open-answer | 116k | 转换为MCQ | [SCP-116K](https://arxiv.org/pdf/2501.15587) |
| SYNTHETIC-1 | stackoverflow衍生 STEM 题 | 313k | 选用10w构造MCQ | [SYNTHETIC-1](https://huggingface.co/datasets/PrimeIntellect/SYNTHETIC-1?row=0) |
| Sangeetha/kaggle | 初中科学题，5选1 | 200 | 原始多选 | [Kaggle-LLM-Science-Exam](https://huggingface.co/datasets/Sangeetha/Kaggle-LLM-Science-Exam?row=85) |
| AI2 ARC / TMMLU+ | 小学题 / 弃用 | - | 弃用/低质量 | [AI2 ARC](https://huggingface.co/datasets/allenai/ai2_arc?row=53) |

### 数据转换与清洗流程

- 对原始 open-answer 数据使用 prompt 构造 **高质量多选题**（见 generate_mcq_prompt 函数）；具体是使用Qwen2.5-72b-instruct进行构建。

```python
# 简答题改为选择题的prompt
def generate_mcq_prompt(question: str, answer: str) -> dict:
    return  f"""
You are an expert at creating multiple-choice questions. Your task is to convert the given question and answer into a well-structured multiple-choice question.

**Instructions:**
- Rewrite the given question into a multiple-choice format.
- Ensure the question requires **genuine reasoning** rather than simple recall or memorization.
- Do **not reduce the original difficulty** of the question.
- Provide at least **four answer options, but more are allowed if needed**.
- Ensure **only one correct answer** is present.
- Make the incorrect options plausible but clearly incorrect.
- Return the question and options in with the correct answer explicitly marked.

**Input:**
Question: "{question}"
Answer: "{answer}"

**Output Format:**
{
    "question": "Your rewritten multiple-choice question that requires reasoning",
    "options": {
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D",
        "E": "Option E",  # Optional extra options
        "F": "Option F"   # Optional extra options
    },
    "correct_answer": "A"  # The correct option letter
}

Now, generate the multiple-choice question while ensuring it requires reasoning.
        """.strip()

# generate_mcq_prompt(data_json[102220]['prompt'],data_json[102220]['gold_standard_solution'])
```

- **双阶段评估清洗**：
  1. 基于 qwen-7b-instruct，sample 16 次 response。
  2. 只保留 1 > responses_accuracy > 0.3 的数据集。# 过滤过于简单或者标签错误的数据
  3. 对 responses_accuracy <= 0.3 的题目，使用 qwen-QWQ-32b sample 16 次。
  4. 保留 responses_accuracy_qwq > 0.3 的数据集。#过滤过于难的数据

- 构建最终数据集：
  - 初始构造20k → 清洗后保留5k；
  - 添加 AGIEval 构成 11k；
  - 使用 SYNTHETIC-1 与 SCP 构造 74k 高质量 MCQ；
  - 最终规模 ≈ **85k 高质量 STEM 多选题**

---

## ⚙️ 模型训练与评估

### 实验设置

- 模型：Qwen2.5-7b-math-base,
- 评价指标：GPQA-diamond （研究生级别的STEM题目）
- 训练框架：字节开源的verl
- 训练策略：
  - RL：rule-based reward（如准确率提升、复读惩罚）；RL方法采用的是GRPO
  - SuperGPQA：尝试训练研究生级10选1题，但效果受限于模型能力。

### 训练挑战与修正

- **问题1：复读现象严重** → 引入 5-gram 重复率惩罚；
- **问题2：VERL框架** verl默认提取第一个box的答案 → 改为提取最后一个 box；
- **问题3：高难题训练不收敛** → 分层训练、逐步加入难题；

---

## 📊 实验结果概述

| **实验阶段** | **数据集规模** | **特征** | **评估指标** | **现象** |
| --- | --- | --- | --- | --- |
| 初始20k | ScienceQA 等 | 多选+反思 | 准确率偏高（易题） | 无挑战性 |
| 清洗后5k | 简中题+逻辑题 | 高质量 | 提升模型泛化 | √ |
| 加入 AGIEval → 11k | 增加难度 | 多任务表现提升 | √ |  |
| SYNTHETIC+SCP构造MCQ → 74k | 开放式转多选 | 可控难度 | 出现反思能力 | √ |
| 加入复读惩罚机制 | 训练稳定性增强 | n-gram≤0.4 | 模型崩塌减少，训练更加稳定 | √ |
| superGPQA（10选1） | 26k | 太难 | 准确率下降 | ✖️ |

---

## ✅ 项目亮点总结

- 设计了高效的数据清洗机制；
- 构建了 **具有难度分布和领域覆盖的STEM多选题集**；
- 实验中揭示了 **复读机惩罚机制 的加入能够有效稳定训练和提升训练效果**
- 成功验证了：**数据质量+结构优化>数据量堆砌**。

---

## 📂 项目代码结构

### 根目录

- **README.md**：项目说明文件，包含项目目标、数据来源、处理流程和实验结果。

- **LICENSE**：开源协议文件，定义项目的使用权限。

### scripts 文件夹

- **prompt_template.py**：包含生成多选题的模板和相关逻辑。

- **generate_mcq.py**：实现将开放式问题转换为结构化多选题的功能。

- **repetition_penalty.py**：实现复读机惩罚机制，通过 n-gram 重复率计算减少重复答案现象。

