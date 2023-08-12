from model.translator import get_translation_from_text
import argparse
from iso639 import Lang

def infer(args):
    text = args.text
    dest_language = Lang(args.to).name
    print(dest_language)
    answer, cost = get_translation_from_text(dest_language, text)

    print(f"The translation is: {answer}")
    print(f"The cost is: ${cost}")


parser = argparse.ArgumentParser()
parser.add_argument('--text', default='', type=str)
parser.add_argument('--to', default='vi', type=str)
args = parser.parse_args()

infer(args)