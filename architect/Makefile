# =======================
# $(ICON_INSTALL) CustomGPT Build System – Architect
# =======================

# Liste explicite des fichiers principaux
CORE_FILES := architect.yaml blackbox-guard.yaml ethics.yaml metadata.yaml self-validation.yaml token-policy.yaml
GPTFIELD_FILES := gpt-fields/instructions.md gpt-fields/conversation-starters.md

# Fichiers dans les sous-dossiers indexes/ et experts/
INDEX_FILES := $(shell find indexes -type f \( -name "*.yaml" -o -name "*.yml" \))
EXPERT_FILES := $(shell find experts -type f \( -name "*.yaml" -o -name "*.yml" \))

# Tous les fichiers à valider
YAML_FILES := $(CORE_FILES) $(INDEX_FILES) $(EXPERT_FILES)

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
	@rm -f experts.yaml
	@rm -rf deploy
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

merge: ## Merge all expert files into a flat, sorted list in experts.yaml
	@printf "$(C_MAGENTA)$(ICON_MERGE) Merging expert files into a flat, sorted list in experts.yaml...$(C_RESET)\n"
	@if [ -f experts.yaml ]; then \
		printf "$(C_RED)$(ICON_FAILURE) Error: experts.yaml already exists. Please run 'make clean' first.$(C_RESET)\n"; \
		exit 1; \
	fi
	@tmpfile=$$(mktemp); \
		yq eval-all '[.[]] | flatten' $(EXPERT_FILES) > $$tmpfile && \
		yq eval 'sort_by(.id)' $$tmpfile | sed '1s/^/---\n/' > experts.yaml && \
		rm $$tmpfile && \
		if yamllint experts.yaml > /dev/null; then \
			printf "$(C_GREEN)$(ICON_SUCCESS) experts.yaml generated successfully.$(C_RESET)\n"; \
		else \
			printf "$(C_RED)$(ICON_FAILURE) experts.yaml is invalid after merge.$(C_RESET)\n"; \
			exit 1; \
		fi
hash: ## Generate hashes and update metadata.yaml without Python
	@printf "$(C_BLUE)$(ICON_HASH) Generating hashes for files listed in metadata.yaml...$(C_RESET)\n"

	@tmpfile=$$(mktemp); \
	cp metadata.yaml $$tmpfile; \
	for i in $$(yq eval '.files[].file' $$tmpfile); do \
		if echo $$i | grep -q 'index'; then f="indexes/$$i"; else f="$$i"; fi; \
		if [ -f "$$f" ]; then \
			hash=$$(sha256sum "$$f" | awk '{print $$1}'); \
			yq eval "(.files[] | select(.file == \"$$i\") ).integrity_hash = \"$$hash\"" -i $$tmpfile; \
		else \
			printf "$(C_YELLOW)$(ICON_WARNING) Warning: $$f not found. Skipping.$(C_RESET)\n"; \
		fi; \
	done; \
	timestamp=$$(date -u +'%Y-%m-%d %H:%M:%S+00:00'); \
	yq eval ".versioning.generated_at = \"$$timestamp\"" -i $$tmpfile; \
	mv $$tmpfile metadata.yaml

	@printf "$(C_GREEN)$(ICON_HASH) Hashes updated in metadata.yaml$(C_RESET)\n"

	@printf "$(C_BLUE)$(ICON_VALIDATE) Validating updated metadata.yaml...$(C_RESET)\n"
	@yamllint metadata.yaml > /dev/null && \
		printf "$(C_GREEN)$(ICON_SUCCESS) metadata.yaml is valid after update.$(C_RESET)\n" || \
		(printf "$(C_RED)$(ICON_FAILURE) metadata.yaml validation failed after update.$(C_RESET)\n" && exit 1)

	@printf "$(C_BLUE)$(ICON_VALIDATE) Verifying integrity hashes in metadata.yaml...$(C_RESET)\n"
	@errors=0; \
	for i in $$(yq eval '.files[].file' metadata.yaml); do \
		if echo $$i | grep -q 'index'; then f="indexes/$$i"; else f="$$i"; fi; \
		if [ -f "$$f" ]; then \
			expected=$$(yq eval ".files[] | select(.file == \"$$i\") | .integrity_hash" metadata.yaml); \
			actual=$$(sha256sum "$$f" | awk '{print $$1}'); \
			if [ "$$expected" != "$$actual" ]; then \
				printf "$(C_RED)$(ICON_FAILURE) Hash mismatch for $$f: expected=$$expected, actual=$$actual$(C_RESET)\n"; \
				errors=1; \
			else \
				printf "$(C_GREEN)$(ICON_SUCCESS) Hash OK for $$f$(C_RESET)\n"; \
			fi; \
		else \
			printf "$(C_YELLOW)$(ICON_WARNING) File not found: $$f (listed in metadata.yaml)$(C_RESET)\n"; \
		fi; \
	done; \
	if [ "$$errors" -eq 0 ]; then \
		printf "$(C_GREEN)$(ICON_SUCCESS) All integrity hashes verified successfully!$(C_RESET)\n"; \
	else \
		printf "$(C_RED)$(ICON_FAILURE) One or more hash mismatches found.$(C_RESET)\n"; \
		exit 1; \
	fi

install: ## Installs selected files into the deploy/ directory
	@echo -e "$(C_GREEN)$(ICON_INSTALL) Installing knowledge files into deploy/ directory...$(C_RESET)"
	@rm -rf deploy
	@mkdir -p deploy

	@# Copy core knowledge files
	@for f in architect.yaml blackbox-guard.yaml ethics.yaml metadata.yaml experts.yaml self-validation.yaml token-policy.yaml; do \
		if [ -f "$$f" ]; then \
			cp "$$f" deploy/; \
		fi \
	done

	@# Copy index files from indexes/
	@for f in indexes/experts-index-*.yaml; do \
		if [ -f "$$f" ]; then \
			cp "$$f" deploy/; \
		fi \
	done

	@echo -e "$(C_GREEN)$(ICON_SUCCESS) Knowledge files successfully deployed into deploy/$(C_RESET)"

archive: ## Archive YAML files and GPT field file into deploy/architect.zip
	@printf "$(C_MAGENTA)$(ICON_ARCHIVE) Creating deployment archive...$(C_RESET)\n"
	@mkdir -p deploy
	@zip -q deploy/architect.zip $(YAML_FILES) $(GPTFIELD_FILES); \
	if [ $$? -eq 0 ]; then \
		printf "$(C_GREEN)$(ICON_SUCCESS) Archive created at deploy/architect.zip$(C_RESET)\n"; \
	else \
		printf "$(C_RED)$(ICON_FAILURE) Failed to create archive.$(C_RESET)\n"; \
		exit 1; \
	fi
