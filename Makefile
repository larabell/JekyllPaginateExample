
build: generate
	jekyll build

trace: generate
	jekyll build --trace

serve: generate
	jekyll serve

generate: clean
	./genposts.py

clean:
	rm -rf _category1 _category2 _category3 _config.yml _layouts _lists _pages _posts _site index.md
