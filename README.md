# 🛠️ SWE-Bench Task Forge

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)]()
[![Benchmark](https://img.shields.io/badge/Format-SWE--bench%20Verified-success)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

**A production toolchain and verification pipeline for authoring, extracting, and verifying SWE-bench & SWE-bench Lite task instances.**

SWE-bench is the premier benchmark for measuring autonomous coding agents on real-world GitHub issues. However, creating high-signal task instances requires strict compliance with isolation rules, deterministic fail-to-pass test guarantees, and zero test leakage. `swe-bench-task-forge` standardizes this authoring workflow.

---

## 🎯 Authoring Methodology & Protocol

Creating a valid SWE-bench instance follows a strict 3-stage verification protocol:

```
        Raw GitHub PR & Issue
                  │
                  ▼
      ┌───────────────────────┐
      │ 1. Base Commit State  │
      └───────────┬───────────┘
                  │ Apply test_patch
                  ▼
      ┌───────────────────────┐
      │ 2. F2P Verification   │ ──► [FAIL_TO_PASS tests MUST FAIL]
      └───────────┬───────────┘
                  │ Apply gold patch
                  ▼
      ┌───────────────────────┐
      │ 3. Patch Verification │ ──► [FAIL_TO_PASS tests MUST PASS]
      │                       │ ──► [PASS_TO_PASS tests MUST PASS]
      └───────────────────────┘
```

1. **Test Isolation:** The `test_patch` must only introduce tests targeting the reported bug. It must never modify application source files.
2. **Gold Patch Purity:** The model solution `patch` must only modify source files. It is strictly forbidden from modifying test suites or assertions (preventing agents from cheating tests).
3. **No Regressions:** All existing tests (`PASS_TO_PASS`) must continue passing without breakage.

---

## 📦 Bundled Verified Instances

The repository includes pre-verified task instances across tier-1 open-source repositories:

| Instance ID | Repository | Target Issue / Bug | F2P Test Targets |
| :--- | :--- | :--- | :---: |
| `psf__requests-7102` | `psf/requests` | Stripping sensitive `Authorization` headers on 307/308 cross-domain/port redirects | 1 |
| `pallets__flask-5421` | `pallets/flask` | Normalizing nested blueprint `url_prefix` with trailing slashes to avoid `//` | 1 |
| `scikit-learn__scikit-learn-28912` | `scikit-learn` | Clamping negative floating-point noise in sparse Euclidean distances | 1 |

---

## 🚀 Usage

### 1. Installation
```bash
git clone https://github.com/jatinsihag2345/swe-bench-task-forge.git
cd swe-bench-task-forge
pip install -e .
```

### 2. Validate All Bundled Instances
Run the automated validator to enforce SWE-bench rules:
```bash
python3 -m swe_forge.cli validate
```

### 3. List Instances
```bash
python3 -m swe_forge.cli list
```

### 4. Export JSONL Dataset
Export task instances to standard SWE-bench JSONL format for evaluation runners:
```bash
python3 -m swe_forge.cli export --out dataset/swe_bench_verified_custom.jsonl
```

---

## 📋 Instance Schema

```json
{
  "instance_id": "psf__requests-7102",
  "repo": "psf/requests",
  "base_commit": "e4b6c311689255a29f8f2b74070a7b4f5358055c",
  "problem_statement": "Description of the bug...",
  "patch": "diff --git a/requests/sessions.py...",
  "test_patch": "diff --git a/tests/test_requests.py...",
  "version": "2.31.0",
  "environment_setup_commit": "e4b6c311689255a29f8f2b74070a7b4f5358055c",
  "FAIL_TO_PASS": ["tests/test_requests.py::test_cross_domain_redirect_strips_auth"],
  "PASS_TO_PASS": ["tests/test_requests.py::test_basic_auth"]
}
```

---

## 📄 License
MIT License. Authored by [Jatin Sihag](https://github.com/jatinsihag2345).
