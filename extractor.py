import re
from itertools import groupby
import jieba
import jieba.posseg as pseg

import logging
jieba.setLogLevel(logging.INFO)

class extractor():
    def __init__(self):
        pass

    def extract_email(self, text):
        if text=='':
            return []
        eng_texts = self.replace_chinese(text)
        eng_texts = eng_texts.replace(' at ','@').replace(' dot ','.')
        sep = ',!?:; ，。！？《》、|\\/'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]

        email_pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z_-]+)+$'

        emails = []
        for eng_text in eng_split_texts:
            result = re.match(email_pattern, eng_text, flags=0)
            if result:
                emails.append(result.string)
        return emails


    def replace_chinese(self, text):
        if text=='':
            return []
        filtrate = re.compile(u'[\u4E00-\u9FA5]')
        text_without_chinese = filtrate.sub(r' ', text)
        return text_without_chinese

    def replace_ids(self, text):
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
        eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) == 18]

        id_pattern = r'^[1-9][0-7]\d{4}((19\d{2}(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(19\d{2}(0[13578]|1[02])31)|(19\d{2}02(0[1-9]|1\d|2[0-8]))|(19([13579][26]|[2468][048]|0[48])0229))\d{3}(\d|X|x)?$'
        ids = []
        for eng_text in eng_split_texts_clean:
            result = re.match(id_pattern, eng_text, flags=0)
            if result:
                ids.append(result.string)

        for phone_num in ids:
            text = text.replace(phone_num,'')
        return text


    def extract_name(self, text):
        if text=='':
            return []
        seg_list = [(str(t.word), str(t.flag)) for t in pseg.cut(text)]
        names = []
        for ele_tup in seg_list:
            if 'nr' in ele_tup[1]:
                names.append(ele_tup[0])
        return self.most_common(names)

    def most_common(self, content_list):
        if content_list==[]:
            return None
        if len(content_list)==0:
            return None
        return max(set(content_list), key=content_list.count)
