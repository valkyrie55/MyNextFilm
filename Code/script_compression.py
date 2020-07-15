import re
import nltk
import random
import spacy
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
#pip install textacy

def warn(*args, **kwargs):                      #to supress warnings
    pass
import warnings
warnings.warn = warn

random_list = []          
filename = "itsamatch.txt"
characters = ['KUSH', 'POOJA', 'DRIVER', 'SHOPKEEPER', 'AKASH', 'RECEPTIONIST', 'Pooja', 'Kush', 'Kushagra Mehta']
refined_line = []
#read file
try:
    with open(filename, "r") as input:
        input_ = input.read().split('\n\n')
    print("File read successfully")
except: 
    print("Error reading file!")
for line in input_:
    refined_line.append(line.strip())

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
total_sc_cnt=0
for sc in scenes:
   # print(sc)
    total_sc_cnt+=1

print ("total scene count\n", total_sc_cnt)    
#print ("SCENES LIST")

new_scene=[]

scene_no=0
for scene in scenes:
    if scene_no == 0:
        scene_no = scene_no+1
        continue
    
    scene_dict={}
    action_counter=1
    dialogue_counter=1
    for line in scene:
        if type(line)==type(""):
            if line.startswith('INT') or line.startswith('EXT') or line.startswith('EXT/INT') or line.startswith('INT/EXT'):
                scene_dict['SL'] = line
                slug_words=line.split(" ")
                for each_word in slug_words:
                    temp_word={}
                    temp_word['word'] = each_word
                    temp_word['scene_num'] = scene_no
                    temp_word['type'] = 'SL'
                    temp_word['type_no'] = "" 
                    temp_word['sentence_no'] = '??'
                    temp_word['word_no_in sent'] = "??"
                    temp_word['importance'] = 0.5
                    temp_word['POS'] = '??pos'
                    #temp_word['Dependency'] = ''
                    words.append(temp_word)

            else:
                scene_dict['AC'+ str(action_counter)] = line
                #print ("Scene_dic  ", scene_dict)
                sent_text = nltk.sent_tokenize(line)
                #print("Sent_text", sent_text)
                sentence_no=0
                for sentence in sent_text:
                    tokens = nltk.word_tokenize(sentence)
                    postag=nltk.pos_tag(tokens)
                    #print ("posttag", postag)
                    sentence_no=sentence_no+1
                    word_no=0
                    for (token,pos) in postag:
                        word_no=word_no+1
                        temp_word={}
                        temp_word['word'] = token.lower()
                        temp_word['scene_num'] = scene_no
                        temp_word['type'] = 'AC'
                        temp_word['type_no'] = str(action_counter)
                        temp_word['sentence_no'] = sentence_no
                        temp_word['word_no_in_sent'] = word_no
                        temp_word['importance'] = 0.5
                        temp_word['POS'] = pos
                        #temp_word['Dependency'] = ''
                        words.append(temp_word)
                        #print("temp word in action")
                    #print("Words in action", action_counter, )
                    #print(words)
                action_counter = action_counter + 1

        else:
            dialogue_words="dialoge"
            diag_list = line.keys()
            diag_list=list(diag_list)
            par_dia=line.values()
            par_dia=list(par_dia)
            f=diag_list[0]+"###"+par_dia[0][0]+"###"+par_dia[0][1]
            #print(diag_list[0]+"###"+par_dia[0][0]+"###"+par_dia[0][1])
            scene_dict['DL'+ str(dialogue_counter)] = f   
            temp_word={}  #for word list
            temp_word['word'] = diag_list[0]
            temp_word['scene_num'] = scene_no
            temp_word['type'] = 'DL_SPEAKER'
            temp_word['type_no'] = str(dialogue_counter)  #dialogue counter in the particular scene
            temp_word['sentence_no'] = '??'
            temp_word['word_no_in_sent'] = "??"
            temp_word['importance'] = 0.5
            temp_word['POS'] = 'NNP'
            #temp_word['Dependency'] = ''
            words.append(temp_word)
            #print(temp_word) 
            parentheticals=par_dia[0][0].split(" ")
            word_no=0
            
            for each_word in parentheticals:
                if each_word=='NONE':
                    break
                word_no= word_no+1
                each_word = each_word.replace("(", "")
                each_word = each_word.replace(")", "")
                temp_word={}
                temp_word['word'] = each_word.lower()
                temp_word['scene_num'] = scene_no
                temp_word['type'] = 'DL_PARENTH'
                temp_word['type_no'] = str(dialogue_counter)
                temp_word['sentence_no'] = 1
                temp_word['word_no_in_sent'] = word_no
                temp_word['importance'] = 0.5
                temp_word['POS'] = '??pos'
                #temp_word['Dependency'] = ''
                words.append(temp_word)
                #print(temp_word) +
            dialogues=par_dia[0][1].split(" ")
            #print("dial=============", dialogues)
            sent_text = nltk.sent_tokenize(par_dia[0][1])
            sentence_no=0
            for sentence in sent_text:
                tokens = nltk.word_tokenize(sentence)
                postag=nltk.pos_tag(tokens)
                sentence_no=sentence_no+1
                word_no=0
                for (token,pos) in postag:
                    word_no=word_no+1
                    temp_word={}
                    temp_word['word'] = token.lower()
                    temp_word['scene_num'] = scene_no
                    temp_word['type'] = 'DL_DELIVERY'
                    temp_word['type_no'] = str(dialogue_counter)
                    temp_word['sentence_no'] = sentence_no
                    temp_word['word_no_in_sent'] = word_no
                    temp_word['importance'] = 0.5
                    temp_word['POS'] = pos
                    words.append(temp_word)   
            dialogue_counter = dialogue_counter + 1
    ##see this
   
    #if scene_no > 1 : do we really need this check 
    new_scene.append(scene_dict)
    scene_no = scene_no+1
# for each_word in words:
#   print(each_word)
#   print()

# for sc in scenes:
#   print(sc)
#   print()
#####################################################################################################
sentences = []

def set_frequency(word_frequencies, scene_no, max_frequency):
    # word = 'mall'
    # print(word_frequencies[word])
    for each_word in words:
        if each_word['scene_num'] == scene_no:
            for word_ in word_frequencies.keys():
                if each_word['word'] == word_:
                    new_imp = each_word['importance'] + (word_frequencies[word_] / max_frequency)
                    each_word['importance'] = round(new_imp,2)

def preprocessed_sentence(sentence):
    t = nltk.RegexpTokenizer(r"\w+")
    sentence = str(sentence)
    new_sentence = t.tokenize(sentence)
    return ' '.join(new_sentence)

def lemmatize(sentence):
  try:
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')      #preprocessing
    sentence = re.sub(BAD_SYMBOLS_RE,"",sentence.lower())
  except:
    print("Error in Preprocessing")
  try:
    lemma = WordNetLemmatizer()
    lemmatized_sentence = " ".join(lemma.lemmatize(word) for word in word_tokenize(sentence))
    return lemmatized_sentence
  except: 
    print("Error in performing Lemmatization")

def filt(x):
    return x.label()=='NP'     #for Noun Phrases

def find_noun_phrases(sentence):
  noun = []
  tokens = nltk.pos_tag(word_tokenize(sentence))
  pattern = " NP:{<DT>?<JJ.*>*<NN.*>+}"      #random pattern
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

SCENES = []

def character_importance(character, scene_no):
    imp_of_character = 0
    total_dialogues = 0
    for each_sentence in sentences:
        if each_sentence['scene_num'] == scene_no:
            if each_sentence['type'] == 'DL_PARENTH' or each_sentence['type'] == 'DL_DELIVERY':
                if each_sentence['speaker'] == character:
                    imp_of_character += 1    #dialgue count
                total_dialogues += 1
    return (imp_of_character / total_dialogues )

#create sentence list
nlp = spacy.load('en_core_web_sm')

scene_no = 1
for each_scene in scenes[1: len(scenes)]:
    #print("Scene no: ", scene_no)
    sentence_counter = 1
    action_counter = 1
    dialogue_counter = 1
    for sentence in each_scene:
        if type(sentence) == type(""):                        
            if sentence.startswith('INT') or sentence.startswith('EXT') or sentence.startswith('EXT/INT') or sentence.startswith('INT/EXT'):
                temp = {}
                temp['sentence'] = sentence
                temp['scene_no'] = scene_no
                temp['sentence_no'] = 0
                temp['type'] = 'SL'
                temp['type_no'] = ''
                temp['speaker'] = 'NONE'
                temp['phrases'] = []
                #temp['phrases'] = []
                temp['importance'] = 0
                sentences.append(temp)
            else:                                                              # AC line
                docx = nlp(sentence)
                sents = list(docx.sents)      #sentence list
                for sentence in sents:                                           
                    temp = {}
                    temp['sentence'] = preprocessed_sentence(sentence)
                    temp['scene_no'] = scene_no
                    temp['sentence_no'] = str(sentence_counter)
                    temp['type'] = 'AC'
                    temp['type_no'] = str(action_counter)
                    temp['speaker'] = '??'
                    temp['phrases'] = []
                    temp['importance'] = 0
                    sentence_counter = sentence_counter + 1
                    sentences.append(temp)
                    action_counter += 1
        elif type(sentence) == type(scene_dic):                #dictionary
            for i in sentence.keys():
                SPEAKER = i
            for item in sentence.values():
                for val in item:
                    # print("Val: ",val)
                    # print("Type: ", type(val))
                    if type(val) == int:
                        pass
                    elif val == 'NONE':
                        pass
                    elif type(val) == type(" "):                
                        if val.startswith("("):           #parenthetical
                            temp = {}
                            temp['sentence'] = preprocessed_sentence(val)
                            temp['scene_no'] = scene_no
                            temp['sentence_no'] = str(sentence_counter)
                            temp['type'] = 'DL_PARENTH'
                            temp['type_no'] = ''
                            temp['speaker'] = SPEAKER
                            temp['phrases'] = []
                            temp['importance'] = 0
                            sentence_counter += 1
                            sentences.append(temp)                    
                        else:  #dialogue
                            temp = {}
                            temp['sentence'] = preprocessed_sentence(val)
                            temp['scene_no'] = scene_no
                            temp['sentence_no'] = str(sentence_counter)
                            temp['type'] = 'DL_DELIVERY'
                            temp['type_no'] = str(dialogue_counter)
                            temp['speaker'] = SPEAKER
                            temp['phrases'] = []
                            temp['importance'] = 0
                            sentences.append(temp)
                            sentence_counter += 1
                            dialogue_counter += 1
    scene_no = scene_no +1

for each_sentence in sentences:
    find_phrases(str(each_sentence['sentence']),each_sentence['scene_no'], each_sentence['sentence_no'])

#word frequency 
scene_no = 1    
sentence_counter = 1
for scene_no in range(1, len(scenes)):
    sentence = ''
    for each_sentence in sentences:
        if each_sentence['scene_no'] == scene_no and each_sentence['type'] != 'SL':
          try:
            sentence = sentence + str(each_sentence['sentence']) + '. '    #merge
            sentence_counter = sentence_counter + 1
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
    # print(l)
    max_frequency = l[0]
    #print("Max frequency: ",  max_frequency)                    #Assign the frequencies to suitable sections in the list
    set_frequency(word_frequencies, scene_no, max_frequency)                                   
    scene_no = scene_no + 1
    
# print("Word list: ------------------------------------------------------------")
# for each_word in words:
#   print(each_word)
#   print()
# print()
# print("Sentences list: ------------------------------------------------------------")
# for each_sent in sentences:
#   print(each_sent)
#   print()

#Assign importance to pharses
DATE = 2.5
TIME = 2.5
CD = 3    # Numeric values
NP = 5
VP = 5

for each_sentence in sentences:
   # print("Sentence: ", each_sentence['sentence'])
    scene_no = each_sentence['scene_no']
    sent_no = each_sentence['sentence_no']
    sentence_type = each_sentence['type']
    for each_dict in each_sentence['phrases']:
        phrase_importance = 0
        ph = each_dict['phrase']
        #print("Phrase: ", ph)
        tokens = nltk.word_tokenize(ph)
        phrase_length = len(tokens)
        for token in tokens:
    # print("Token: ", token)
                for each_word in words:
                    if each_word['scene_num'] == scene_no and each_word['type'] != 'SL' and each_word['sentence_no'] == int(sent_no):
                        if each_word['word'] == token and each_dict['phrase_type'] =='NP':
                            pos = each_word['POS']
                            if pos == 'NNP':
                               # print("Its NNP")
                                if word in characters:
                                     each_word['importance'] = each_word['importance'] + character_importance(phrase_word, scene_no) * l
                                else:   #city, etc
                                    each_word['importance'] = each_word['importance'] + (NP * 1.5) * phrase_length
                            else: 
                                each_word['importance'] = each_word['importance'] + NP * phrase_length
                                #phrase_importance += each_word['importance']
                            phrase_importance += each_word['importance']
                            #print("Phrase importance: ", phrase_importance)
                            each_dict['importance'] = each_dict['importance'] + phrase_importance
                            #print(each_dict['importance'])
                        # elif each_word['word'] == token and each_dict['phrase_type'] =='VP':
                        #     #print("Verb phrase----------------------")
                        #     for d in each_sentence['phrases']:
                        #         if d['phrase_type'] == 'NP':
                        #             each_dict['importance'] += d['importance']
                        #     #print(each_dict['importance'])
                        else:
                            pass
    
for each_sentence in sentences:
    found = 0
    scene_no = each_sentence['scene_no']
    sent_no = each_sentence['sentence_no']
    sentence_type = each_sentence['type']
    for each_dict in each_sentence['phrases']:
        phrase_importance = 0
        ph = each_dict['phrase']
        #print("Phrase: ", ph)
        tokens = nltk.word_tokenize(ph)
        l = len(tokens)
        for token in tokens:
            #if token not in STOP_WORDS:
               # print("Token: ", token)
                for each_word in words:
                    if each_word['scene_num'] == scene_no and each_word['type'] != 'SL' and each_word['sentence_no'] == int(sent_no):
                        if each_word['word'] == token and each_dict['phrase_type'] =='VP':
                            if token in characters:
                                     each_word['importance'] = each_word['importance'] + character_importance(phrase_word, scene_no) * l
                            # print("Verb phrase------------")
                            # print("Phrase: ", ph)
                            for d in each_sentence['phrases']:
                                if d['phrase_type'] == 'NP':
                                    found += 1
                                if found < 1:   #no noun phrase
                                    each_word['importance'] = each_word['importance'] + VP * l
                                    phrase_importance += each_word['importance']
                            each_dict['importance'] = each_dict['importance'] + phrase_importance


            # l = len(phrase)
            # print()
            # for ent in phrase_doc.ents:
            #     print("Entity: ",ent)                # print("Entity: ", ent)
                # if not ent in STOP_WORDS:
                #     temp = {}
                #     temp['word'] = ent
                #     temp['entity'] = ent.label_
                #     for each_word in words:
                #         if each_word['scene_num'] == scene_no and each_word['sentence_no'] == sentence_no and each_word['word'] == ent:                       
                #             if ent.label_ == 'DATE':
                #                 each_word['importance'] = (each_word['importance'] + DATE) * l
                #                 temp['importance'] = each_word['importance']
                #             elif ent.label_ == 'TIME':
                #                 each_word['importance'] = (each_word['importance'] + TIME) * l
                #                 temp['importance'] = each_word['importance']
                #             elif each_word['type'] == 'DL_SPEAKER':                 #character
                #                 CH = imp_of_character()        #in scene
                #                 each_word['importance'] = (each_word['importance'] + CH) * l
                #                 temp['importance'] = each_word['importance']
                #             elif each_word['POS'] == 'VB' or each_word['POS'] == 'VBZ':
                #                 each_word['importance'] = (each_word['importance'] + VERB) * l
                #                 temp['importance'] = each_word['importance']
                #             elif each_word['POS'] == 'CD':
                #                 each_word['importance'] = (each_word['importance'] + CD) * l
                #                 temp['importance'] = each_word['importance']
                #             elif each_word['POS'] == 'RB' or each_word['POS'] == 'JJ':
                #                 each_word['importance'] = (each_word['importance'] + AB) * l
                #                 temp['importance'] = each_word['importance']
                #             else:
                #                 pass      # location, object, etc to be added
                #     to be worked on
                #sentences['entity'].append(temp)

# ########################### Sentence Importance ##################

for each_sentence in sentences:
    scene_no = each_sentence['scene_no']
    sentence_no = each_sentence['sentence_no']
    sent_imp = 0
    for each_dict in each_sentence['phrases']:
        sent_imp = sent_imp + each_dict['importance']
    each_sentence['importance'] = sent_imp

# print("Sentences list: ------------------------------------------------------------")
# for each_sent in sentences:
#   print(each_sent)
#   print()

# print("Sentences and importance list: ------------------------------------------------------------")
# for each_sent in sentences:
#   print("Sentence: ",each_sent['sentence'], "| Importance ", each_sent['importance'])
#   print()
########################### Scene Importance ##################

# for i in range(1, len(scenes)):
#     for each_sentence in sentences:
#     scene_no = each_sentence['scene_no']

# for each_word in words:
#   print(each_word)
#   print()

    
print("Word list: ------------------------------------------------------------")
for each_word in words:
  print(each_word)
  print()
