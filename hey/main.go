package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

const (
	localEndpoint  = "http://localhost:5000"
	remoteEndpoint = "http://notdeployedy.com"
)

// Suggestion is the return structure
type Suggestion struct {
	ID    string  `json:"id"`
	Score float64 `json:"score"`
	Str   string  `json:"str"`
}

func main() {
	if len(os.Args) == 1 {
		printHelp()
	} else if len(os.Args) == 2 && os.Args[1] == "test" {
		selfTest()
	} else if len(os.Args) > 2 && os.Args[1] == "local" {
		fmt.Println(fetchSuggestions(localEndpoint, strings.Join(os.Args[2:], " ")))
	} else {
		fmt.Println(fetchSuggestions(remoteEndpoint, strings.Join(os.Args[2:], " ")))
	}
}

func fetchSuggestions(endpoint, q string) string {
	client := &http.Client{}

	url := fmt.Sprintf("%s/cli/help/%s", endpoint, q)
	resp, err := client.Get(url)

	if err != nil {
		return "Whoops, something went wrong: %s"
	}

	defer resp.Body.Close()
	buff, err := ioutil.ReadAll(resp.Body)

	var r []Suggestion
	err = json.Unmarshal(buff, &r)
	if err != nil {
		return err.Error()
	}

	if len(r) == 0 {
		return "I have no idea what you are talking about."
	}

	return fmt.Sprintf("Do you mean `az %s`. Confidence level: %v", r[0].ID, r[0].Score)
}

func printHelp() {
	fmt.Println("Hey! What's up?")
	fmt.Println()
	fmt.Println("Ask me anything. Say, `hey list my virtual machines`")
	fmt.Println()
}

func selfTest() {
	resp, err := testEndpoint(localEndpoint)
	if err != nil {
		fmt.Println("Local endpoint test FAILED: " + err.Error())
	} else {
		fmt.Println("Local endpoint test PASSED: " + resp)
	}

	resp, err = testEndpoint(remoteEndpoint)
	if err != nil {
		fmt.Println("Remote endpoint test FAILED: " + err.Error())
	} else {
		fmt.Println("Remote endpoint test PASSED: " + resp)
	}
}

func testEndpoint(url string) (string, error) {
	client := &http.Client{}
	resp, err := client.Get(url)

	if err != nil {
		return "", fmt.Errorf("Connect endpoint failed: %s", err.Error())
	} else {
		defer resp.Body.Close()
		buf, _ := ioutil.ReadAll(resp.Body)

		return string(buf), nil
	}
}
