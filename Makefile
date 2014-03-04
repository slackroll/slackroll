.PHONY: all clean

all: index.txt
	asciidoc index.txt

clean:
	rm -f index.html
