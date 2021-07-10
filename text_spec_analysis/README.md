```python
import pandas as pd
```


```python
df = pd.read_csv('data/analysis.csv')
```


```python
import hgtk, os, re
from tqdm.notebook import tqdm
```


```python
import MeCab
import ast
mecab=MeCab.Tagger()
```


```python
def parse_text(text):
    bucket = []
    start = 0
    pattern = re.compile(".*\t[A-Z]+") 
    for token, pos in  [tuple(pattern.match(token).group(0).split("\t")) for token in mecab.parse(text).splitlines()[:-1]]:
        if start == 0:
            lspace = False
        elif text[start] == ' ':
            lspace = True
        else:
            lspace = False
        start = text.find(token, start)
        end = start + len(token)
        bucket.append((token, pos, lspace, start, end))
        start = end
    return bucket
def apply_noun_ext(df):
    total = ast.literal_eval(df['advice_total'])
    detail = ast.literal_eval(df['advice_detail'])
    text = ' '.join(total)+ ' '.join(detail)
    clean_text = re.sub('\[지원자\]', '', text)
    result = noun_ext(parse_text(clean_text))
    return result

def check_noun(cand):
    if len(re.findall('[^가-힣a-zA-Z0-9+]', cand)) > 0:
        return False
    else:
        return True
```


```python
def noun_ext(parsed_text):
    global stopwords
    global one_list
    noun_bucket = []
    bi_bucket = []
    tri_bucket = []
    last_last_add = None
    last_add = None
    last_lspace = None
    for ichunk in parsed_text:
        token = ichunk[0]
        pos = ichunk[1]
        lspace = ichunk[2]
        add = False
        if pos == 'NNG': 
            if check_noun(token) == True: 
                if token not in stopwords:
                    if len(token) > 1: 
                        add = True
                    elif token in one_list:
                        add = True
        if pos == 'NNP': 
            if token not in stopwords:
                if len(token) > 1:
                    add = True
                elif token in one_list:
                    add = True
                    
        if add == True:
            if (last_add == True) and (lspace == False) and (len(noun_bucket) > 0):
                bi_bucket.append('|'.join([noun_bucket[-1], token]))
            if (last_add == True) and (last_last_add == True) and (lspace == False) and \
            (last_lspace == False) and (len(noun_bucket) > 1):
                tri_bucket.append('|'.join([noun_bucket[-2], noun_bucket[-1], token]))
            noun_bucket.append(token)
        last_lspace = lspace
        last_last_add = last_add
        last_add = add
    return pd.Series((noun_bucket, bi_bucket, tri_bucket))
```


```python
one_list = list('젤펄물향색립손짱굳양톤물티밤코빛붓굿돈팩맥맛감웜집샵끈선속밖겉봄반광팁샷솔볼폼딥입펜발템갑값'
            '똥룩꿀떡존몸핏땀핫옆꽃액칠금쿨차밥병솜망폰링통옷목팔숱배살털컬홈짝뷰')
```


```python
tqdm.pandas()
```


```python
stopwords = ['전반','지원자','직무', '내용','부분','항목','회사','지원', '소개서','제시','관련','질문','작성']
df[['keywords','bigrams','trigrams']] = df[['advice_total','advice_detail']].fillna('').progress_apply(apply_noun_ext, axis=1)
```


      0%|          | 0/3434 [00:00<?, ?it/s]

df[['keywords','bigrams','trigrams']]

```python
from collections import Counter
task_list = ['사무·총무·법무','기획·전략·경영','응용프로그래머','전기·전자·제어','영업관리·지원·영업기획','생산관리·공정관리·품질관리']
word_df=pd.DataFrame()
for task in task_list:
    c = Counter()
    c_b = Counter()
    c_t = Counter()

    for i,row in df[(df['task']==task)].iterrows():
        keywords = row['keywords']
        c.update(keywords)

    word_df = pd.concat([word_df,pd.DataFrame(c.most_common(20))], axis=1)
```


```python
import matplotlib.pyplot as plt
%matplotlib inline
plt.rc('font', family='AppleGothic')
```


```python
df[(df['task']=='사무·총무·법무')][[
    'univ','degree','point_ratio','toeic','toeic_speaking','act_school', 
    'act_society', 'act_volunteer', 'act_oversea', 
    'act_intern', 'act_prize', 'act_club', 'lang']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>univ</th>
      <th>degree</th>
      <th>point_ratio</th>
      <th>toeic</th>
      <th>toeic_speaking</th>
      <th>act_school</th>
      <th>act_society</th>
      <th>act_volunteer</th>
      <th>act_oversea</th>
      <th>act_intern</th>
      <th>act_prize</th>
      <th>act_club</th>
      <th>lang</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>지방4년</td>
      <td>산업공학과</td>
      <td>0.744444</td>
      <td>810.0</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>26</th>
      <td>지방4년</td>
      <td>국제통상학과</td>
      <td>0.853333</td>
      <td>NaN</td>
      <td>6.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>32</th>
      <td>지방4년</td>
      <td>수학과</td>
      <td>0.755556</td>
      <td>730.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>37</th>
      <td>서울4년</td>
      <td>국제통상학전공</td>
      <td>0.753333</td>
      <td>NaN</td>
      <td>5.0</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>40</th>
      <td>서울4년</td>
      <td>영어영문학과</td>
      <td>0.913333</td>
      <td>950.0</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>3343</th>
      <td>고졸</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3368</th>
      <td>수도권4년</td>
      <td>법학과</td>
      <td>0.822222</td>
      <td>805.0</td>
      <td>6.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3378</th>
      <td>고졸</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3392</th>
      <td>지방4년</td>
      <td>경제통상학부</td>
      <td>0.866667</td>
      <td>930.0</td>
      <td>7.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3408</th>
      <td>서울4년</td>
      <td>마케팅학과</td>
      <td>0.711111</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>365 rows × 13 columns</p>
</div>



### 학생 전공별 자소서 분포 


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['degree'].value_counts()
    ax[row][col].pie(tmp, labels=tmp.index)
    ax[row][col].set(title=name, aspect='equal')

    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()
```


    
![png](output_14_0.png)
    


### 학점/학점총점 히스토그램


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['point_ratio'].dropna() #.plot.hist(bins=20, title="학점 비율")
    ax[row][col].hist(tmp,  bins=20, histtype='bar', fill=True)
    ax[row][col].set(title=name)

    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_16_0.png)
    


### 직군별 토익점수 히스토그램 


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['toeic'].dropna() #.plot.hist(bins=20, title="학점 비율")
    ax[row][col].hist(tmp,  bins=20, histtype='bar', fill=True)
    ax[row][col].set(title=name + '|개수 : ' + str(len(tmp)))

    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_18_0.png)
    


### 토익 스피킹 레벨별 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['toeic_speaking'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_20_0.png)
    


### 오픽 레벨별 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['opic'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_22_0.png)
    


### 자격증 개수 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['cert_num'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_24_0.png)
    


### 교내활동 개수 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['act_school'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_26_0.png)
    


### 사회활동 개수 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['act_society'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_28_0.png)
    


### 자원 봉사 횟수 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['act_volunteer'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_30_0.png)
    


### 해외경험 개수 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['act_oversea'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_32_0.png)
    


### 인턴경험 횟수 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['act_intern'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_34_0.png)
    


### 수상횟수 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['act_prize'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_36_0.png)
    


### 동아리 횟수 분포


```python
rows=2
cols=3
row=0
col=0
fig, ax = plt.subplots(rows, cols, figsize=(20,10))
names = ["사무·총무·법무","기획·전략·경영","응용프로그래머","전기·전자·제어","제품·서비스영업","영업관리·지원·영업기획"]
for name in names:
    tmp = df[(df['task']==name)]['act_club'].value_counts() 
    ax[row][col].bar(tmp.index, height = tmp)
    ax[row][col].set(title=name + '|개수 : ' + str(sum(tmp)) +' | 비율 : ' + str(round(
                                                            sum(tmp)/len(df[(df['task']==name)]),2)))
    row+=1
    if row==rows:
        row=0
        col+=1
fig.tight_layout()
plt.show()

```


    
![png](output_38_0.png)
    



```python

```
