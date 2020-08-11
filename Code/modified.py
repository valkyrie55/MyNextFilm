######################################################### PART I CODE ###############################################################
###########   updated code for dialogues - its half only
import re
import nltk
import spacy
import json
import textacy
import docx 
from docx.shared import Inches, Pt
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
nlp = spacy.load('en_core_web_sm')
def warn(*args, **kwargs):                      #to supress warnings
    pass
import warnings
warnings.warn = warn

random_list=[]

def create_character_list():
    for i in data['data_file']:
        characters.append(i['name'])

def preprocessed_sentence(sentence):                 # for removing punchuations
    t = nltk.RegexpTokenizer(r"\w+")
    new_sentence = t.tokenize(sentence)
    return ' '.join(new_sentence)

def filt(x):
    return x.label()=='NP'                           # for Noun Phrases

def find_noun_phrases(sentence):
  noun = []
  tokens = nltk.pos_tag(word_tokenize(sentence))
  pattern = " NP:{<DT>?<JJ>*<NN>}"                   # pattern for NP
  ch = nltk.RegexpParser(pattern)
  tree = ch.parse(tokens)
  for subtree in tree.subtrees(filter =  filt): 
    res = ''
    for i in range(0, len(subtree)):
      res = res + subtree[i][0] + ' '
    noun.append(res)
  return noun

def find_phrases(sentence, scene_no, sentence_no_in_scene, sent_type, paragraph_no):
    if sentence:
        verb = [] 
        noun = [] 
        sentence = sentence.lower()
        pattern = r'(<VERB>?<ADV>*<VERB>+)'
        docx = textacy.make_spacy_doc(sentence, lang = "en_core_web_sm")
        verb_phrases_list = textacy.extract.pos_regex_matches(docx, pattern)
        noun = find_noun_phrases(sentence)
        val = 1
        for noun_phrase in noun:
            if noun_phrase: 
                temp = {}
                temp['phrase'] = noun_phrase
                temp['importance'] = val
                temp['phrase_type'] = 'NP'
                # append phrase data in sentences list
                for each_sentence in sentences:
                    if each_sentence['type'] == 'AC':
                        if each_sentence['scene_no'] == scene_no and each_sentence['sentence_no_in_scene'] == sentence_no_in_scene:
                            each_sentence['phrases'].append(temp)                   
                temp['scene_no'] = scene_no
                temp['sentence_no_in_scene'] = sentence_no_in_scene
                temp['type'] = sent_type
                temp['paragraph_no'] = paragraph_no
                phrases.append(temp)
                val += 1
        # apply same procedure for verb phrases
        for chunk in verb_phrases_list:
            verb.append(chunk.text)  
        #append in the phrases list
        for verb_phrase in verb:
            if verb_phrase:
                temp = {}
                temp['phrase'] = verb_phrase
                temp['importance'] = val
                temp['phrase_type'] = 'VP'
                for each_sentence in sentences:
                    if each_sentence['type'] == 'AC':
                        if each_sentence['scene_no'] == scene_no and each_sentence['sentence_no_in_scene'] == sentence_no_in_scene:
                            each_sentence['phrases'].append(temp)
                temp['scene_no'] = scene_no
                temp['sentence_no_in_scene'] = sentence_no_in_scene
                temp['type'] = sent_type
                temp['paragraph_no'] = paragraph_no
                phrases.append(temp)
                val += 1


# extract characters from .json file
def create_character_list():
    for i in data['data_file']:
        characters.append(i['name'])

# extract character importance from .json file
def character_importance(character_name):
    for i in data['data_file']:
        if i['name'] == character_name.upper() :
            return i['character_importance']

def set_importance(phrase, sent_no, scene_no, importance):
    for each_phrase in phrases:
        if each_phrase['scene_no'] == scene_no and each_phrase['type'] == 'AC' and each_phrase['sentence_no_in_scene'] == sent_no and each_phrase['phrase'].lower() == phrase.lower():          
            each_phrase['importance'] = each_phrase['importance'] * importance 

def set_importance1(ph, sent_no, scene_no, importance):
    for each_phrase in phrases:
        if each_phrase['scene_no'] == scene_no and each_phrase['type'] == 'AC' and each_phrase['sentence_no_in_scene'] == sent_no and each_phrase['phrase'].lower() == ph.lower() :    
                each_phrase['importance'] = each_phrase['importance'] * importance 
#calculate imp of the sentences
def set_importance2(phrase, scene_no, sent_no):
    for each_phrase in phrases:
        if each_phrase['scene_no'] == scene_no and each_phrase['type'] == 'AC' and each_phrase['sentence_no_in_scene'] == sent_no and each_phrase['phrase'].lower() == phrase.lower() : 
            return each_phrase['importance']
    return 0

# read file
filename = "itsamatch.txt"
refined_line = []
try:
    with open(filename, "r") as input:
        input_ = input.read().split('\n\n')
    print(" File read successfully")
except: 
    print(" Error reading file!")

for line in input_:
    refined_line.append(line.strip())

#read json file
try:
    with open('/home/shweta/work/MNF_work/papers/vectors/itsamatchCharacterVector.json') as f:
        data = json.load(f)
except:
    print("Error in reading json file")
words = []
phrases = []
speakers_words = [] #word list for speakers and their dialogues
scenes=[]
characters = []
scene=[]
priority=[]
phrase_importance = []
sent_importance=[]
parenthetical='NONE'
dialogues=[]
actionline=[]
scene_dic = {}
t = ()
refined_line=list(filter(lambda a: a != "", refined_line))
a_counter=0

create_character_list() 

##CREATE SCENES LIST ALONG ACTION AND DIALOGUES IN THE GIVEN SEQUENCE   MAY UPDATE THE CODE FROM SHIVAM  ##RENU
for line in refined_line:            #if new scene
    if line.startswith('INT') or line.startswith('EXT') or line.startswith('EXT/INT') or line.startswith('INT/EXT'):
        a_counter=0
        #scene_number += 1
        dialogue_no = 0
        scenes.append(scene)
        #print(scene)
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
                dia = " ".join(lis[2:])
                dia = dia.replace("\n"," ")
            
            else:
                dia = " ".join(lis[1:])
                dia = dia.replace("\n"," ")
            if not (len(dia)==0 and parenthetical=="NONE"):
                list_speaker = []
                # dialogue_no += 1
                mydic[speaker]=[parenthetical,dia,len(dia)]
                dialogues.append(mydic)
                scene.append(mydic)
                speakers_info.append(list_speaker)
            parenthetical = "NONE"
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

# create sentences list
sentences = []
scene_no = 1
for each_scene in scenes[1: len(scenes)]:
    paragraph_no = 0
    sentence_counter = 1
    action_counter = 1
    for sentence in each_scene:
        if type(sentence) == type(""):                        
            if sentence.startswith('INT') or sentence.startswith('EXT') or sentence.startswith('EXT/INT') or sentence.startswith('INT/EXT'):
                temp = {}
                temp['sentence'] = sentence 
                temp['scene_no'] = scene_no
                temp['sentence_no_in_scene'] = 0
                temp['type'] = 'SL'
                temp['type_no'] = ''
                temp['speaker'] = '??'
                temp['phrases'] = []
                temp['importance'] = 0
                temp['final_importance'] = 0
                temp['zero_one'] = '1'
                temp['paragraph_no'] = paragraph_no
                sentences.append(temp)
            else:       
                paragraph_no += 1                                      # AC line
                sentence_list = sentence.split('.')                    # sentence list
                val = 1
                for sentence in sentence_list:  
                    if sentence:                  
                        temp = {}
                        temp['sentence'] = sentence + '. '
                        temp['scene_no'] = scene_no
                        temp['sentence_no_in_scene'] = sentence_counter
                        temp['type'] = 'AC'
                        temp['type_no'] = str(action_counter)
                        temp['speaker'] = '??'
                        temp['phrases'] = []
                        temp['final_importance'] = 0
                        temp['zero_one'] = '1'
                        temp['importance'] = val
                        temp['paragraph_no'] = paragraph_no
                        sentence_counter = sentence_counter + 1
                        sentences.append(temp)
                        action_counter += 1
                        val += 1
        else:                      # dialogues
            dialogue_words = "dialoge"
            diag_list = sentence.keys()
            diag_list = list(diag_list)
            par_dia = sentence.values()
            par_dia = list(par_dia)
            f = diag_list[0]+"###"+par_dia[0][0]+"###"+par_dia[0][1]
            # scene_dict['DL'+ str(dialogue_counter)] = f   
            temp = {} 
            temp['sentence'] = diag_list[0]          # speaker
            temp['scene_no'] = scene_no
            temp['type'] = 'DL_SPEAKER'
            temp['phrases'] = []
            temp['type_no'] = ''  #dialogue counter in the particular scene
            temp['sentence_no'] = 0
            temp['paragraph_no'] = 0
            temp['importance'] = 0
            temp['final_importance'] = 0
            temp['zero_one'] = '1'
            sentences.append(temp)
            parentheticals = par_dia[0][0].split(" ")            
            if parentheticals[0] != 'NONE':
                temp={}
                temp['sentence'] = " ".join(parentheticals)
                temp['scene_no'] = scene_no
                temp['type'] = 'DL_PARENTH'
                temp['type_no'] = ''
                temp['phrases'] = []
                temp['sentence_no_in_scene'] = 0
                temp['paragraph_no'] = 0
                temp['importance'] = 0
                temp['final_importance'] = 0
                temp['zero_one'] = '1'
                sentences.append(temp)
            
            dialogues = par_dia[0][1].split(" ")         # dialogues
            sent_text = (par_dia[0][1]).split(".")
            temp = {}
            temp['sentence'] = " ".join(dialogues)
            temp['scene_no'] = scene_no
            temp['type'] = 'DL_DELIVERY'
            temp['type_no'] = ''
            temp['phrases'] = []
            temp['sentence_no_in_scene'] = 0
            temp['paragraph_no'] = 0
            temp['importance'] = 0
            temp['final_importance'] = 0
            temp['zero_one'] = '1'
            sentences.append(temp)   
    scene_no = scene_no +1

# scenes list
scenes_list = []
val = 1
scene_no = 0   
for scene in scenes:
    if scene_no == 0:
        scene_no = scene_no+1
        continue
    paragraph_no = 0
    temp = {}
    temp['scene_no'] = scene_no
    for line in scene:
        if type(line) == type(""):                        
            if line.startswith('INT') or line.startswith('EXT') or line.startswith('EXT/INT') or line.startswith('INT/EXT'):
                temp['slug line'] = line
            else: 
                paragraph_no += 1     #AC
        else:
            pass
    temp['importance'] = val
    scenes_list.append(temp)
    scene_no = scene_no+1
    val += 1

# character importanc will be used mainly with dialogues
characters_importance = []  
for character in characters:
    temp = {}
    temp['character'] = character
    temp['importance'] = character_importance(character)
    temp['relative_importance'] = 0
    characters_importance.append(temp)

# # sort character importance
characters_importance = sorted(characters_importance, key = lambda k: k['importance'])

val = 1
for char in characters_importance:
    ch = char['character']
for character_dict in characters_importance:
    if character_dict['character'].lower() == ch.lower():
        val -= 1 
        character_dict['relative_importance'] += val    
        ch = character_dict['character']
    else: 
        character_dict['relative_importance'] += val 
        ch = character_dict['character']
    val += 1 

# relative importance of a phrase in the script
# find phrases
for each_sentence in sentences:
    if each_sentence['type'] == 'AC':
        find_phrases(each_sentence['sentence'], each_sentence['scene_no'], each_sentence['sentence_no_in_scene'], each_sentence['type'], each_sentence['paragraph_no'])

# assign inherent importance to phrases
VP = 5
NP = 4
for each_phrase in phrases:
    if each_phrase['type'] == 'AC':
        if each_phrase['phrase_type'] == 'VP': 
            each_phrase['importance'] = each_phrase['importance'] * VP
        elif each_phrase['phrase_type']== 'NP':
            each_phrase['importance'] = each_phrase['importance'] * NP  
        else:
            each_phrase['importance'] = each_phrase['importance'] * 2

# # # importance of sentence in paragraph 
for each_sentence in sentences:
    if each_sentence['type'] == 'AC':
        for each_dict in each_sentence['phrases']:
            phrase = each_dict['phrase']
            set_importance(phrase, each_sentence['sentence_no_in_scene'], each_sentence['scene_no'], each_sentence['importance'])

# Note: we are updating importance of phrases in the phrases list, not in the sentences list

# relative importance of paragraph in scene and scene in script 
for each_phrase in phrases:
    if each_phrase['type'] == 'AC':
        each_phrase['importance'] = each_phrase['importance'] * each_phrase['paragraph_no'] * each_phrase['scene_no']

# add relative importance of characters in the phrases
# eg: if phrase == 'KUSH':
#        phrase['importance'] = phrase['importance'] * ( relative importance of KUSH )
for each_phrase in phrases:
    if each_phrase['type'] == 'AC':
        ph = each_phrase['phrase'].upper()
        if ph.strip(' ') in characters:
            for ch in characters_importance:
                if ch['character'] == ph.strip(' '):
                    importance = ch['relative_importance']
                    set_importance1(ph, each_phrase['sentence_no_in_scene'], each_phrase['scene_no'], importance)

# calculating sentence importance by adding the importance of the phrases in it
# Eg: sentence['importance'] = phrase1 + phrase2 + phrase3...
for each_sentence in sentences:
    if each_sentence['type'] == 'AC':
        sentence = each_sentence['sentence']
        for each_dict in each_sentence['phrases']:
            ph = each_dict['phrase']
            imp = set_importance2(ph, each_sentence['scene_no'], each_sentence['sentence_no_in_scene'])
            each_sentence['final_importance'] += imp
