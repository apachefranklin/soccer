from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,reverse
import string, random
import unidecode
import os

class Utility:
    @classmethod
    def get_random_string(cls,length=15):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
    
    @classmethod
    def url_stringify(cls,string_pattern,sep="-"):
        """Function who take a string and transform it to url 
        String by removing all special character, remove all space,
        and replace thems by a -"""
        final_str=unidecode.unidecode(string_pattern)
        final_str=final_str.strip()
        final_str=final_str.replace('\s+',' ')
        final_str=final_str.replace(" ",sep)
        #print(final_str)
        #print(string_pattern)
        return final_str
    
    @classmethod
    def remove_accent(cls,chre):
        """remove all accent characters from a chre string"""
        return unidecode.unidecode(chre)
    
    @classmethod
    def is_null_or_empty(cls,chaine,null_function=''):
        """Function who find is value is null or empty. white space are removed
        you can pass your own function who test is value is null with param
            @null_function, for example null_function=is_none """
        if(null_function==''):
            if chaine is None:
                return True
        else:
            if(null_function(chaine)):
                return True
        try:
            if(chaine.strip()==""):
                return True
        except Exception as e:
            return False

            

