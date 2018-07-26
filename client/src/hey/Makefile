all: test build-linux build-darwin build-windows

build-linux:
	GOARCH=amd64 GOOS=linux go build -o bin/linux/amd64/hey .

build-darwin:
	GOARCH=amd64 GOOS=darwin go build -o bin/darwin/amd64/hey .

build-windows:
	GOARCH=amd64 GOOS=windows go build -o bin/windows/amd64/hey.exe .

test:
	go test -v

clean:
	rm -rf bin/
	rm -f ./hey