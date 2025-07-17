# validation.md

## 🧪 Self-Validation and Recovery Audit — The Architect GPT

---

### 📜 Purpose

The `self-validation.yaml` module defines The Architect’s ability to detect:
- Broken team state
- Corrupted or outdated snapshots
- Missing expert definitions
- Degraded internal security

It is critical to ensuring long-session reliability and preventing silent drift in expert orchestration.

---

## 🔁 `validate_team_integrity`

```yaml
- name: validate_team_integrity
  check_every: 10_rounds
  if: team_confirmed == false and session_state.last_confirmed_team exists
```

✅ **Purpose**:
- Recovers expert team after memory flush
- Ensures persistent team continuity across session resumption

✅ **Enforcement Detected**:
- `architect.yaml` includes:
  ```yaml
  - condition: round_number % 10 == 0
    then:
      validate_team_integrity: true
  ```

📌 Team is validated every 10 rounds.
📌 Expert names must exist in `experts.yaml`.
📌 If successful: team is restored + `team_confirmed = true`.

---

## 📦 `validate_snapshot_consistency`

```yaml
- name: validate_snapshot_consistency
  if: session_state.last_confirmed_team exists
```

✅ **Purpose**:
- Verifies that `session_state.last_confirmed_team` only references valid expert entries

✅ **Logic**:
- Enforces `enforce_exact_match: true`
- Responds with pass/fail message based on match

🔄 Used by: `run_all_validations`

---

## 🧪 `run_all_validations`

```yaml
- name: run_all_validations
  run_block:
    - validate_team_integrity
    - validate_snapshot_consistency
```

✅ Combines both validations.
✅ Used manually or through admin triggers.
✅ Sends summary to user.

---

## 🔐 `validate_blackbox_guard_loaded`

```yaml
- name: validate_blackbox_guard_loaded
  check_once: true
  if: plugin_metadata_access_guard not loaded
```

✅ **Purpose**:
- Ensures the security plugin (`blackbox-guard.yaml`) is active

✅ Responds:
- Warning if not loaded
- Confirmation if plugin is present

🔒 Required for sealed system enforcement

---

## ✅ Audit Summary

| Validation Block | Enforced in System | Notes |
|------------------|--------------------|-------|
| `validate_team_integrity` | ✅ Yes | Triggered every 10 rounds |
| `validate_snapshot_consistency` | ✅ Yes | Used in block 14 audit |
| `run_all_validations` | ✅ Optional utility | Can be triggered manually |
| `validate_blackbox_guard_loaded` | ✅ Yes | Ensures plugin guard is not missing |

---

### 🧩 Final Status

Your validation logic is **fully integrated** and active at runtime.

- ✅ Team state is auto-repaired if lost
- ✅ Expert names are matched exactly to avoid hallucination
- ✅ Blackbox plugin presence is checked defensively
- ✅ User is warned if any security or memory sync issue arises

