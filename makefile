all: install

install:
	./scripts/install.sh

run:
	./scripts/run.sh

clean:
	./scripts/cleanup.sh

build:
	./scripts/build.sh

publish: clean build
	./scripts/publish.sh


.PHONY: all install run clean build