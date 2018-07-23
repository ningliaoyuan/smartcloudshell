package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/user"
	"strings"
)

const (
	localEndpoint  = "http://localhost:5000"
	remoteEndpoint = "http://smartcloudshellapi.westus2.azurecontainer.io"
)

var (
	debugMode = false
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
		debugMode = true
		r, err := fetchSuggestions(localEndpoint, strings.Join(os.Args[2:], " "))

		if err != nil {
			fmt.Printf("Something went wrong: %s\n", err.Error())
		}

		presentResult(r)
	} else {
		input := ""
		if os.Args[1] == "-d" {
			debugMode = true
			input = strings.Join(os.Args[2:], " ")
		} else {
			input = strings.Join(os.Args[1:], " ")
		}

		if debugMode {
			fmt.Printf("[DEBUG] Input: %s\n", input)
		}

		r, err := fetchSuggestions(remoteEndpoint, input)

		if err != nil {
			fmt.Printf("Something went wrong: %s\n", err.Error())
		}

		if debugMode {
			fmt.Printf("[DEBUG] %d results returned.\n", len(r))

			for _, item := range r {
				fmt.Printf("[DEBUG] %v\t%s\t%s\n", item.Score, item.ID, item.Str)
			}
		} else {
			presentResult(r)
		}
	}
}

func presentResult(r []Suggestion) {
	reader := bufio.NewReader(os.Stdin)

	for i, c := range r {
		fmt.Printf("Did you mean `az %s` that will `%s`? (Y/n)", c.ID, c.Str)

		input, _ := reader.ReadString('\n')

		if len(input) == 1 || input[0] == 'Y' || input[0] == 'y' || i > 5 || strings.ToLower(input) == "yes" {
			break
		}
		fmt.Println()
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

func getLastCommand() string {
	usr, err := user.Current()
	if err != nil {
		log.Fatal(err)
	}

	histFile := usr.HomeDir + "/.bash_history"

	if _, err := os.Stat(histFile); err != nil {
		fmt.Println(err)
		return ""
	}

	buff, err := ioutil.ReadFile(histFile)

	if err != nil {
		fmt.Println(err)
		return ""
	}

	commands := strings.Split(string(buff), "\n")
	return commands[len(commands)-2]
}

func printHelp() {
	fmt.Println("Hey! What's up?")
	fmt.Println()
	fmt.Println("Ask me anything. Say, `hey list my virtual machines`")
	fmt.Println()

	lastCommand := getLastCommand()

	if lastCommand != "" {
		fmt.Println("Last command you typed: " + lastCommand)
		r, err := fetchSuggestions(remoteEndpoint, lastCommand)

		if err != nil {
			fmt.Println("Sorry I have no idea what you mean.")
			return
		}

		presentResult(r)
	}
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
