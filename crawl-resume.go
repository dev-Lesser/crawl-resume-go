package main

import (
	"bufio"
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"sort"
)

const (
	MAX_PAGE        = 458
	RESUME_BASE_URL = "https://jasoseol.com/example_resume/list.json" // 자소설 사이트의 데이터를 가져옴
)

var headers = []string{
	"id",
	"source_id",
	"category_id",
	"apply_time",
	"company",
	"duty",
	"school",
	"major",
	"score",
	"foreign_score",
	"activity",
	"scrap",
	"status",
	"created_at",
	"updated_at",
}

type Query struct {
	// json 특성상 뒤쪽에 변수 실제명이 필요함
	Num  int `json:"num"`  // 15개
	Page int `json:"page"` // 페이지 번호
}

func main() {
	file, err := os.Create("./data/data.csv") // 저장 파일 설정
	if err != nil {
		panic(err)
	}
	wr := csv.NewWriter(bufio.NewWriter(file))
	defer wr.Flush()
	sort.Strings(headers) // header 설정 및 소팅
	wr.Write(headers)

	for i := 1; i < MAX_PAGE; i++ {
		fmt.Println("process page\t", i)
		query := Query{15, i}

		queryBytes, _ := json.Marshal(query)
		buff := bytes.NewBuffer(queryBytes)
		req, err := http.NewRequest("POST", RESUME_BASE_URL, buff)
		if err != nil {
			panic(err)
		}
		req.Header.Add("Content-Type", "application/json")
		client := &http.Client{}
		response, err := client.Do(req)
		if err != nil {
			panic(err)
		}

		defer response.Body.Close()

		body, _ := ioutil.ReadAll(response.Body)

		data := make(map[string]interface{}) // 결과값 json 파싱
		json.Unmarshal(body, &data)
		res := data["example_resumes"] // resume 만 있는 interface 저장

		// csv writer 생성
		for _, element := range res.([]interface{}) {
			s := []string{}
			keys := make([]string, 0, len(headers))
			for k := range element.(map[string]interface{}) {
				keys = append(keys, k)
			}
			sort.Strings(keys)
			for _, k := range keys { // key 별로 순회
				value := element.(map[string]interface{})[k]
				str := fmt.Sprintf("%v", value)
				if value == nil {
					str = ""
				}
				s = append(s, str)

			}
			wr.Write(s)
		}

	}
	wr.Flush()

}
