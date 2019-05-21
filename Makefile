.PHONY: pages proposal clean-docs

pages:
	cat docs/pages.head > docs/index.md
	cat docs/docs.md >> docs/index.md


proposal:
	cat docs/proposal.head > docs/proposal.md
	cat docs/docs.md >> docs/proposal.md
	pandoc -f markdown -t latex -o docs/proposal.pdf docs/proposal.md

clean-docs:
	-@ rm docs/proposal.md docs/proposal.pdf
