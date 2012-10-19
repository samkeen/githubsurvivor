LESS=res/less
CSS=res/static/styles

.PHONY: all css

all: css

$(CSS)/%.css: $(LESS)/%.less
	lessc $< >$@

css: $(patsubst $(LESS)/%.less,$(CSS)/%.css,$(wildcard $(LESS)/*.less))
