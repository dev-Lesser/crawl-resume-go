import pandas as pd
import ast
import matplotlib.pyplot as plt
import numpy as np

def point_ratio(d):
        d = d['point']
        if d == None:
            return None
        return float(d.split('/')[0])/float(d.split('/')[1])

def create_spec_split(d):
    
    spec= d['spec']
    spec = ast.literal_eval(spec)
    univ, degree, point, toeic, toeic_speaking, opic, cert_num, act_school,     act_society, act_volunteer, act_oversea, act_intern, act_prize, act_club, lang = [None for i in range(15)]
    for item in spec:
        if item.endswith('년') or item in ["고졸","초대졸", "대학원"]:
            univ = item
        elif item.startswith('학점'):
            r = item.split()[-1]
            point = r
        elif item.startswith('토익'):
            r = item.split()[-1]
            toeic = int(r)
        elif item.startswith('토스'):
            r = item.split()[-1].replace('Level','')
            toeic_speaking = r
        elif item.startswith('오픽'):
            r = item.split()[-1]
            opic = r
        elif item.startswith('자격증'):
            r = item.split()[-1].replace('개','')
            cert_num = int(r)
        elif item.startswith('교내활동'):
            r = item.split()[-1].replace('회','')
            act_school = int(r)
        elif item.startswith('사회활동'):
            r = item.split()[-1].replace('회','')
            act_society = int(r)
        elif item.startswith('자원봉사'):
            r = item.split()[-1].replace('회','')
            act_volunteer = int(r)
        elif item.startswith('해외경험'):
            r = item.split()[-1].replace('회','')
            act_oversea = int(r)
        elif item.startswith('인턴'):
            r = item.split()[-1].replace('회','')
            act_intern = int(r)
        elif item.startswith('수상'):
            r = item.split()[-1].replace('회','')
            act_prize = int(r)
        elif item.startswith('동아리'):
            r = item.split()[-1].replace('회','')
            act_club = int(r)
        elif item.startswith('제2외국어'):
            r = item.split()[-1].replace('개','')
            act_lang = int(r)
        else:
            degree = item
    return pd.Series((univ, degree, point, toeic, toeic_speaking, opic, cert_num, act_school, 
            act_society, act_volunteer, act_oversea, act_intern, act_prize, act_club, lang ))

if __name__=="__main__":
    df = pd.read_csv('data/jobkorea.csv')

    df[['univ', 'degree', 'point', 'toeic', 'toeic_speaking', 
        'opic', 'cert_num', 'act_school', 
        'act_society', 'act_volunteer', 'act_oversea', 
        'act_intern', 'act_prize', 'act_club', 'lang' ]] = df.apply(create_spec_split, axis=1)

    
    plt.rc('font', family='AppleGothic')

    # cralw 데이터 기업별 개수 그래프 저장
    df['company'].value_counts().iloc[:10].plot.bar(figsize=(15,9))
    plt.savefig('data/resume_num_1_10.png')
    df['company'].value_counts().iloc[10:20].plot.bar(figsize=(15,9))
    plt.savefig('data/resume_num_11_20.png')


    result = []
    for idx, row in df[['title']].iterrows():
        d =row['title'].split() # 년도, 상/하반기, 신입/인턴, 직무
        result.append({'year': d[0], 'half': d[1], 'class': d[2], 'task': d[3]})


    df_class = pd.DataFrame(result)

    df_class_new = pd.DataFrame()
    for i in range(0,len(df_class['task'].unique()),10):
        tmp = pd.DataFrame(sorted(df_class['task'].unique())[i:i+10])
        df_class_new = pd.concat([df_class_new, tmp], axis=1, ignore_index=True)

    task_list = sorted(df_class['task'].unique())
    task_num = []
    for task in task_list:
        task_num.append(len(df_class[df_class['task']==task]))


    
    task_num = np.array(task_num)
    fig, ax = plt.subplots(figsize=(15,15))

    a = np.pad(task_num, (0,9), 'constant', constant_values=0).reshape(10,10).T
    im = ax.imshow(a)

    for i in range(10):
        for j in range(10):
            text = ax.text(j,i, df_class_new.iloc[i][j],ha="center", va="center", color="w")

    plt.savefig('data/task_class_num.png')

    df = pd.concat([df, df_class], axis=1)

    df = df.drop(columns=['title','spec'])

    df['point_ratio'] = df.apply(point_ratio, axis=1)

    df.to_csv('data/analysis.csv', index=False)





