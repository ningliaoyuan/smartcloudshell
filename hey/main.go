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
	remoteEndpoint = "http://heyapi.trafficmanager.net"
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

// CliSuggestion is the result for CLI
type CliSuggestion struct {
	CliType    string  `json:"cliType"`
	Executable bool    `json:"executable"`
	Help       string  `json:"help"`
	ID         string  `json:"id"`
	Score      float64 `json:"score"`
}

// SuggestionV2 is the new return structure
type SuggestionV2 struct {
	Cli    []CliSuggestion `json:"cli"`
	Custom string          `json:"custom"`
}

func main() {
	if len(os.Args) == 1 {
		handleDefault()
	} else if len(os.Args) == 2 && strings.ToLower(os.Args[1]) == "help" {
		showHelp()
	} else if len(os.Args) == 2 && os.Args[1] == "test" {
		selfTest()
	} else if len(os.Args) > 2 && os.Args[1] == "local" {
		debugMode = true
		r, err := fetchSuggestions(localEndpoint, strings.Join(os.Args[2:], " "))

		if err != nil {
			fmt.Printf("Something went wrong: %s\n", err.Error())
		}

		presentResult(*r)
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
			fmt.Printf("[DEBUG] %d results returned.\n", len(r.Cli))

			for _, item := range r.Cli {
				fmt.Printf("[DEBUG] %v\t%s\t%s\n", item.Score, item.ID, item.Help)
			}

			fmt.Printf("[DEBUG] Custom: %s", r.Custom)
		} else {
			presentResult(*r)
		}
	}
}

func presentResult(r SuggestionV2) {
	reader := bufio.NewReader(os.Stdin)

	if len(r.Cli) > 0 {
		for i, c := range r.Cli {
			fmt.Printf("Did you mean `az %s` that will `%s`? (Y/n)", c.ID, c.Help)

			input, _ := reader.ReadString('\n')

			if len(input) == 1 || input[0] == 'Y' || input[0] == 'y' || i > 5 || strings.ToLower(input) == "yes" {
				break
			}
			fmt.Println()
		}
	} else if r.Custom != "" {
		cowsay([]string{r.Custom})
	}
}

func fetchSuggestions(endpoint, q string) (*SuggestionV2, error) {
	client := &http.Client{}

	url := fmt.Sprintf("%s/q/%s?custom=true&search=true&top=10", endpoint, q)
	resp, err := client.Get(url)

	if err != nil {
		return nil, fmt.Errorf("Whoops, something went wrong: %s", err)
	}

	defer resp.Body.Close()
	buff, err := ioutil.ReadAll(resp.Body)

	var r SuggestionV2
	err = json.Unmarshal(buff, &r)
	if err != nil {
		return nil, err
	}

	if len(r.Cli) == 0 && r.Custom == "" {
		return nil, fmt.Errorf("I have no idea what you are talking about")
	}

	return &r, nil
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
	last := ""
	if len(commands) >= 2 {
		cmd := commands[len(commands)-2]

		segments := strings.Split(cmd, " ")

		if len(segments) > 0 && segments[0] == "az" {
			for i := 1; i < len(segments); i++ {
				c := segments[i]
				if len(c) > 0 && c[0] == '-' {
					break
				}

				last = last + " " + c
			}
		}
	}

	return last
}

func handleDefault() {
	lastCommand := getLastCommand()

	if lastCommand != "" {
		fmt.Println("Last command you typed: " + lastCommand)
		r, err := fetchSuggestions(remoteEndpoint, lastCommand)

		if err != nil {
			fmt.Println("Sorry I have no idea what you mean.")
			return
		}

		presentResult(*r)
	} else {
		showHelp()
	}
}

func showHelp() {
	welcome := []string{"Hey! What's up?", "Ask me anything. Say, `hey list my virtual machines`"}
	cowsay(welcome)
}

func cowsay(text []string) {
	width := maxWidth(text)
	messages := setPadding(text, width)

	cow := "default"
	cowfile = &cow

	f := newFace()
	balloon := constructBallon(f, messages, width)

	fmt.Println(balloon)
	renderCow(f, os.Stdout)
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
