package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"strings"

	"github.com/alecthomas/template"
	runewidth "github.com/mattn/go-runewidth"
)

type face struct {
	Eyes     string
	Tongue   string
	Thoughts string
	cowfile  string
}

var think *bool
var list *bool
var columns *int32
var cowfile *string

func newFace() *face {
	f := &face{
		Eyes:    "oo",
		Tongue:  "  ",
		cowfile: *cowfile,
	}

	f.Eyes = "**"
	f.Tongue = "U "
	return f
}

func setPadding(msgs []string, width int) []string {
	var ret []string
	for _, m := range msgs {
		s := m + strings.Repeat(" ", width-runewidth.StringWidth(m))
		ret = append(ret, s)
	}

	return ret
}

func constructBallon(f *face, msgs []string, width int) string {
	var borders []string
	line := len(msgs)

	f.Thoughts = "\\"
	if line == 1 {
		borders = []string{"<", ">"}
	} else {
		borders = []string{"/", "\\", "\\", "/", "|", "|"}
	}

	var lines []string

	topBorder := " " + strings.Repeat("_", width+2)
	bottomBoder := " " + strings.Repeat("-", width+2)

	lines = append(lines, topBorder)
	if line == 1 {
		s := fmt.Sprintf("%s %s %s", borders[0], msgs[0], borders[1])
		lines = append(lines, s)
	} else {
		s := fmt.Sprintf(`%s %s %s`, borders[0], msgs[0], borders[1])
		lines = append(lines, s)
		i := 1
		for ; i < line-1; i++ {
			s = fmt.Sprintf(`%s %s %s`, borders[4], msgs[i], borders[5])
			lines = append(lines, s)
		}
		s = fmt.Sprintf(`%s %s %s`, borders[2], msgs[i], borders[3])
		lines = append(lines, s)
	}

	lines = append(lines, bottomBoder)
	return strings.Join(lines, "\n")
}

func maxWidth(msgs []string) int {
	max := -1
	for _, m := range msgs {
		l := runewidth.StringWidth(m)
		if l > max {
			max = l
		}
	}

	return max
}

func renderCow(f *face, w io.Writer) {
	t := template.Must(template.New("cow").Parse(cows[f.cowfile]))

	if err := t.Execute(w, f); err != nil {
		log.Println(err)
		os.Exit(1)
	}
}
