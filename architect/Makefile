# =======================
# CustomGPT Build System – Architect
# =======================

VERSION := 1.0
MAINTAINER := ericvachon@bibittes.casa

# Liste explicite des fichiers principaux
GPTFIELD_FILES := gpt-fields/instructions.md gpt-fields/conversation-starters.md

# Fichiers dans les sous-dossiers indexes/ et experts/
CORE_FILES := $(shell find core -type f \( -name "*.yaml" -o -name "*.yml" \))
INDEX_FILES := $(shell find indexes -type f \( -name "*.yaml" -o -name "*.yml" \))
EXPERT_FILES := $(shell find experts -type f \( -name "*.yaml" -o -name "*.yml" \))
ETHIC_FILES := $(shell find ethics -type f \( -name "*.yaml" -o -name "*.yml" \))

# Tous les fichiers à valider
YAML_FILES := $(CORE_FILES) $(INDEX_FILES) $(EXPERT_FILES) $(ETHIC_FILES)

# ─── COLORS ──────────────────────────────────────────────────────────────
C_RESET  := \033[0m
C_BLUE   := \033[36m
C_GREEN  := \033[32m
C_RED    := \033[31m
C_YELLOW := \033[33m
C_MAGENTA := \033[35m
C_CYAN   := \033[36m

# ─── ICONS (NERD FONTS) ──────────────────────────────────────────────────
ICON_CLEAN     :=    # nf-fa-trash
ICON_VALIDATE  :=    # nf-oct-check
ICON_MERGE     :=    # nf-oct-git_merge
ICON_HASH      :=    # nf-oct-shield
ICON_INSTALL   :=    # nf-fa-cloud_upload
ICON_SUCCESS   :=    # nf-oct-checklist
ICON_FAILURE   :=    # nf-oct-x
ICON_WARNING   :=    # nf-fa-warning
ICON_ARCHIVE   :=    # nf-oct-package

# =======================
# FLAGS
# =======================
VERBOSE ?= 0
ifeq ($(VERBOSE),1)
	ECHO = @echo
else
	ECHO = @:
endif

.PHONY: all clean validate merge hash install help

all: clean validate merge hash install archive



help: ## Show this help message
	@printf "\n"
	@printf "$(C_MAGENTA)╭────────────────────────────────────────────╮$(C_RESET)\n"
	@printf "$(C_MAGENTA)│  $(ICON_INSTALL) CustomGPT Build System – Architect     │$(C_RESET)\n"
	@printf "$(C_MAGENTA)╰────────────────────────────────────────────╯$(C_RESET)\n"
	@printf "          _           _           _        \n"
	@printf " __ _ _ __| |__   ___ | |__   __ _| |_ ___  \n"
	@printf "/ _\` | '__| '_ \\ / _ \\| '_ \\ / _\` | __/ _ \\ \n"
	@printf "| (_| | |  | | | | (_) | |_) | (_| | || (_) |\n"
	@printf " \\__,_|_|  |_| |_|\\___/|_.__/ \\__,_|\\__\\___/ \n"
	@printf "\n"
	@printf "$(C_BLUE)$(ICON_INSTALL) Available Commands:$(C_RESET)\n"
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(C_CYAN)%-15s$(C_RESET) %s\n", $$1, $$2}'
	@printf "\n"

clean: ## Clean temporary files and deploy directory
	@printf "$(C_YELLOW)$(ICON_CLEAN) Cleaning files...$(C_RESET)\n"
	@rm -rf deploy
	@rm -rf build
	@printf "$(C_BLUE)$(ICON_SUCCESS) Clean completed.$(C_RESET)\n"

validate: ## Validate all YAML files with yamllint
	@printf "$(C_BLUE)$(ICON_VALIDATE) Validating YAML files...$(C_RESET)\n"
	@errors=0; \
	for file in $(YAML_FILES); do \
		yamllint "$$file" > /dev/null; \
		if [ $$? -eq 0 ]; then \
			printf "  $(C_GREEN)$(ICON_SUCCESS) $$file$(C_RESET)\n"; \
		else \
			printf "  $(C_RED)$(ICON_FAILURE) $$file$(C_RESET)\n"; \
			yamllint "$$file"; \
			errors=1; \
		fi; \
	done; \
	if [ "$$errors" -eq 0 ]; then \
		printf "$(C_GREEN)$(ICON_SUCCESS) All YAML files are valid!$(C_RESET)\n"; \
	else \
		printf "$(C_RED)$(ICON_FAILURE) Validation failed: some YAML files contain errors.$(C_RESET)\n"; \
		exit 1; \
	fi

merge: ##   Fusionne tous les experts avec leurs règles d’éthique dans build/experts.yaml (strict: aucune règle manquante)
#	@python scripts/merge_experts.py
	@python scripts/generate-experts.py
	@python scripts/create-architect.py

hash: ## Generate hashes and update build/metadata.yaml
	@printf "$(C_BLUE)$(ICON_HASH) Generating integrity hashes into build/metadata.yaml...$(C_RESET)\n"

	@mkdir -p build

	@cp core/metadata.yaml build/metadata.yaml

	@for i in $$(yq eval '.files[].filename' build/metadata.yaml); do \
		case "$$i" in \
			experts.yaml) f="build/$$i" ;; \
			*index*)      f="indexes/$$i" ;; \
			*)            f="core/$$i" ;; \
		esac; \
		if [ -f "$$f" ]; then \
			hash=$$(sha256sum "$$f" | awk '{print $$1}'); \
			yq eval "(.files[] | select(.filename == \"$$i\") ).integrity_hash = \"$$hash\"" -i build/metadata.yaml; \
		else \
			printf "$(C_YELLOW)$(ICON_WARNING) Warning: file not found: $$f (for entry $$i)$(C_RESET)\n"; \
		fi; \
	done

	@timestamp=$$(date -u +'%Y-%m-%d %H:%M:%S+00:00'); \
	yq eval ".generated_at = \"$$timestamp\"" -i build/metadata.yaml
	@yq eval ".version = $(VERSION)" -i build/metadata.yaml
	@yq eval ".maintainer = \"$(MAINTAINER)\"" -i build/metadata.yaml

	@printf "$(C_GREEN)$(ICON_HASH) Hashes successfully updated in build/metadata.yaml$(C_RESET)\n"

	@printf "$(C_BLUE)$(ICON_VALIDATE) Validating build/metadata.yaml...$(C_RESET)\n"
	@yamllint build/metadata.yaml > /dev/null && \
		printf "$(C_GREEN)$(ICON_SUCCESS) metadata.yaml is valid.$(C_RESET)\n" || \
		(printf "$(C_RED)$(ICON_FAILURE) metadata.yaml validation failed.$(C_RESET)\n" && exit 1)

	@printf "$(C_BLUE)$(ICON_VALIDATE) Verifying hashes against disk...$(C_RESET)\n"
	@errors=0; \
	for i in $$(yq eval '.files[].filename' build/metadata.yaml); do \
		case "$$i" in \
			experts.yaml) f="build/$$i" ;; \
			*index*)      f="indexes/$$i" ;; \
			*)            f="core/$$i" ;; \
		esac; \
		if [ -f "$$f" ]; then \
			expected=$$(yq eval ".files[] | select(.filename == \"$$i\") | .integrity_hash" build/metadata.yaml); \
			actual=$$(sha256sum "$$f" | awk '{print $$1}'); \
			if [ "$$expected" != "$$actual" ]; then \
				printf "$(C_RED)$(ICON_FAILURE) Hash mismatch for $$f: expected=$$expected, actual=$$actual$(C_RESET)\n"; \
				errors=1; \
			else \
				printf "$(C_GREEN)$(ICON_SUCCESS) OK: $$f$(C_RESET)\n"; \
			fi; \
		else \
			printf "$(C_YELLOW)$(ICON_WARNING) Missing file: $$f (referenced as $$i)$(C_RESET)\n"; \
		fi; \
	done; \
	if [ "$$errors" -eq 0 ]; then \
		printf "$(C_GREEN)$(ICON_SUCCESS) All hashes verified successfully.$(C_RESET)\n"; \
	else \
		printf "$(C_RED)$(ICON_FAILURE) One or more hash mismatches detected.$(C_RESET)\n"; \
		exit 1; \
	fi

install: clean-deploy ## Copy all final deployment files to deploy/
	@printf "$(C_BLUE)$(ICON_INSTALL) Preparing deployment folder → deploy/$(C_RESET)\n"

	@mkdir -p deploy

	@cp build/metadata.yaml deploy/metadata.yaml

	@for i in $$(yq eval '.files[].filename' build/metadata.yaml); do \
		case "$$i" in \
			experts.yaml) f="build/$$i" ;; \
			*index*)      f="indexes/$$i" ;; \
			*)            f="core/$$i" ;; \
		esac; \
		if [ -f "$$f" ]; then \
			cp "$$f" "deploy/$$i"; \
			printf "$(C_GREEN)$(ICON_SUCCESS) Copied: $$f → deploy/$$i$(C_RESET)\n"; \
		else \
			printf "$(C_YELLOW)$(ICON_WARNING) Skipped missing file: $$f$(C_RESET)\n"; \
		fi; \
	done

	@printf "$(C_GREEN)$(ICON_SUCCESS) Deployment package ready in deploy/$(C_RESET)\n"

clean-deploy: ## Clean the deploy/ folder before fresh install
	@printf "$(C_RED)$(ICON_CLEAN) Cleaning deployment folder → deploy/$(C_RESET)\n"
	@rm -rf deploy/
	@mkdir -p deploy
	@printf "$(C_GREEN)$(ICON_SUCCESS) deploy/ is now clean and ready.$(C_RESET)\n"

archive: ## Create a flat zip archive from deploy/ and gpt-fields/
	@printf "$(C_MAGENTA)$(ICON_ARCHIVE) Creating flat archive → build/architect.zip$(C_RESET)\n"
	@mkdir -p build/archive_temp
	@cp -a deploy/* build/archive_temp/
	@cp -a gpt-fields/* build/archive_temp/
	@cd build/archive_temp && zip -rq ../architect.zip .
	@rm -rf build/archive_temp
	@printf "$(C_GREEN)$(ICON_SUCCESS) Archive build/architect.zip ready.$(C_RESET)\n"
