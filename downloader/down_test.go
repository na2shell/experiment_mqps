package main

import (
	"fmt"
	"testing"
)

func Test_poling(t *testing.T) {
	url := "https://www.wis-jma.go.jp/data/syn?ContentType=Text&Category=&Type=Alphanumeric&Access=Open"
	outfile := "filelist.txt"
	fmt.Print("test is start \n")
	err := Polling_udpate_file(outfile, url)
	//fmt.Print("test is done \n")
	if err != nil {
		t.Error("something happen. err is ", err)
	}
}

func Test_dwn_all(t *testing.T) {
	Download_all("filelist.txt")
}
