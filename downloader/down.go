package main

import (
	"bufio"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

func Checkerr(err error) {
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func main() {

	fileUrl := "https://www.wis-jma.go.jp/data/syn?ContentType=Text&Category=&Type=Alphanumeric&Access=Open"

	if err := Polling_udpate_file("filelist.txt", fileUrl); err != nil {
		panic(err)
	}

	if err := Download_all("filelist.txt"); err != nil {
		os.Exit(1)
	}
}

func Polling_udpate_file(filepath string, url string) error {
	etag_filepath := "Etag.txt"
	req, err := Make_header(etag_filepath, url)
	Checkerr(err)

	client := new(http.Client)
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	etag_val := resp.Header.Values("Etag")[0]
	err = Save_etag("Etag.txt", etag_val)
	Checkerr(err)

	out, err := os.Create(filepath)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	return err
}

func Make_header(filepath string, url string) (req *http.Request, err error) {
	etag, err := os.ReadFile(filepath)
	Checkerr(err)
	etag_str := string(etag)
	req, err = http.NewRequest("GET", url, nil)
	req.Header.Set("If-None-Match", etag_str)

	return req, err
}

func Save_etag(filepath string, val string) error {
	out, err := os.Create(filepath)
	Checkerr(err)
	defer out.Close()

	_, err = out.WriteString(val)
	Checkerr(err)
	return err
}

func Download_all(filepath string) error {
	fp, err := os.Open(filepath)
	Checkerr(err)
	defer fp.Close()

	scanner := bufio.NewScanner(fp)
	cnt := 0

	for scanner.Scan() {
		fmt.Println(scanner.Text())
		Get_and_sava(scanner.Text())
		cnt += 1
		if cnt > 12 {
			break
		}
	}
	return err
}

func Get_and_sava(url string) error {
	resp, err := http.Get(url)
	Checkerr(err)

	arr := strings.Split(url, "/")
	dir := "Cache"
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		err = os.Mkdir(dir, 0777)
		Checkerr(err)
	}

	out, err := os.Create(dir + "/" + arr[len(arr)-1])
	Checkerr(err)
	_, err = io.Copy(out, resp.Body)

	return err
}
