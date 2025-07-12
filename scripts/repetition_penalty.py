from collections import Counter

def ngram_repetition_penalty(text, n=5, penalty_weight=1):
    """
    计算 n-gram 级别的重复惩罚
    :param text: 输入文本
    :param n: 计算 n-gram 重复率
    :param penalty_weight: 惩罚系数
    :return: 计算出的重复惩罚值（负值表示惩罚）
    """
    words = text.split()
    if len(words) < n:
        return 0  # 过短的文本不惩罚

    ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
    ngram_counts = Counter(ngrams)
    repeat_rate = sum(c-1 for c in ngram_counts.values() if c > 1) / len(ngrams)

    if repeat_rate < 0.4:
        return 0

    return -penalty_weight * repeat_rate  # 负值表示惩罚
