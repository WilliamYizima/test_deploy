# sentence = ["Quero saber qual produto eu consigo melhorar minha queda de cabelo?"]
# sentence2 = ["Preciso de um produto que faça meu cabelo parar de cair"]
"""
- Como combater os danos causados pelo sol neste verão?
- Como proteger meu cabelo dos danos causados pelo sol?
- Meu cabelo está ressecado. Como tratar?
- Qual linha para proteger meus cabelos do sol, vento e mar?
- Qual produto para combater a quebra do cabelo?
- Meu cabelo está fraco e preciso nutrir melhor eles
- Quero restaurar a maciez e brilho dos meus cabelos
"""

import openai
import pt_core_news_lg


class NLPExtract:
    """ use open ai response and nlp analyze to extract entities and response questions """

    def __init__(self, open_api_key,stop_words = ["afirmar","resposta","frase"], question_resume = False):
        self._openai_api_key = open_api_key
        self._nlp_instance = pt_core_news_lg.load()
        self._stop_words = stop_words
        self._question_resume = question_resume

        self._question = None
        self._entities = None
        self._response_question = None
        self._resume_question = None


    def _get_resume_question(self):
        openai.api_key = self._openai_api_key
        question = f'O que é pedido na frase: "{self.question}"'
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                temperature=0.15,
                max_tokens=1000,
                top_p=1,
                #   frequency_penalty=0.0,
                #   presence_penalty=0.6,
                stop=[" Human:", " AI:"]
                )
        self._resume_question = response["choices"][0]["text"]
        return self._resume_question

    def _sentence_lemma(self):
        docs = self._nlp_instance.pipe([self.question])
        docs = list(docs)
        list_sentence = []
        for token in docs[0]:
            if(token.pos_ == "VERB" or token.pos_ == "NOUN" or token.pos_ == "ADJ"):
                token_lemma = token.lemma_.split(' ')[0] if len(token.lemma_.split(' ')) > 0 else token.lemma_
                if token_lemma not in self._stop_words:
                    list_sentence.append(token_lemma)
        list_sentence_excluded_duplicated = list(set(list_sentence))
        list_sentence_excluded_duplicated.sort()
        self._entities = list_sentence_excluded_duplicated
        return self._entities

    def _get_resume_response(self):
        openai.api_key = self._openai_api_key
        question = f'Responda de forma resumida  a frase:"{self.question}"'
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                temperature=0.15,
                max_tokens=1000,
                top_p=1,
                #   frequency_penalty=0.0,
                #   presence_penalty=0.6,
                stop=[" Human:", " AI:"]
                )
        self._response_question = response["choices"][0]["text"]
        return self._response_question

    def _dto_payload(self):
        return {"question": self.question,
                "entities": self._entities,
                "sentence_semantic": self.question,
                "response_question": self._response_question.replace("\n","") if self._response_question else self._response_question
                # "count_words": len(sentence_semantic)
                }

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, question_input):
        if(self._question_resume):
            self._question = self._get_resume_question(sentence=question_input)
        else:
            self._question = question_input

    def analyze(self, sentence: str):
        """
        pipe:
        - send question to chatgpt
        - extract lemma
        - create payload
        """
        self.question = sentence
        self._sentence_lemma()
        self._get_resume_response()
        return self._dto_payload()
