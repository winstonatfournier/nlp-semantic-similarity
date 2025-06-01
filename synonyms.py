import math
import re

def cosine_similarity(vec1, vec2):
    common_keys = []
    dot_product = 0
    for key in vec1:
        if key in vec2:
            common_keys.append(key)
    for key in common_keys:
        dot_product += vec1[key] * vec2[key]
    magnitude_vec1 = math.sqrt(sum(value**2 for value in vec1.values()))
    magnitude_vec2 = math.sqrt(sum(value**2 for value in vec2.values()))
    if magnitude_vec1 == 0 or magnitude_vec2 == 0:
        return 0.0
    similarity = dot_product / (magnitude_vec1 * magnitude_vec2)
    return similarity

def build_semantic_descriptors(sentences):
    semantic_descriptors = {}
    word_counts = {}
    for sentence in sentences:
        unique_words_in_sentence = set(sentence)
        for word in unique_words_in_sentence:
            word_counts[word] = word_counts.get(word, 0) + 1
            if word not in semantic_descriptors:
                semantic_descriptors[word] = {}
            for co_word in unique_words_in_sentence:
                if co_word != word:
                    semantic_descriptors[word][co_word] = semantic_descriptors[word].get(co_word, 0) + 1
    for word, co_words in semantic_descriptors.items():
        for co_word in co_words:
            semantic_descriptors[word][co_word] /= word_counts[word]
    return semantic_descriptors

def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for filename in filenames:
        with open(filename, "r", encoding="utf-8", errors="replace") as file:
            file_content = file.read()
            sentences.extend(re.split(r'[.!?]', file_content))
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    tokenized_sentences = [re.findall(r'\b\w+\b', sentence.lower()) for sentence in sentences]
    semantic_descriptors = build_semantic_descriptors(tokenized_sentences)
    return semantic_descriptors

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return None
    most_similar = None
    min_similarity = float('inf')
    for choice in choices:
        if word == choice:
            pass
        elif choice in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
            if similarity < min_similarity:
                most_similar = choice
                min_similarity = similarity
    return most_similar

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct_guesses = 0
    total_questions = 0
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            line = line.strip().split()
            if line:
                total_questions += 1
                word, correct_answer, choices = line[0], line[1], line[2:]
                guess = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
                if guess == correct_answer:
                    correct_guesses += 1
    percentage_correct = (correct_guesses / total_questions) * 100
    return percentage_correct
