import json
from collections import defaultdict
import os


def load_final_vocab(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        vocab_data = json.load(f)
    return {entry["word"] for entry in vocab_data if "word" in entry}


def tokenize(sentence):
    return sentence.strip().split()


def build_word_matrix(corpus_path, final_vocab):
    transitions = defaultdict(lambda: defaultdict(int))

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            words = tokenize(line)
            for i in range(len(words) - 1):
                current, nxt = words[i], words[i + 1]
                if current in final_vocab and nxt in final_vocab:
                    transitions[current][nxt] += 1

    # Convertir les transitions en probabilités
    word_matrix = []
    for word, next_words in transitions.items():
        total = sum(next_words.values())
        transition_list = [
            {"word": to_word, "probability": round(count / total, 4)}
            for to_word, count in next_words.items()
        ]
        word_matrix.append({
            "word": word,
            "transitions": transition_list
        })

    return word_matrix


def save_word_matrix(matrix, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(matrix, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 🔁 Adapte les chemins selon ta structure de dossier
    base_dir = os.path.dirname(os.path.abspath(__file__))
    final_dict_path = os.path.join(base_dir, '..', '..', 'data', 'processed', 'finalDictionary.json')
    corpus_path = os.path.join(base_dir, '..', '..', 'data', 'processed', 'splittedCorpus.txt')
    output_path = os.path.join(base_dir, '..', '..', 'data', 'processed', 'word_matrix.json')

    final_vocab = load_final_vocab(final_dict_path)
    word_matrix = build_word_matrix(corpus_path, final_vocab)
    save_word_matrix(word_matrix, output_path)

    print(f"Matrice de transitions sauvegardée dans {output_path}")
