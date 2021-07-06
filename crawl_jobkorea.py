## 잡코리아에 부담을 주지 않기 위해 병렬처리를 하지 않기 위해 간단히 python 으로 작성합니다.
import time, os
import requests
import pandas as pd
from tqdm import tqdm
from lxml import html

if __name__ == '__main__':
    if not os.path.exists('data'): # create data dir
        os.makedirs('data')
    df = pd.read_csv('data/data.csv')
    """
    || 회사명 || 제목(신입, 인턴 등 뽑기 위함)|| 전문가가 본 자소서 평점|| 지원자 스펙 || 자소서 텍스트 || 자소서 total advice || 자소서 각 문단 advice ||
    """
    result_df = pd.DataFrame(columns=['company', 'title','score','spec','text','advice_total','advice_detail'])

    for idx, row in tqdm(df.iterrows()):
        try:
            source_id = row['source_id']
            url = 'https://www.jobkorea.co.kr/starter/passassay/view/{}'.format(source_id)
            res = requests.get(url)
            if res.status_code!=200:
                print(source_id, url)
                break

            root = html.fromstring(res.text)

            data = {
                'company': [i.text_content() for i in root.xpath('//div[@class="viewTitWrap"]/h2[@class="hd"]/strong/a[@target="_blank"]')][0],
                'title':[i.text_content() for i in root.xpath('//div[@class="viewTitWrap"]/h2[@class="hd"]/em')][0],
                'score': [i.text_content().strip() for i in root.xpath('//div[@class="adviceTotal"]/div[@class="hd"]/span[@class="grade"]')][0],
                'spec': [i.text_content().strip() for i in root.xpath('//ul[@class="specLists"]/li')][:-1],
                'text': [i.text_content().strip() for i in root.xpath('//dl[@class="qnaLists"]/dd[@class="show"]/div[@class="tx"]')],
                'advice_total':[i.text_content().strip() for i in root.xpath('//div[@class="adviceTotal"]/p[@class="tx"]')],
                'advice_detail':[i.text_content().strip() for i in root.xpath('//div[@class="advice"]/p')]

            }
            result_df = result_df.append(data, ignore_index=True)
        except Exception:
            # 데이터 존재하지 않을때
            print('skip source id {}'.format(source_id))
        time.sleep(0.4)
    


    result_df.to_csv('data/jobkorea.csv', index=False)      
    print('Done \n data length : {}'.format(len(result_df)))