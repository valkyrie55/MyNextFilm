#-------------------------------- LATEST CODE 23/07/2020 ----------------------------------------
#---------------------------------WITHOUT PARENTHETICALS ----------------------------------------
import re
import nltk
import spacy
import json
import textacy
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.tokenizer import Tokenizer
from nltk.tokenize import word_tokenize
from nltk.tree import *
from string import punctuation
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))

NP_count = 0
VP = 50
NNP = 0
nlp = spacy.load('en_core_web_sm')
def warn(*args, **kwargs):                      #to supress warnings
    pass
import warnings
warnings.warn = warn

random_list = []          
filename = "itsamatch.txt"
characters = ['KUSH', 'POOJA','MAID','DRIVER', 'SHOPKEEPER', 'AKASH', 'RECEPTIONIST', 'kush', 'pooja','driver','maid', 'shopkeeper', 'akash ','receptionist', 'kushagra mehta', 'Pooja', 'Kush','Akash' ]
slug_line_words = ['mall', 'car', 'cab', 'stall', 'hospital', 'hospital cafe','traffic/cab', 'chemist shop', 'evening', 'atm from', 'hotel front','bathroom', 'reception']
refined_line = []
# #read file
try:
    with open(filename, "r") as input:
        input_ = input.read().split('\n\n')
    print("File read successfully")
except: 
    print("Error reading file!")
for line in input_:
    refined_line.append(line.strip())

#read json file
try:
    with open('/home/shweta/work/MNF_work/papers/vectors/itsamatchCharacterVector.json') as f:
        data = json.load(f)
except:
    print("Error in reading json file!")

words = []
speakers_words = [] #word list for speakers and their dialogues
scenes=[]
scene=[]
priority=[]
word_importance=[]
parenthetical='NONE'
dialogues=[]
actionline=[]
scene_dic = {}
t = ()
#print("Type of t: ",type(t))
refined_line=list(filter(lambda a: a != "", refined_line))
a_counter=0

for line in refined_line:            #if new scene
    if line.startswith('INT') or line.startswith('EXT') or line.startswith('EXT/INT') or line.startswith('INT/EXT'):
        a_counter=0
        dialogue_no = 0
        scenes.append(scene)
        scene=[]
        scene.append(line)
        scene_dic['SL']=line
        continue 
    else: #if the line is simple not a scene
        speakers_info = [[]]
        lis=line.split("\n")
        lis=[l.strip() for l in lis]
        word=lis[0]
        if word.split('(')[0].strip() in characters:
            mydic={}
            #spm=re.findall(r'\(([^()]+)\)',word)
            speaker=word.split('(')[0].strip()
            if len(lis)>1 and re.match(r"\(.*\)",lis[1]):
                parenthetical = lis[1]
                parenthetical=parenthetical.replace("\n"," ")
                dia=" ".join(lis[2:])
                dia=dia.replace("\n"," ")
            
            else:
                dia = " ".join(lis[1:])
                dia = dia.replace("\n"," ")
            if not (len(dia)==0 and parenthetical=="NONE"):
                list_speaker = []
                # dialogue_no += 1
                mydic[speaker]=[parenthetical,dia,len(dia)]
                dialogues.append(mydic)
                scene.append(mydic)
                #print("List of speakers in a scene: ", list_speaker)
                speakers_info.append(list_speaker)
                #print("speakers info: ", speakers_info)
            parenthetical = "NONE"
            #print("dialogue**********\n")
            scene_dic['D'] = mydic
            
        else:
            line = line.replace("\n"," ")
            line = ' '.join(line.split())
            actionline.append(line)
            scene.append(line)
            #print("action******\n")
            a_counter = a_counter+1

            scene_dic['A'+str(a_counter)] = line
    #print(scene_dic)
scenes.append(scene)
# total_sc_cnt=0
# for sc in scenes:
#    # print(sc)
#     total_sc_cnt+=1

#print ("total scene count\n", total_sc_cnt)    
#print ("SCENES LIST")

# def lemmatize(word):
#     doc = nlp(word)
#     tokens = [token.lemma_ if token.lemma_ != '-PRON-' else token for token in doc]
#     s = " ".join(str(v) for v in tokens)
#     return s

def preprocessed_sentence(sentence):
    t = nltk.RegexpTokenizer(r"\w+")
    new_sentence = t.tokenize(sentence)
    return ' '.join(new_sentence)

new_scene=[]

scene_no=0
for scene in scenes:
    if scene_no == 0:
        scene_no = scene_no+1
        continue
    # scene_dict={}
    diag_sentence_no = 1
    sentence_no = 0
    action_counter=1
    dialogue_counter=1
    for line in scene:
        if type(line)==type(""):
            if line.startswith('INT') or line.startswith('EXT') or line.startswith('EXT/INT') or line.startswith('INT/EXT'):
                # scene_dict['SL'] = line
                slug_words=line.split(" ")
                for each_word in slug_words:
                    temp_word={}
                    temp_word['word'] = each_word
                    temp_word['scene_num'] = scene_no
                    temp_word['type'] = 'SL'
                    temp_word['type_no'] = "" 
                    temp_word['sentence_no'] = 0
                    temp_word['word_no_in sent'] = "??"
                    temp_word['importance'] = 0.5
                    temp_word['POS'] = '??pos'
                    #temp_word['Dependency'] = ''
                    words.append(temp_word)

            else:
                sent_text = line.split('.')
                for s in sent_text:
                    if s:
                        sentence = preprocessed_sentence(str(s))       #remove punchuations
                        tokens = nltk.word_tokenize(sentence)
                        pos_tag = nltk.pos_tag(tokens)
                        sentence_no = sentence_no+1
                        word_no = 0
                        for (token,pos) in pos_tag:
                            word_no = word_no + 1
                            temp_word = {}
                            temp_word['word'] = token
                            temp_word['scene_num'] = scene_no
                            temp_word['type'] = 'AC'
                            temp_word['type_no'] = str(action_counter)
                            temp_word['sentence_no'] = sentence_no
                            temp_word['word_no_in_sent'] = word_no
                            temp_word['importance'] = 0.5
                            temp_word['POS'] = pos
                            words.append(temp_word)
                action_counter += 1           

        else:
            dialogue_words = "dialoge"
            diag_list = line.keys()
            diag_list = list(diag_list)
            # print("Diag list: ")
            # print(diag_list)
            par_dia = line.values()
            par_dia = list(par_dia)
            f = diag_list[0]+"###"+par_dia[0][0]+"###"+par_dia[0][1]
            # print("f: ", f)
            #print(diag_list[0]+"###"+par_dia[0][0]+"###"+par_dia[0][1])
            # scene_dict['DL'+ str(dialogue_counter)] = f   
            temp_word={}  #for word list
            temp_word['word'] = diag_list[0]
            temp_word['scene_num'] = scene_no
            temp_word['type'] = 'DL_SPEAKER'
            temp_word['type_no'] = str(dialogue_counter)  #dialogue counter in the particular scene
            temp_word['sentence_no'] = 0
            temp_word['word_no_in_sent'] = "??"
            temp_word['importance'] = 0.5
            temp_word['POS'] = 'NNP'
            words.append(temp_word)
            parentheticals=par_dia[0][0].split(" ")
            word_no = 0
            sentence_no += 1
            for each_word in parentheticals:
                if each_word == 'NONE':
                    break
                word_no= word_no + 1
                each_word = each_word.replace("(", "")
                each_word = each_word.replace(")", "")
                temp_word={}
                temp_word['word'] = each_word
                temp_word['scene_num'] = scene_no
                temp_word['type'] = 'DL_PARENTH'
                temp_word['type_no'] = str(dialogue_counter)
                temp_word['sentence_no'] = sentence_no
                temp_word['word_no_in_sent'] = word_no
                temp_word['importance'] = 0.5
                temp_word['POS'] = '??pos'
                #temp_word['Dependency'] = ''
                words.append(temp_word)
            dialogues = par_dia[0][1].split(" ")
            # print("----------------------------------")
            # print("par_dia[0][1]: ", dialogues)
            dialogue = " ".join(dialogues)
            # print("dialogue: ", dialogue)
            diag_list = dialogue.split(".")
            # print("Dialogue list: ")
            # print(diag_list)
            for s in diag_list:
                # print("s: ", s)
                if s:
                    tokens = nltk.word_tokenize(preprocessed_sentence(s))
                    postag = nltk.pos_tag(tokens)
                    sentence_no = sentence_no + 1
                    word_no = 0
                    for (token,pos) in postag:
                        word_no=word_no+1
                        temp_word={}
                        temp_word['word'] = token
                        temp_word['scene_num'] = scene_no
                        temp_word['type'] = 'DL_DELIVERY'
                        temp_word['type_no'] = str(dialogue_counter)
                        temp_word['sentence_no'] = sentence_no
                        temp_word['word_no_in_sent'] = word_no
                        temp_word['importance'] = 0.5
                        temp_word['POS'] = pos
                        words.append(temp_word)  
            dialogue_counter = dialogue_counter + 1
    scene_no = scene_no+1
    ##see this
   
    #if scene_no > 1 : do we really need this check 
    # new_scene.append(scene_dict)

# # #####################################################################################################
sentences = []

def set_frequency(word_frequencies, scene_no, max_frequency):
    for each_word in words:
        if each_word['scene_num'] == scene_no:
            for word_ in word_frequencies.keys():
                if each_word['word'] == word_:
                    new_imp = each_word['importance'] + (word_frequencies[word_] / max_frequency)
                    each_word['importance'] = round(new_imp,2)


def filt(x):
    return x.label()=='NP'     #for Noun Phrases

def find_noun_phrases(sentence):
  noun = []
  tokens = nltk.pos_tag(word_tokenize(sentence))
  pattern = " NP:{<DT>?<JJ>*<NN>}"      # pattern for NP
  ch = nltk.RegexpParser(pattern)
  tree = ch.parse(tokens)
  for subtree in tree.subtrees(filter =  filt): 
    res = ''
    for i in range(0, len(subtree)):
      res = res + subtree[i][0] + ' '
    noun.append(res)
  return noun

def find_phrases(sentence, scene_no, sentence_no):
    if sentence.startswith('EXT') or sentence.startswith('INT'):  
        return
    verb = [] 
    noun = [] 
    pattern = r'(<VERB>?<ADV>*<VERB>+)'
    docx = textacy.make_spacy_doc(sentence, lang = "en_core_web_sm")
    verb_phrases_list = textacy.extract.pos_regex_matches(docx, pattern)
    noun = find_noun_phrases(sentence)
    for noun_phrase in noun:
        temp = {}
        temp['phrase'] = noun_phrase
        temp['importance'] = 0
        temp['phrase_type'] = 'NP'
        for each_sentence in sentences:
            if each_sentence['scene_no'] == scene_no and each_sentence['sentence_no'] == sentence_no:
                each_sentence['phrases'].append(temp)

    for chunk in verb_phrases_list:
        verb.append(chunk.text)  
#append in the phrases list
    for verb_phrase in verb:
        temp = {}
        temp['phrase'] = verb_phrase
        temp['importance'] = 0
        temp['phrase_type'] = 'VP'
        for each_sentence in sentences:
            if each_sentence['scene_no'] == scene_no and each_sentence['sentence_no'] == sentence_no:
                each_sentence['phrases'].append(temp)

def character_importance(character, scene_no, sent_no):
    for i in data['data_file']:
        if i['name'] == character.upper() :
            return i['character_importance']

def word_found(word, scene_no, sent_no):
    for each_word in words:
        if each_word['scene_num'] == scene_no and each_word['sentence_no'] == sent_no:
            print("First")
            if each_word['type'] != 'SL' and each_word['word'] == word:
                print("Second")
    return each_word

def compute_slugline_words_frequency(para):
    docx = nlp(para)
    tokens = [token.text for token in docx
        if not token.is_stop and not token.is_punct]
    slugline_words_frequency = Counter(tokens)
    return slugline_words_frequency

def set_slugline_words_importance(w, each_word, slugline_words_frequency):
    if w in slug_line_words:
        each_word['importance'] = each_word['importance'] + slugline_words_frequency[w] 

def set_slugline_sentence_importance(scene_no, sentence_no, each_sentence):
    imp = 0
    for each_word in words:
        if each_word['scene_num'] == scene_no and each_word['type'] == 'SL':
            imp += round(each_word['importance'], 2)
    return imp

def set_importance(token, sent_no, scene_no, phrase_length, NP, VP, p):
    phrase_importance = 0
    #find the token in words list
    for each_word in words:
        if each_word['scene_num'] == scene_no and each_word['sentence_no'] == sent_no and each_word['word'] == token:          
            if p == 'NP':
                # print("Its NP")
                pos = each_word['POS']
                if word in characters:
                    each_word['importance'] = each_word['importance'] + character_importance(word, scene_no, sent_no) 
                    phrase_importance = each_word['importance']
                    # print("character imp: ", phrase_importance)
                elif pos == 'NN' or 'NNS' or 'NNP' or 'NNPS' :   #city, object, etc
                    each_word['importance'] = each_word['importance'] + NP * phrase_length
                    # print("Its NN case")
                    phrase_importance = each_word['importance']
                else: 
                    each_word['importance'] = each_word['importance'] + NP * phrase_length
                    phrase_importance = each_word['importance']
                    # print("Else imp: ", each_word['importance'])
                    phrase_word_importance = phrase_word_importance + each_word['importance']

            elif p == 'VP':
                # print("Its VP")
                NP_phrase_count = 0
                for d in each_sentence['phrases']:
                    if d['phrase_type'] == 'NP':
                        NP_phrase_count += 1
                        each_word['importance'] += d['importance']
                # print("VP imp: ", each_word['importance'])
                if NP_phrase_count == 0:  
                    each_word['importance'] += VP * phrase_length
                phrase_importance = each_word['importance']

    return phrase_importance

# #create sentences list
scene_no = 1
for each_scene in scenes[1: len(scenes)]:
    # print(each_scene)
#     # print()
    sentence_counter = 1
    action_counter = 1
    dialogue_counter = 1
    for sentence in each_scene:
        # print("Sentence: ", sentence)
        if type(sentence) == type(""):                        
            if sentence.startswith('INT') or sentence.startswith('EXT') or sentence.startswith('EXT/INT') or sentence.startswith('INT/EXT'):
                temp = {}
                temp['sentence'] = preprocessed_sentence(str(sentence))
                temp['scene_no'] = scene_no
                temp['sentence_no'] = 0
                temp['type'] = 'SL'
                temp['type_no'] = ''
                temp['speaker'] = 'NONE'
                temp['phrases'] = []
                #temp['phrases'] = []
                temp['importance'] = 0
                sentences.append(temp)
            else:                                                 # AC line
                sentence_list = sentence.split('.')      #sentence list
                for sentence in sentence_list:  
                    if sentence:                  
                        temp = {}
                        temp['sentence'] = preprocessed_sentence(str(sentence))
                        temp['scene_no'] = scene_no
                        temp['sentence_no'] = sentence_counter
                        temp['type'] = 'AC'
                        temp['type_no'] = str(action_counter)
                        temp['speaker'] = '??'
                        temp['phrases'] = []
                        temp['importance'] = 0
                        sentence_counter = sentence_counter + 1
                        sentences.append(temp)
                        action_counter += 1
        elif type(sentence) == type(scene_dic):                #dictionary
            # print("sentence: ", sentence)
            for i in sentence.keys():
                SPEAKER = i
            for item in sentence.values():
                # print("item: ", item)
                for val in item:
                    if type(val) == int:
                        pass
                    elif val == 'NONE':
                        pass
                    elif type(val) == type(" "):  
                        sent = val.split(".")
                        for s in sent: 
                            if s:
                                if s.startswith("("):           #parenthetical
                                    temp = {}
                                    temp['sentence'] = preprocessed_sentence(str(s))
                                    temp['scene_no'] = scene_no
                                    temp['sentence_no'] = sentence_counter
                                    temp['type'] = 'DL_PARENTH'
                                    temp['type_no'] = ''
                                    temp['speaker'] = SPEAKER
                                    temp['phrases'] = []
                                    temp['importance'] = 0
                                    sentence_counter += 1
                                    sentences.append(temp)                    
                                else:  #dialogue
                                    temp = {}
                                    temp['sentence'] = preprocessed_sentence(str(s))
                                    temp['scene_no'] = scene_no
                                    temp['sentence_no'] = sentence_counter
                                    temp['type'] = 'DL_DELIVERY'
                                    temp['type_no'] = str(dialogue_counter)
                                    temp['speaker'] = SPEAKER
                                    temp['phrases'] = []
                                    temp['importance'] = 0
                                    sentences.append(temp)
                                    sentence_counter += 1
                                    dialogue_counter += 1
    scene_no = scene_no +1

# # #find phrases
for each_sentence in sentences:
    find_phrases(each_sentence['sentence'], each_sentence['scene_no'], each_sentence['sentence_no'])

# # word frequency at scene level
for scene_no in range(1, len(scenes)):
    sentence = ''
    for each_sentence in sentences:
        if each_sentence['scene_no'] == scene_no:   
            try:
                sentence = sentence + each_sentence['sentence'] + '. '    #merge
            except:
                print("Some error in concatenation")
    docx = nlp(sentence)
    tokens = [token.text for token in docx
        if not token.is_stop and not token.is_punct]
    word_frequencies = Counter(tokens)
    l = []
    for i in word_frequencies.values():
        l. append(i)
    l.sort(reverse = True)            #sort in descending order
    max_frequency = l[0]
    set_frequency(word_frequencies, scene_no, max_frequency)                                   
    scene_no = scene_no + 1

for sent in sentences:
    for each_dict in sent['phrases']:                   # calculate total Noun Phrases in the script
        if each_dict['phrase_type'] == 'NP':
            NP_count = NP_count + 1

for e in words:                                        
    if e['POS'] == 'NNP':                               # a constant value for all the Proper Nouns
        NNP += 1      
NP = NNP / NP_count * 100
NP = round(NP, 2)

# for each_sentence in sentences:
#     if each_sentence['scene_no'] == 4 and each_sentence['sentence_no'] == 14:
#         print("Sentence: ", each_sentence['sentence'])
#         sent_no = each_sentence['sentence_no']
#         scene_no = each_sentence['scene_no']
#         for each_dict in each_sentence['phrases']:
#             ph = each_dict['phrase']
#             p = each_dict['phrase_type']
#             tokens = nltk.word_tokenize(ph)
#             phrase_length = len(tokens)
#             for token in tokens:
#                 if token.lower() not in STOP_WORDS:
#                     print("Phrase: ", token)
#                     imp = set_importance(token, sent_no, scene_no, phrase_length, NP, VP, p)
#                     each_dict['importance'] = each_dict['importance'] + round(imp, 2)
#                     print("Each_dict: ", each_dict['importance'])

for each_sentence in sentences:
    sent_no = each_sentence['sentence_no']
    scene_no = each_sentence['scene_no']
    for each_dict in each_sentence['phrases']:
        ph = each_dict['phrase']
        p = each_dict['phrase_type']
        tokens = nltk.word_tokenize(ph)
        phrase_length = len(tokens)
        for token in tokens:
            if token.lower() not in STOP_WORDS:
                    # print("Phrase: ", token)
                    imp = set_importance(token, sent_no, scene_no, phrase_length, NP, VP, p)
                    each_dict['importance'] = each_dict['importance'] + round(imp, 2)
                    # print("Each_dict: ", each_dict['importance'])
# # # print("Done!")
# # #scene string
for scene_no in range(1, len(scenes)+1):
    para = ''
    for each_sentence in sentences:
        try:
            para = para + each_sentence['sentence'].lower() + '. '    #merge
        except:
            print("Error while concatenation")

# #  #overall frequency distribution of slug line words in the script
slugline_words_frequency = compute_slugline_words_frequency(para)

# # # # # # #slug line importance
for scene_no in range(1, len(scenes)):
    for each_word in words:
        if each_word['scene_num'] == scene_no and each_word['type'] == 'SL' and each_word['word'] != 'EXT' and each_word['word'] != 'INT' and each_word['word'] != 'EXT/INT':
            w = each_word['word'].lower()
            w = w.replace('.', '')
            w = w.replace('-', '')
            set_slugline_words_importance(w, each_word, slugline_words_frequency)

# # # # # # # # ########################### Sentence Importance ##################
# # # # # #slug line
for each_sentence in sentences:
    scene_no = each_sentence['scene_no']
    sentence_no = each_sentence['sentence_no']
    if each_sentence['type'] == 'SL':
        each_sentence['importance'] += set_slugline_sentence_importance(scene_no, sentence_no, each_sentence)

for each_sentence in sentences:
    scene_no = each_sentence['scene_no']
    sentence_no = each_sentence['sentence_no']
    sent_imp = 0
    for each_dict in each_sentence['phrases']:
        sent_imp = sent_imp + each_dict['importance']
        each_sentence['importance'] = each_sentence['importance'] +  round(sent_imp, 2)
        each_sentence['importance'] = round(each_sentence['importance'], 2)

# for s in sentences:
#     print("Sentence: ", s['sentence']," || Scene: ", s['scene_no']," || Sent no: ", s['sentence_no'], " || Importance: ", s['importance'])
#     print()

for s in words:
    print(s)
    print()