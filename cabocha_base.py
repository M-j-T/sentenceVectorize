#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import unicodedata
reload(sys)
sys.setdefaultencoding('utf-8')

import CaboCha
c = CaboCha.Parser()

### Functions
def main():
    dataname="data_cabocha"
    methodname="baseline"

    file_name=0 #学習用のファイル名
    storyNum=4 #作品数
    vector_file_name=0 #ベクトルファイル名

    while file_name<storyNum:
        print file_name
        ##ラベル付け
        names = { file_name : 1,
                  file_name+storyNum : -1
                  }

        allfile = open('./'+dataname+'/'+methodname+ '/sum.txt')
        vector_file = open('./'+dataname+'/'+methodname+'/vector/' + str(vector_file_name) + '.txt','w')
        vector2_file = open('./'+dataname+'/'+methodname+'/vector2/' + str(vector_file_name) + '.txt','w')
        data = allfile.readline()

        words = {}
        num = 0;
        count=0;

        #phraseListに係り受け解析した語を入れる
        while data:
            tree =  c.parse(data)##関係性を取得
            phraseList=[] ##元の文節
            linkList=[] ##係受け先の文節

            k=normalize(data) #正規化などの処理をした文字列を返す
            phraseList.extend(k.split(","))##,で区切ってリストに格納

            linkList=re.findall("link=\"(.+?)\"",str(tree.toString(CaboCha.FORMAT_XML)))

            for i in range(len(linkList)):
                if linkList[i] in words:
                    pass #重複しているときは入れない
                else:
                    if len(phraseList[i])>0:
                        words[phraseList[i]] = phraseList[i]
                        #words[phraseList[i]] = num
                        num = num + 1
                        if not int(linkList[i])==-1:
                            words[phraseList[i]+""+phraseList[int(linkList[i])]] = phraseList[i]+""+phraseList[int(linkList[i])]
                            #words[phraseList[i]+""+phraseList[int(linkList[i])]] = num
                            num = num + 1

            data=allfile.readline()

        #学習用のベクトル
        #print '学習用ファイル名　'+str(file_name)+'  ベクトルファイルの番号 '+str(vector_file_name)
        for i in names.keys():
            file_learn = open('./'+dataname+'/'+methodname+'/learn/' + str(i) + '.txt')
            data2=file_learn.readline()

            while data2:
                tree =  c.parse(data2)##関係性を取得
                attrs = {}
                phraseList=[] ##文節リストを作成
                linkList=[]

                k=normalize(data2) #正規化などの処理をした文字列を返す
                phraseList.extend(k.split(","))##,で区切ってリストに格納

                linkList=re.findall("link=\"(.+?)\"",str(tree.toString(CaboCha.FORMAT_XML)))

                data2=file_learn.readline()

                print
                for j in range(len(linkList)):

                    if len(phraseList[j])>0:
                        if phraseList[j] not in words or phraseList[j]+""+phraseList[int(linkList[j])] not in words:
                            break

                        print phraseList[j]
                        id = words[phraseList[j]] #get()でKeyCodeError（例外）の発生を防ぐ
                        if id in attrs:
                            attrs[id] = attrs[id] + 1
                        else:
                            attrs[id] = 1

                        if not int(linkList[j])==-1:
                            print phraseList[j]+""+phraseList[int(linkList[j])]
                            id = words[phraseList[j]+""+phraseList[int(linkList[j])]] #get()でKeyCodeError（例外）の発生を防ぐ
                            if id in attrs:
                                attrs[id] = attrs[id] + 1
                            else:
                                attrs[id] = 1

                #print names[i],
                vector_file.write(str(names[i])+" "),
                for ak in sorted( attrs.keys() ):
                    #print str(ak)+":"+str(attrs[ak]),
                    vector_file.write(str(ak) + ":" + str(attrs[ak])+" "),  # 引数の文字列をファイルに書き込む
                #print
                vector_file.write('\n') #ファイルに改行を挿入する
        vector_file.close() # ファイルを閉じる

        #print

        #評価用のベクトル
        for i in names.keys():
            file_learn = open('./'+dataname+'/'+methodname+'/eval/' + str(i) + '.txt')
            data2=file_learn.readline()

            while data2:
                tree =  c.parse(data2)##関係性を取得
                attrs = {}
                phraseList=[] ##文節リストを作成
                linkList=[]

                k=normalize(data2) #正規化などの処理をした文字列を返す
                phraseList.extend(k.split(","))##,で区切ってリストに格納

                linkList=re.findall("link=\"(.+?)\"",str(tree.toString(CaboCha.FORMAT_XML)))

                data2=file_learn.readline()

                print
                for j in range(len(linkList)):

                    if len(phraseList[j])>0:
                        if phraseList[j] not in words or phraseList[j]+""+phraseList[int(linkList[j])] not in words:
                            break

                        print phraseList[j]
                        id = words[phraseList[j]] #get()でKeyCodeError（例外）の発生を防ぐ
                        if id in attrs:
                            attrs[id] = attrs[id] + 1
                        else:
                            attrs[id] = 1

                        if not int(linkList[j])==-1:
                            print phraseList[j]+""+phraseList[int(linkList[j])]
                            id = words[phraseList[j]+""+phraseList[int(linkList[j])]] #get()でKeyCodeError（例外）の発生を防ぐ
                            if id in attrs:
                                attrs[id] = attrs[id] + 1
                            else:
                                attrs[id] = 1

                #print names[i],
                vector2_file.write(str( names[i])+" "),
                for ak in sorted( attrs.keys() ):
                    #print str(ak)+":"+str(attrs[ak]),
                    vector2_file.write(str(ak) + ":" + str(attrs[ak])+" "),  # 引数の文字列をファイルに書き込む
                #print
                vector2_file.write('\n') #ファイルに改行を挿入する
        vector2_file.close() # ファイルを閉じる


        #次のファイルへ
        file_name+=1;
        vector_file_name+=1;

def normalize(data):
    norm = re.sub(r'-D|EOS| |-|\|', r'', str(c.parseToString(data)))
    norm = re.sub(r'\n', r',', norm)
    norm = re.sub(r',,', r',', norm)
    return norm

### Execute
if __name__ == "__main__":
    main()