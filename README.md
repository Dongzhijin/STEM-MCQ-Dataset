# STEM Dataset

## 项目简介

STEM Dataset 是一个用于评估和训练神经模型的科学相关任务数据集集合。该项目旨在整理、清洗和分析多个公开数据集，以构建一个高质量的 STEM 数据集。

## 项目结构
```
STEM-dataset/
├── datasets/                # 存放原始数据集和清洗后的数据集
│   ├── raw/                 # 原始数据集
│   ├── cleaned/             # 清洗后的数据集
│   └── metadata/            # 数据集的元信息
├── scripts/                 # 数据处理和清洗脚本
│   ├── data_cleaning.py     # 数据清洗流程脚本
│   ├── generate_mcq.py      # MCQ生成脚本
│   └── evaluation.py        # 实验评估脚本
├── experiments/             # 实验结果和分析
│   ├── tensorboard_logs/    # TensorBoard日志
│   ├── results/             # 实验结果文件
│   └── analysis/            # 分析报告
├── models/                  # 模型相关文件
│   ├── qwen-7b/             # qwen-7b模型相关
│   ├── qwen-QWQ-32b/        # qwen-QWQ-32b模型相关
│   └── superGPQA/           # superGPQA模型相关
├── README.md                # 项目说明文件
├── LICENSE                  # 开源协议文件
└── .gitignore               # Git忽略文件
```

## 数据集来源

### 原始数据集
- CMMLU 中文11k: [链接](https://github.com/haonan-li/CMMLU/#%E6%8E%92%E8%A1%8C%E6%A6%9C)
- Measuring Vision-Language STEM Skills of Neural Models: [链接](https://huggingface.co/datasets/stemdataset/STEM)
- SCP-116K: [链接](https://arxiv.org/pdf/2501.15587)
- Kaggle-LLM-Science-Exam: [链接](https://huggingface.co/datasets/Sangeetha/Kaggle-LLM-Science-Exam?row=85)
- OpenBookQA: [链接](https://huggingface.co/datasets/allenai/openbookqa)
- AI2 ARC: [链接](https://huggingface.co/datasets/allenai/ai2_arc?row=53)
- ScienceQA: [链接](https://huggingface.co/datasets/derek-thomas/ScienceQA)
- TMMLU+: [链接](https://huggingface.co/datasets/ikala/tmmluplus?row=4)
- AGIEval: [链接](https://huggingface.co/datasets/PrimeIntellect/SYNTHETIC-1?row=0)
- PrimeIntellect/SYNTHETIC-1: [链接](https://huggingface.co/datasets/PrimeIntellect/SYNTHETIC-1?row=0)

### 数据清洗流程
1. 基于 qwen-7b-instruct，sample 16 次 response。
2. 只保留 1 > responses_accuracy > 0.3 的数据集。
3. 对 responses_accuracy <= 0.3 的题目，使用 qwen-QWQ-32b sample 16 次。
4. 保留 responses_accuracy_qwq > 0.3 的数据集。

## 实验结果

### 实验数据集
- 20k 数据集（ScienceQA、OpenBookQA 等）。
- 清洗后剩下 5k 数据。
- 添加 AGIEval 数据集 6k，累计数据 11k。
- 构造 STEM 数据集：增加难度、多样性。

### 实验分析
- 实验结果见 TensorBoard 日志。
- 复读机现象分析与解决方案。
- 添加 "复读机惩罚机制"，n-gram 计算重复比率，提升训练稳定性。

## 开源协议
MIT License
