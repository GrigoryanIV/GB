# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, TakeFirst

def clean_salary_Sujob(lst_in):
    stroka_in = " ".join(lst_in)
    stroka_out = [0,0,'RU','neto']
    if len(stroka_in) == 0 or stroka_in == 'По договорённости':
        print("нет данных !")
    else:
        stroka_in = stroka_in.replace(' ', '')
        stroka_in = stroka_in.replace('&nbsp;', '')
        if 'наруки' in stroka_in:
            stroka_out[3] = 'neto'
            stroka_in = stroka_in.replace('наруки', '')
        elif 'довычетаналогов' in stroka_in:
            stroka_out[3] = 'bruto'
            stroka_in = stroka_in.replace('довычетаналогов', '')
        if 'руб.' in stroka_in:
            stroka_out = [None, None, 'RU']
            stroka_in = stroka_in.replace('руб.', '')
        elif 'USD' in stroka_in:
            stroka_out = [None, None, 'USD']
            stroka_in = stroka_in.replace('USD', '')
        elif 'EUR' in stroka_in:
            stroka_out = [None, None, 'EUR']
            stroka_in = stroka_in.replace('EUR', '')
        if 'от' in stroka_in:
            stroka_out[0] = int(stroka_in[2:])
            stroka_out[1] = None
        elif 'до' in stroka_in:
            stroka_out[0] = None
            stroka_out[1] = int(stroka_in[2:])
        elif '/' in stroka_in:
            stroka_kort = stroka_in.split('/')
            stroka_out[0] = int(stroka_kort[0])
            stroka_out[1] = int(stroka_kort[1])
        else :
            stroka_out[0] = int(stroka_in)
            stroka_out[1] = int(stroka_in)

    str_out = 'min: ' + str(stroka_out[0]) + 'max: ' + str(stroka_out[1]) + 'val: ' + str(stroka_out[2]) + 'tip: ' +  str(stroka_out[3])
    return str_out

def clean_salary_HH(lst_in):
    stroka_in = " ".join(lst_in)
    stroka_out = [0, 0, 'RU', 'neto']
    if len(stroka_in) == 0 or stroka_in == 'з/п не указана:':
        print("нет данных !")
    else:
        stroka_in = stroka_in.replace(' ', '')
        stroka_in = stroka_in.replace('\u202f', '')
        if 'руб.' in stroka_in:
            stroka_out = [None, None, 'RU']
            stroka_in = stroka_in.replace('руб.', '')
        elif 'USD' in stroka_in:
            stroka_out = [None, None, 'USD']
            stroka_in = stroka_in.replace('USD', '')
        elif 'EUR' in stroka_in:
            stroka_out = [None, None, 'EUR']
            stroka_in = stroka_in.replace('EUR', '')
        if 'от' in stroka_in:
            stroka_out[0] = int(stroka_in[2:])
            stroka_out[1] = None
        elif 'до' in stroka_in:
            stroka_out[0] = None
            stroka_out[1] = int(stroka_in[2:])
    stroka_kort = stroka_in.split('–')
    stroka_out[0] = int(stroka_kort[0])
    stroka_out[1] = int(stroka_kort[1])
    if 'наруки' in stroka_in:
        stroka_out[3] = 'neto'
    elif 'довычетаналогов' in stroka_in:
        stroka_out[3] = 'bruto'
    str_out = 'min: ' + str(stroka_out[0]) + 'max: ' + str(stroka_out[1]) + 'val: ' + str(stroka_out[2]) + 'tip: ' +  str(stroka_out[3])
    return str_out

class ParserJobItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor = TakeFirst())
    salary = scrapy.Field(input_processor=Compose(clean_salary_HH), output_processor = TakeFirst())
    _id = scrapy.Field(output_processor = TakeFirst())

class ParserJobItem_2(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor = TakeFirst())
    salary = scrapy.Field(input_processor=Compose(clean_salary_Sujob), output_processor = TakeFirst())
    _id = scrapy.Field(output_processor = TakeFirst())

