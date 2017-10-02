#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import unicodedata
reload(sys)
sys.setdefaultencoding('utf-8')

import MeCab
### Constants
MECAB_MODE = 'mecabrc'
PARSE_TEXT_ENCODING = 'utf-8'
mecab = MeCab.Tagger('-Ochasen')

### Functions
def main():
    dataname="data_mecab"
    methodname="baseline"

    categoly=1
    file_name=0 #学習用のファイル名
    storyNum=4
    vector_file_name=0; #ベクトルファイル名
    while categoly<=1:
        while file_name<storyNum:
            print file_name
            ##ラベル付け
            names = { file_name : 1,
                      file_name+storyNum : -1
                      }

            allfile = './'+dataname+'/'+methodname+'/sum.txt'
            vector_file = './'+dataname+'/'+methodname+'/vector/' + str(vector_file_name) + '.txt'#学習用ベクトルファイル
            vector2_file = './'+dataname+'/'+methodname+'/vector2/' + str(vector_file_name) + '.txt'#評価用ベクトルファイル
            vector = open(vector_file, 'w') # 書き込みモードで開く
            vector2 = open(vector2_file, 'w') # 書き込みモードで開く

            data = open( allfile ).read()
            node = mecab.parseToNode( data )
            words = {}
            num = 0;
            phrases = node.next
            while phrases:
                try:
                    ustr=unicode(str(node.surface))
                    unicodedata.normalize( 'NFKC', ustr)
                    ustrlow=ustr.lower()
                    words_dict = parse(ustrlow)
                    """
                    if num==0:
                        k = "".join(words_dict['all'])
                    if words_dict['nouns']:
                        k = "".join(words_dict['nouns'])
                    elif words_dict['verbs']:
                        k = "".join(words_dict['verbs'])
                    elif words_dict['adjs']:
                        k = "".join(words_dict['adjs'])
                    elif words_dict['adve']:
                        k = "".join(words_dict['adve'])
                    elif words_dict['rentai']:
                        k = "".join(words_dict['rentai'])
                    else:
                        pass
                    """

                    k = "".join(words_dict['all'])
                    #文字列から文字を除去
                    k = k.strip().rstrip()
                    #初めて出てきた単語に番号を振り分ける
                    if k in words:
                        pass
                    else:
                        #words[k] = k
                        words[k] = num
                        num = num + 1
                    node = node.next
                except AttributeError:
                    break

            #学習用のベクトル
            print '学習用ファイル名　'+str(file_name)+'  ベクトルファイルの番号 '+str(vector_file_name)
            for i in names.keys():
                file_learn = './'+dataname+'/'+methodname+'/learn/' + str(i) + '.txt'
                print file_learn
                for line in open( file_learn, 'r' ):
                    line = line.strip().rstrip()
                    #vector.write(str(line+"\n"))
                    n = mecab.parseToNode( line )
                    attrs = {}
                    p = n.next
                    while p:
                        try:
                            ustr=unicode(str(p.surface))
                            unicodedata.normalize('NFKC', ustr)
                            ustrlow=ustr.lower()
                            words_dict = parse(ustrlow)
                            """
                            non=0
                            if words_dict['nouns']:
                                k = "".join(words_dict['nouns'])
                            elif words_dict['verbs']:
                                k = "".join(words_dict['verbs'])
                            elif words_dict['adjs']:
                                k = "".join(words_dict['adjs'])
                            elif words_dict['adve']:
                                k = "".join(words_dict['adve'])
                            elif words_dict['rentai']:
                                k = "".join(words_dict['rentai'])
                            else:
                                non=1
                            """

                            k = "".join(words_dict['all'])
                            #指定した形態素があった場合
                            #if non==0:
                            if k not in words:
                                break
                            id = words[k] #get()でKeyCodeError（例外）の発生を防ぐ
                            if id in attrs:
                                attrs[id] = attrs[id] + 1
                            else:
                                attrs[id] = 1
                            p = p.next
                            #else:
                                #p = p.next
                        except AttributeError:
                            break

                    #print names[i],
                    if len(attrs.keys())!=0:
                        vector.write(str(names[i])+" "),
                        for ak in sorted( attrs.keys() ):
                            if str(ak)!="":
                                #print str(ak)+":"+str(attrs[ak]),
                                vector.write(str(ak) + ":" + str(attrs[ak])+" "),  # 引数の文字列をファイルに書き込む
                        #print ""
                        vector.write('\n') #ファイルに改行を挿入する
            vector.close() # ファイルを閉じる

            #評価用のベクトル
            for i in names.keys():
                file_eval = './'+dataname+'/'+methodname+'/eval/' + str(i) + '.txt'
                print file_eval
                for line in open( file_eval, 'r' ):
                    line = line.strip().rstrip()
                    n = mecab.parseToNode( line )
                    attrs = {}
                    p = n.next
                    while p:
                        try:
                            ustr=unicode(str(p.surface))
                            unicodedata.normalize( 'NFKC', ustr)
                            ustrlow=ustr.lower()
                            words_dict = parse(ustrlow)
                            """
                            non=0
                            if words_dict['nouns']:
                                k = "".join(words_dict['nouns'])
                            elif words_dict['verbs']:
                                k = "".join(words_dict['verbs'])
                            elif words_dict['adjs']:
                                k = "".join(words_dict['adjs'])
                            elif words_dict['adve']:
                                k = "".join(words_dict['adve'])
                            elif words_dict['rentai']:
                                k = "".join(words_dict['rentai'])
                            else:
                                non=1
                            """
                            k = "".join(words_dict['all'])
                            #指定した形態素があった場合
                            #if non==0:
                            if k not in words:
                                break
                            id = words[k] #get()でKeyCodeError（例外）の発生を防ぐ
                            if id in attrs:
                                attrs[id] = attrs[id] + 1
                            else:
                                attrs[id] = 1
                            p = p.next
                            #else:
                                #p = p.next
                        except AttributeError:
                            break

                    #print names[i],
                    if len(attrs.keys())!=0:
                        vector2.write(str( names[i])+" "),
                        for ak in sorted( attrs.keys() ):
                            if str(ak)!="":
                                #print str(ak)+":"+str(attrs[ak]),
                                vector2.write(str(ak) + ":" + str(attrs[ak])+" "),  # 引数の文字列をファイルに書き込む
                        #print
                        vector2.write('\n') #ファイルに改行を挿入する
            vector2.close() # ファイルを閉じる

            #次のファイルへ
            file_name+=1;
            vector_file_name+=1;

        categoly+=1; #次のカテゴリへ
        file_name=1; #ファイル名を1からに戻す

def parse(unicode_string):
    tagger = MeCab.Tagger(MECAB_MODE)
    # str 型じゃないと動作がおかしくなるので str 型に変換
    text_p = unicode_string.encode(PARSE_TEXT_ENCODING)
    node_p = tagger.parseToNode(text_p)

    words_p = []
    nouns_p = []
    verbs_p = []
    adjs_p = []
    adve_p = []
    rentai_p = []
    while node_p:
        pos = node_p.feature.split(",")[0]
        # unicode 型に戻す
        word = node_p.feature.split(",")[6].decode("utf-8")
        """
        if pos == "名詞":
            nouns_p.append(node_p.surface)
        elif pos == "動詞":
            verbs_p.append(word)
        elif pos == "形容詞":
            adjs_p.append(word)
        elif pos == "副詞":
             adve_p.append(word)
        elif pos == "連体詞":
            rentai_p.append(word)
        else:
            pass
        """

        if pos == "名詞":
            words_p.append(node_p.surface)
        else:
            if word!="*":
                words_p.append(word)

        node_p = node_p.next

    parsed_words_dict = {
        "all": words_p # 最初と最後には空文字列が入るので除去
    }
    """
    parsed_words_dict = {
        "all": words_p[1:-1], # 最初と最後には空文字列が入るので除去
        "nouns": nouns_p,
        "verbs": verbs_p,
        "adjs": adjs_p,
        "adve": adve_p,
        "rentai": rentai_p
        }
    """
    return parsed_words_dict
### Execute
if __name__ == "__main__":
    main()