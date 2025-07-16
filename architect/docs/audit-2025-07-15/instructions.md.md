# instructions_patch.md

## ✅ Suggested Additions and Improvements for Instructions Window

These items ensure full alignment with `architect.yaml`, `self-validation.yaml`, `token-policy.yaml`, and expert arbitration logic.

---

### 🔧 1. Add Validation Checks Section

```markdown
### VALIDATION & CONTINUITY
- Validate expert team identity and integrity every 10 rounds.
- Detect expert mismatch and restore from snapshot when necessary.
- If expert entries are invalid or team state is lost, rebuild is triggered.
```

---

### 🧠 2. Add Confidence Score Thresholds

```markdown
### EXPERT CONFIDENCE & CONFLICT HANDLING
- Expert responses with confidence ≥80% are shown.
- Responses below 50% are discarded automatically.
- Architect attempts conflict resolution or offers user choices.
```

---

### ♻️ 3. Add Manual Reset and Rebuild Logic

```markdown
### TEAM RESET & REPAIR
- If an expert ID no longer exists or integrity fails, the Architect triggers a team rebuild.
- Session memory anchor is re-established via validation logic.
```

---

### 🚫 4. Add Expert Pool Truncation Logic

```markdown
### EXPERT MATCH LIMITS
- If user intent matches too many experts, only the top 1–5 are selected.
- Lower-ranked matches are ignored to conserve token budget.
```

---

### 🧹 5. (Optional) Combine Duplicate Fallback Warnings

Consider consolidating fallback warnings from `ACCESS GATING` and `FALLBACK & BLACK BOX` into one unified section to reduce redundancy.

---

## 🧩 Summary

These additions complete the link between your declared instructions and system-enforced rules — covering expert validation, response scoring, rebuild triggers, and overflow handling explicitly.

