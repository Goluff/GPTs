# token.md

## 🧠 Token Policy — Enforcement and Runtime Safeguards

---

### 📜 Purpose

This file defines how The Architect handles **context window management**, token overflow risks, and expert coordination under tight budget constraints. It aligns with the 128,000-token limit of GPT-4o and ensures graceful degradation through dynamic compression, user alerts, and modular response strategies.

---

## 🔢 Context Boundaries

```yaml
max_context_tokens: 128000
```

- The limit is correctly set for GPT-4o.
- This does **not truncate automatically** — it defines the theoretical cap against which dynamic strategies are triggered.

---

## 🔄 Segments and Risk Management

The policy is divided into **4 segments**, each addressing a critical operational stage:

---

### 🔹 Segment 1: `expert_ranking`

**Scope**: Team formation

**Risks**:
- Full expert registry scan may overload token space
- Ambiguity-triggered semantic expansion bloats score phase

**Mitigations**:
- ✅ Tag/domain prefiltering (confirmed present in `architect.yaml`)
- ✅ Warnings if expert pool > 25 (should be reflected in behavior blocks)
- ✅ Batch scoring logic present via `score_experts_by_tags`
- ⚠️ Only enforced if `expert_score_pool` respects batch boundaries in runtime

---

### 🔹 Segment 2: `expert_response_integration`

**Scope**: Synthesizing multi-expert replies

**Risks**:
- Large token blocks during consensus/synthesis
- Conflicting replies increase load

**Mitigations**:
- ✅ Show only top-N (80% confidence in `architect.yaml`)
- ✅ Queue others — implied by “load more” warning pattern
- ✅ Pause summary — reflected in block `rank_responses` logic

---

### 🔹 Segment 3: `file_snapshot_validation`

**Scope**: Hash validation during file edits

**Risks**:
- If root SHA summary is lost, session cannot verify file integrity

**Mitigations**:
- ✅ Hash summary required (found in `architect.yaml`)
- ✅ Session anchored to `metadata.yaml` hash table
- ✅ Re-archive logic is enforced every 30–60 min idle

---

### 🔹 Segment 4: `user_input_handling`

**Scope**: Logs, configs, or user-pasted code

**Risks**:
- Paste > 8K tokens disrupts team logic
- Experts cannot score or reason under overflow

**Mitigations**:
- ✅ User warned over 8K input
- ✅ Supports `compress_history` override
- ✅ Tasks deferred until input is handled — enforced in `behavior_flow`

---

## ⏱️ Runtime Threshold Actions

### ⚠️ Nearing Limit — 90,000 Tokens

```yaml
runtime_actions:
  nearing_token_limit:
    trigger_at: 90000
    actions:
      - warn_user
      - allow_user_choice
```

✅ **Confirmed Enforced** in `architect.yaml`:
```yaml
- condition: token_count > 90000
  then:
    respond: "⚠️ Context window nearing limit. I may compress earlier content..."
```

---

### 🚫 Hard Limit Prep — 110,000 Tokens

```yaml
runtime_actions:
  overload_detected:
    trigger_at: 110000
    actions:
      - auto_compress_active_team_state
      - suppress logs
      - reanchor with summary_state.yaml
```

✅ Also enforced:
```yaml
- condition: token_count > 110000
  then:
    compress_state: true
    block_all_actions: true
```

---

## ✅ Audit Summary

| Segment | Risks Addressed | Enforced in `architect.yaml`? |
|---------|------------------|-------------------------------|
| expert_ranking | Token bloating from full scans | ✅ via batch scoring + tag filter |
| expert_response_integration | Reply overflow | ✅ via top-N and synthesis arbitration |
| file_snapshot_validation | SHA mismatch | ✅ via hash snapshots, re-archive prompt |
| user_input_handling | Pasted input overflow | ✅ with chunking, deferral, and override |

| Runtime Event | Actions Present | Enforced? |
|---------------|-----------------|-----------|
| nearing_token_limit | Warn + Choice | ✅ |
| overload_detected | Compress + Suspend | ✅ |

---

### 🧩 Final Note

This policy is **fully active** and successfully integrated into your `architect.yaml`. It protects session memory integrity, ensures modular response safety, and prevents expert logic collapse due to token bloat.

