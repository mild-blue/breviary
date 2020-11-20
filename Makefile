.PHONY: help

.DEFAULT: help
help:
	@echo "TODO"

CONDA_ENV=breviary

# creates environment from the file
conda-create:
	conda env create -f conda.yml --name $(CONDA_ENV)

# exports all changes made locally - then one must copy the changes to conda.yml
conda-export:
	conda env export --from-history

# updates environment when some changes were applied to the file
conda-update:
	conda env update --file conda.yml --prune --name $(CONDA_ENV)

# does not actually work, has to be called manually
conda-activate:
	conda activate $(CONDA_ENV)

db:
	docker-compose up -d db

build_and_push_worker:
	. ./devops/build_and_push_to_dockerhub.sh && build_and_push_worker

build_and_push_backend:
	. ./devops/build_and_push_to_dockerhub.sh && build_and_push_backend

redeploy_staging:
	. ./devops/redeploy_staging.sh