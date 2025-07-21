# 🔁 Recall Anchor : Expert Index Keyword Generation Configuration

## Purpose

Generate high-recall, low-collision keyword lists for each expert.  
These keywords enable accurate user-to-expert matching in a semantic index.  
You will use experts given to you and output the YAML.

## Instructions

### Goal

Produce **45–60 unique, user-facing keyword phrases (2–4 words each)** per expert.  
Phrases must reflect how a user would **describe their need** or **formulate a prompt**,  
not how the expert describes their internal methods or tools.

### Source Fields

- `id`
- `name`
- `title`
- `domain`
- `purpose`
- `capabilities`

### Generation Rules

- All keywords must be between **2 and 4 words**. Three is ideal.
- Phrases must use **user-facing phrasing**, not academic or system-internal language.
- Phrases must be **prompt-like**, representing things a user might type or say.
- Prioritize extracting verbs and nouns from capabilities to form **user intent expressions**.
- Use domain context to disambiguate overloaded terms (e.g., qualify “pipeline” as “CI pipeline”).
- Remove vague or weak phrases (e.g., "strategy", "framework", "optimization").
- Avoid including acronyms, tool names alone, or stopword-heavy phrases.

#### ✅ Keyword Refinement Strategy

- When a term is broad, ambiguous, or overloaded (e.g., “policy”, “logging”, “model”),  
  always **anchor it with a domain-specific qualifier** to maximize precision and recall.

  **Examples**:
  - ❌ `"logging"` → ✅ `"compliance logging"`, ✅ `"pipeline logging"`
  - ❌ `"access control"` → ✅ `"SSH access control"`, ✅ `"API access control"`
  - ❌ `"template"` → ✅ `"CI template scaffolding"`, ✅ `"cookiecutter starter template"`

#### ✅ Optional Enhancement: Filter Tool-Only or Acronym Phrases

- Reject any keyword that consists solely of a tool name, library, acronym, or vendor term  
  unless it is **qualified with a user-relevant task or domain context**.

  **Examples**:
  - ❌ `"Sigstore"` → ✅ `"artifact signing with Sigstore"`
  - ❌ `"Z3"` → ✅ `"SMT solving using Z3"`
  - ❌ `"Nix"` → ✅ `"declarative setup with Nix"`

#### ✅ Optional Enhancement: Encourage User-Verb Anchors

- Favor expressions that **begin with or imply a user action**, such as:
  - `detect`, `validate`, `configure`, `enforce`, `scan`, `deploy`, `automate`, `refactor`, `visualize`, `triage`, `benchmark`, `verify`, `debug`.

- These help bind the keyword to **intent-like phrasing**, increasing matchability in CustomGPT prompt vectors.

---

## Output Format

```yaml
yaml_block: true
structure:
  - id: <copy from expert>
    name: <copy from expert>
    title: <copy from expert>
    domain: <copy from expert>
    keywords:
      - <generated keyword phrase 1>
      - <generated keyword phrase 2>
      - ...
    type: expert-index

## ⚙️ Matching Configuration Reference
  semantic_expansion_enabled: true
  intended_use: expert scoring and matching in OpenAI CustomGPT
