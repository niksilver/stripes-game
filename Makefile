ifeq ($(VIRTUAL_ENV),)
$(error Please activate virtual environment for Python)
endif

images:
	@echo "\n\n\n\n\n\n\n\n\n\n\n"
	python gen_assets.py

pdf:
	@echo "\n\n\n\n\n\n\n\n\n\n\n"
	python gen_pdf.py
