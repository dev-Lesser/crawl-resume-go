package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

const (
	MAX_PAGE        = 458
	RESUME_BASE_URL = "https://jasoseol.com/example_resume/list.json" // 자소설 사이트의 데이터를 가져옴
)

type Query struct {
	Keyword string // 빈 문자열
	Num     string // 15개
	Page    string // 페이지 번호
}
type Person struct {
	Name string
	Age  int
}

func main() {
	query := Query{"", "15", "1"}

	queryBytes, _ := json.Marshal(query)
	buff := bytes.NewBuffer(queryBytes)
	fmt.Println(RESUME_BASE_URL)
	response, err := http.Post(RESUME_BASE_URL, "application/json", buff)

	if err != nil {
		panic(err)
	}
	defer response.Body.Close()

	// Response 체크.
	fmt.Println("response Status:", response.Status)
	fmt.Println("response Headers:", response.Header)
	body, _ := ioutil.ReadAll(response.Body)
	if err == nil {
		fmt.Println("response Body:", string(body))
	}
	// person := Person{"Alex", 10}
	// pbytes, _ := json.Marshal(person)
	// buff := bytes.NewBuffer(pbytes)
	// resp, err := http.Post("http://httpbin.org/post", "application/json", buff)
	// if err != nil {
	// 	panic(err)
	// }

	// defer resp.Body.Close()

	// // Response 체크.
	// respBody, err := ioutil.ReadAll(resp.Body)
	// if err == nil {
	// 	str := string(respBody)
	// 	println(str)
	// }
}
