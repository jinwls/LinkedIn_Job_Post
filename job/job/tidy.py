from sre_parse import State
import pandas as pd 
import numpy as np
import string
import re 
import time 
import unidecode 
import nltk 
from nltk.corpus import stopwords 
nltk.download('stopwords') 
from nltk.tokenize import word_tokenize 

# dictionary map
us_state_to_abbrev = {
    "alabama": "al",
    "alaska": "ak",
    "arizona": "az",
    "arkansas": "ar",
    "california": "ca",
    "colorado": "co",
    "connecticut": "ct",
    "delaware": "de",
    "florida": "fl",
    "georgia": "ga",
    "hawaii": "hi",
    "idaho": "id",
    "illinois": "il",
    "indiana": "in",
    "iowa": "ia",
    "kansas": "ks",
    "kentucky": "ky",
    "louisiana": "la",
    "maine": "me",
    "maryland": "md",
    "massachusetts": "ma",
    "michigan": "mi",
    "minnesota": "mn",
    "mississippi": "ms",
    "missouri": "mo",
    "montana": "mt",
    "nebraska": "ne",
    "nevada": "nv",
    "new hampshire": "nh",
    "new jersey": "nj",
    "new mexico": "nm",
    "new york": "ny",
    "north carolina": "nc",
    "north dakota": "nd",
    "ohio": "oh",
    "oklahoma": "ok",
    "oregon": "or",
    "pennsylvania": "pa",
    "rhode island": "ri",
    "south carolina": "sc",
    "south dakota": "sd",
    "tennessee": "tn",
    "texas": "tx",
    "utah": "ut",
    "vermont": "vt",
    "virginia": "va",
    "washington": "wa",
    "west virginia": "wv",
    "wisconsin": "wi",
    "wyoming": "wy",
    "district of columbia": "dc",
    "american samoa": "as",
    "guam": "gu",
    "northern mariana islands": "mp",
    "puerto rico": "pr",
    "united States minor outlying islands": "um",
    "virgin islands": "VI",
}

contraction_map = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have",
}


def lower_case(value):
    return value.lower()


def remove_newlines(text):
    Newlines_removed = text.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ').replace('. com', '.com')
    return Newlines_removed


def remove_whitespace(text):
    # For cases where there are no space after ? ()
    text = text.replace('?', ' ? ').replace(')', ' ) ').replace('(', ' ( ')
    Whitespace_removed = text.strip()
    return Whitespace_removed


def remove_special(text):
    Special_removed = re.sub(r"[^a-zA-Z0-9:$-,%.?!]+", ' ', text)
    return Special_removed


def remove_accented(text):
    # example: àéêö
    Accented_removed = unidecode.unidecode(text)
    return Accented_removed


def remove_repeat(text):
    pattern = re.compile(r'([A-za-z])\1{1,}', re.DOTALL)
    ALpha_repeatation = pattern.sub(r'\1\1', text)
    Repeatation_removed = re.sub(' {2,}',' ', ALpha_repeatation)
    return Repeatation_removed




## tidy classes for linkedin dataset
class StopwordRemove(object):
    
    def __call__(self, values):
        values = ' '.join(values)
        values = values.strip()
        Token_list = values.split(' ')
        stopword = stopwords.words('english')
        stopword = set(stopword)

        # check for contraction words
        for word in Token_list:
            if word in contraction_map:
                token = [item.replace(word, contraction_map[word]) for item in Token_list]
        # convert back to string
        values = ' '.join(str(word) for word in Token_list)
        
        # remove stopwords
        values = repr(values)
        Stopword_removed = [word for word in word_tokenize(values) if word not in stopword]
        Stopword_removed = ' '.join(Stopword_removed)
        Stopword_removed = Stopword_removed.replace("'",'').replace("'",'')
        return Stopword_removed


class TakeJob(object):

    def __call__(self, values):
        values = str(values)
        pattern_engineer = re.compile(r'(?=.*data)(?=.*engineer)')
        pattern_analyst = re.compile(r'(?=.*data)(?=.*analyst)')
        pattern_scientist = re.compile(r'(?=.*data)(?=.*(scientist|science))')
        pattern_specialist = re.compile(r'(?=.*data)(?=.*specialist)')
        if pattern_engineer.search(values):
            Job_extracted = 'data engineer'
        elif pattern_analyst.search(values):
            Job_extracted = 'data analyst'
        elif pattern_scientist.search(values):
            Job_extracted = 'data scientist'
        elif pattern_specialist.search(values):
            Job_extracted = 'data specialist'
        else:
            Job_extracted = 'None'
        return Job_extracted


# The value may contain 1 or 2 value (['location', 'applicant number'])
# also, there are two info in location, (city, state) or (state, country) 
class TakeLocation(object):
    
    def __call__(self, values):
        if len(values) == 2:
            self.values = values[0]
        else:
            self.values = values

    def take_city(self, values):
        values = values[0].split(',')
        if len(values) == 1:
            City_extracted = 'None'
        else:    
            City_extracted = str(np.where('united states' in values[1], 'None', values[0]))
        return City_extracted
    
    def take_states(self, values):
        values = values[0].split(',')
        states = us_state_to_abbrev
        if len(values) == 1:
            State_extracted = str(np.where('united states' in values[0], 'None', values[0]))
        else:
            State_extracted = str(np.where('united states' in values[1], values[0], values[1]))

        if State_extracted == 'None':
            return 'None'
        else:
            State_extracted_abbrev = states.get(State_extracted, State_extracted)
            return State_extracted_abbrev


# there are 4 categories in job criteria section (seniority level, employment type, job function, industries)
# there are some company with only employment type information 
class TakeOther(object):

    def __call__(self, values):
        self.values = values

    def take_level(self, values):
        if len(values) >= 4:
            Level_extracted = values[0]
        else: 
            Level_extracted = 'None'
        return Level_extracted

    def take_type(self, values):
        if len(values) >= 4:
            Type_extracted = values[1]
        else: 
            Type_extracted = values[0]
        return Type_extracted

    def take_function(self, values):
        if len(values) >= 4:
            Function_extracted = values[2]
        else: 
            Function_extracted = 'None'
        return Function_extracted

    def take_industry(self, values):
        if len(values) >= 4:
            Industry_extracted = values[3]
        else: 
            Industry_extracted = 'None'
        return Industry_extracted
