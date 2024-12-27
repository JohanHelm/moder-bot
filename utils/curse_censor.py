import check_swear
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer


class Censorship():

    nltk.download('stopwords')
    stop_words = set(stopwords.words('russian'))

    @classmethod
    def deletepoints(cls, text: str) -> str:
        tokenizer = RegexpTokenizer(r'\w+')
        temp_text = tokenizer.tokenize(text)
        temp_text = " ".join(temp_text)
        return temp_text


    @classmethod
    def deletestopwods(cls, text : str) -> str:
        word_tokens = word_tokenize(text)
        filtered_sentence = []
        for w in word_tokens:
            if w not in cls.stop_words:
                filtered_sentence.append(w)
        filtered_sentence = " ".join(filtered_sentence)
        return filtered_sentence

    @classmethod
    def ban_words(cls):
        file_path = 'data/words.txt'
        words = []
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                word = line.strip()  # Убираем лишние пробелы и символы новой строки
                words.append(word)

        return words

    @classmethod
    async def main_filter(cls, text):
        text_without_points = cls.deletepoints(text)
        clear_text = cls.deletestopwods(text_without_points)
        sch = check_swear.SwearingCheck(bins=len(clear_text.split(' ')), stop_words = cls.ban_words())
        return max(sch.predict_proba(clear_text))




