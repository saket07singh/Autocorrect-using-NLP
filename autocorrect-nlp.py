#!/usr/bin/env python
# coding: utf-8

# In[8]:




import re
from collections import Counter

class SpellChecker:
    
    def __init__(self, file_path='book.txt'):
        self.words = self.process_text(file_path)
        self.vocab = set(self.words)
        self.word_count_dict = self.get_count()
        self.prob_of_occurr = self.occurr_prob()
    def process_text(self, path):
     words = []
     with open(path, encoding='utf-8') as f:
        file_name_data = f.read()
     file_name_data = file_name_data.lower()
     words = re.findall(r'\w+', file_name_data)
     return words
    

    def get_count(self):
        return Counter(self.words)

    def occurr_prob(self):
        probs = {}
        m = sum(self.word_count_dict.values())
        for key in self.word_count_dict:
            probs[key] = self.word_count_dict[key] / m
        return probs

    def del_letter(self, word):
        del_letter = []
        split_letter = []

        for i in range(len(word)):
            split_letter.append([word[:i], word[i:]])
        for a, b in split_letter:
            del_letter.append(a + b[1:])

        return del_letter

    def switch_letter(self, word):
        sw_letter = []
        split_letter = []

        for c in range(len(word)):
            split_letter.append([word[:c], word[c:]])
        sw_letter = [a + b[1] + b[0] + b[2:] for a, b in split_letter if len(b) >= 2]

        return sw_letter

    def replace_letter(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        repl_let = []
        split_let = []

        for c in range(len(word)):
            split_let.append([word[:c], word[c:]])
        repl_let = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_let if b for l in letters]
        repl_set = set(repl_let)
        repl_set.remove(word)
        repl_let = sorted(list(repl_set))

        return repl_let

    def insert_letter(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        ins_let = []
        split_let = []
        for c in range(len(word)):
            split_let.append([word[:c], word[c:]])
        ins_let = [a + l + b for a, b in split_let for l in letters]

        return ins_let

    def edit_one_letter(self, word, allow_switches=True):
        edit_one_set = set()

        edit_one_set.update(self.del_letter(word))
        if allow_switches:
            edit_one_set.update(self.switch_letter(word))
        edit_one_set.update(self.replace_letter(word))
        edit_one_set.update(self.insert_letter(word))

        return edit_one_set

    def edit_two_letter(self, word, allow_switches=True):
        edit_two_set = set()

        edit_one = self.edit_one_letter(word, allow_switches=allow_switches)
        for w in edit_one:
            if w:
                edit_two = self.edit_one_letter(w, allow_switches=allow_switches)
                edit_two_set.update(edit_two)
        return edit_two_set

    def get_correlations(self, word, n=2):
        suggestions = []
        n_best = []

        suggestions = list((word in self.vocab and word) or self.edit_one_letter(word).intersection(self.vocab) or self.edit_two_letter(word).intersection(self.vocab))
        n_best = [[s, self.prob_of_occurr[s]] for s in list(reversed(suggestions))]

        return n_best



# In[10]:


if __name__ == "__main__":
    print(10 * '-')
    print('Type a word to check: ', end='')
    my_word = input()
    print(10 * '-')

    spell_checker = SpellChecker()  # Using default corpus 'book.txt'
    tmp_corrections = spell_checker.get_correlations(my_word, 2)

    for i, word_prob in enumerate(tmp_corrections):
        print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")


# In[ ]:





# In[ ]:




