import evaluate
from model.translator import get_translation_from_list

def load_phomt(split):
    en_lst = []
    vi_lst = []

    with open(f'data/phomt/{split}.en', encoding="utf8") as file:
      for line in file:
          line = line.strip()
          en_lst.append(line)

    with open(f'data/phomt/{split}.vi', encoding="utf8") as file:
        for line in file:
            line = line.strip()
            vi_lst.append(line)

    return list(zip(en_lst, vi_lst))
def eval():
    dataset = load_phomt('test')
    texts = []
    labels = []
    for row in dataset:
        texts.append(row[0])
        labels.append(row[1])

    answers, costs = get_translation_from_list('Vietnamese', texts)
    bleu = evaluate.load("bleu")
    print(costs)
    bleu_results = bleu.compute(predictions=answers, references=[label for label in labels[:len(answers)]])
    print(bleu_results)

if __name__ == "__main__":
    eval()
    


