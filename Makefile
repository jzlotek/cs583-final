.PHONY: pdf

pdf:
	pandoc -f markdown -t latex -o docs/proposal.pdf docs/proposal.md
