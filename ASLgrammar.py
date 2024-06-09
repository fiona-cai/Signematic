import spacy

nlp = spacy.load('en_core_web_md')

def SOTVify(english_grammar):
    doc = nlp(english_grammar.lower())
    print('>',doc)
    sentences_data = POStokenize(doc)
    sentences = \
        [
            dict(subjects=[t.text for t in s.subjects],
                 objects=[t.text for t in s.objects],
                 times=[t.text for t in s.times],
                 verbs=[t.text for t in s.verbs]
                 )
            for s in sentences_data
        ]
    #print(sentences)
    ARTICLES=['a','an','the']
    TO_BE_VERBS=['am','is','are','was','were','be','being','been']
    if sentences:
        l = [' '.join(sentences[0][d]) for d in sentences[0]]
        print(' '.join(l).replace('  ',' '))
    else:
        print(' '.join([i for i in english_grammar.lower().split() if i not in ARTICLES+TO_BE_VERBS]))

class POS: #part of speech
    VERB, OBJECT, SUBJECT, TIME, MOD = 1,2,3,4,5

class Token:
    def __init__(self, text, lemma, pos):
        self.part_of_speech = pos
        self.text = text
        self.lemma = lemma  # use to find videos for objects and verbs
        text = lemma if pos is POS.OBJECT or pos is POS.VERB else text

class Sentence:
    def __init__(self):
        self.verbs = list()
        self.subjects = list()
        self.objects = list()
        self.times = list()

    def add_word(self, pos, token, adjs):
        word_list = None
        if pos == POS.VERB:
            word_list = self.verbs
        if pos == POS.SUBJECT:
            word_list = self.subjects
        if pos == POS.OBJECT:
            word_list = self.objects
        if pos == POS.TIME:
            word_list = self.times
        word_list.append(Token(text=token.text, lemma=token.lemma_, pos=pos))
        while adjs:
            word_list.append(adjs.pop(0))


def POStokenize(doc):
    sentences = list()
    sentence = None
    # adjectives go after subjects or objects
    adjs = []
    for token in doc:
        if not sentence:
            sentence = Sentence()
        token_pos = token.pos_
        if token_pos == 'VERB':
            # 'to be' verbs are not used in ASL
            if token.lemma_ == 'be':
                continue
            sentence.add_word(POS.VERB, token, adjs)
        elif token_pos == 'NOUN':
            if token.dep_ == 'npadvmod':        # modifiers are adjectives
                sentence.add_word(POS.TIME, token, adjs)
            else:
                sentence.add_word(POS.OBJECT, token, adjs)
        elif token_pos == 'PRON':
            if token.dep_ == 'npadvmod':
                sentence.add_word(POS.TIME, token, adjs)
            elif not sentence.subjects:         # just append first subject
                sentence.add_word(POS.SUBJECT, token, adjs)
        elif token_pos == 'ADJ':
            adjs.append(Token(text=token.text, lemma=token.lemma_, pos=POS.MOD))
        elif token_pos == 'PUNCT' or token.text == 'then':  # new sentence
            if True: #if sentence.verbs and (sentence.objects or sentence.subjects):
                sentences.append(sentence)
                adjs = None
                sentence = None
    if sentence.verbs and (sentence.objects or sentence.subjects):
        sentences.append(sentence)
    return sentences

SOTVify('Hello there')
SOTVify('I had coffee for breakfast')
SOTVify('I ate a cold pizza')
SOTVify('You ate a cold pizza ')
SOTVify('Meet me at the park at noon')
SOTVify('You are tall')
SOTVify('I go to Idaho')
