package main

import (
	"bufio"
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
		r, err := fetchSuggestions(localEndpoint, strings.Join(os.Args[2:], " "))

		if err != nil {
			fmt.Printf("Something went wrong: %s\n", err.Error())
		}

		reader := bufio.NewReader(os.Stdin)

		for i, c := range r {
			fmt.Printf("Did you mean `%s` that will `%s`? Confident level %v. (Y/n)", c.ID, c.Str, c.Score)

			input, _ := reader.ReadString('\n')

			if len(input) == 1 || input[0] == 'Y' || input[0] == 'y' || i > 5 {
				break
			}
			fmt.Println()
		}
	} else {
		r, err := fetchSuggestions(remoteEndpoint, strings.Join(os.Args[2:], " "))

		if err != nil {
			fmt.Printf("Something went wrong: %s\n", err.Error())
		}

		reader := bufio.NewReader(os.Stdin)

		for i, c := range r {
			fmt.Printf("Did you mean `%s` that will `%s`? Confident level %v\n", c.ID, c.Str, c.Score)

			input, _ := reader.ReadString('\n')

			if len(input) == 0 || input == "Y" || input == "y" || i > 5 {
				break
			}
			fmt.Println()
		}
	}
}

func fetchSuggestions(endpoint, q string) ([]Suggestion, error) {
	client := &http.Client{}

	url := fmt.Sprintf("%s/cli/help/%s", endpoint, q)
	resp, err := client.Get(url)

	if err != nil {
		return nil, fmt.Errorf("Whoops, something went wrong: %s", err)
	}

	defer resp.Body.Close()
	buff, err := ioutil.ReadAll(resp.Body)

	var r []Suggestion
	err = json.Unmarshal(buff, &r)
	if err != nil {
		return nil, err
	}

	if len(r) == 0 {
		return nil, fmt.Errorf("I have no idea what you are talking about")
	}

	return r, nil
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
	}

	defer resp.Body.Close()
	buf, _ := ioutil.ReadAll(resp.Body)

	return string(buf), nil
}
