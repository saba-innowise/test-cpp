# tether_sum — CI/CD Release-Flow Challenge (C++ / CMake / Conan 2 / GitHub Actions)

This repository contains a **tiny C++ library** (`int sum(int a, int b)`) and—more importantly—a **fully automated CI/CD pipeline** implementing the release process described in the challenge.

The C++ code is intentionally trivial. The core of this project is the **label-driven, multi-platform, Conan-based release flow**.

---

## Goals and non-goals

### Goals
- Build + test a trivial C++ library using **CMake** + **GoogleTest**
- Package the library with **Conan 2** so consumers can:
  - `conan install --requires=tether_sum/<ref>`
- Run CI on **Linux / Windows / macOS**
- Enforce PR rules:
  - Up-to-date with `main`
  - Linear history
  - Format/lint + build + unit tests
- Add label-driven workflows:
  - `verify` label → integration/E2E consumer test
  - `publish` label → pre-merge RC packages uploaded to `conan-rc` (per OS) + validation that release doesn’t already exist in `conan-stable`
- On merge of a PR with `publish` label:
  - Upload final packages to `conan-stable`
  - Create git tag `vX.Y.Z`
  - Create a GitHub Release
- Extract reusable workflows/actions into a separate **shared** repository
- Automate branch protection setup (no manual clicking)

### Shared repo (reusable workflows/actions)

This project expects a second repository, referred to below as:

- **`test-cpp-shared-actions`** [link](https://github.com/saba-innowise/test-cpp-shared-actions)

That repo contains reusable GitHub Actions components, for example:
- A reusable workflow for build/test across OS matrix
- A reusable workflow for linting with clang-format
The main repo calls into these via:

- `uses: saba-innowise/test-cpp-shared-actions/.github/workflows/<workflow>.yml@main`

---

## Versioning and package references

### Semantic versioning
- Versions follow **SemVer**: `X.Y.Z`
- The version must be explicitly bumped in the PR (no “auto bump on merge”)
- Bumping is done via the `VERSION` file located under the `tether_sum` directory

### Conan reference formats
- **Release candidate (pre-merge)**:
  - `mylib/<X.Y.Z>-dev-<short-sha>`
  - uploaded to remote: **`conan-rc`**
- **Final release (post-merge)**:
  - `mylib/<X.Y.Z>`
  - uploaded to remote: **`conan-stable`**

> `<short-sha>` is derived from the PR HEAD commit, ensuring each RC is unique and traceable.

> For convenience both remotes share the same package registry, which is trivial to split.

---

## Conan packaging requirements (Conan 2)

### Profiles (required)
Conan 2 profiles exist per platform/toolchain and capture:
- `os`
- `arch`
- `compiler`
- `build_type`

Profiles are stored in `conan-profiles/` and used in CI to ensure consistent toolchain settings.

---

## GitHub Actions workflows (what happens when)

### 1) Pull Request verification (every PR)

Triggered on all Pull Requests to the main branch.

**Enforced rules:**
- **Up-to-date with `main`**
  - PR fails if the branch is behind `main` (requires rebase/merge-from-main before merge)
- **Linear history**
  - enforced via branch protection (“Require linear history”)

**Checks run on a matrix (Linux/Windows/macOS):**
- `clang-format` check
- conan create (with tests enabled)

**Merge gating:**
- The PR cannot be merged unless all required checks are green (branch protection requires them).

---

### 2) Label-driven workflow: `verify`

Applying the **`verify`** label triggers **integration/E2E tests**.

- CI builds a **consumer** CMake project that:
  1. Builds the tether_sub library
  2. Installs the library via Conan:
     - `conan install --requires=tether_sum/vX.Y.Z ...`
  3. Links against the package and runs a tiny executable that calls `sum()`

---

### 3) Label-driven workflow: `publish` (pre-merge RC publishing)

Applying the **`publish`** label triggers creation and upload of **release-candidate packages**.

**Pre-merge requirements:**
- Build packages for the full OS matrix (Linux/Windows/macOS)
- Upload to **`conan-rc`** with reference:
  - `tether_sum/<X.Y.Z>-dev-<short-sha>`
- **Block if release already exists in stable**
  - CI checks whether `tether_sum/<X.Y.Z>` already exists in **`conan-stable`**
  - If it exists, the workflow fails to prevent accidental duplicate releases

---

### 4) Release on merge (PR with `publish` label)

When a PR that carries the `publish` label is merged to `main`, CI performs the final release steps:

1. Build Conan packages for the full OS matrix
2. Upload final packages to **`conan-stable`** as:
   - `tether_sum/<X.Y.Z>`
3. Create git tag:
   - `vX.Y.Z`
4. Create a GitHub Release for `vX.Y.Z`

---

## Secrets and configuration

To publish Conan packages and create releases, GitHub Actions needs credentials.

### Required GitHub variables and secrets (configured for `stable` and `rc` environments)
- `CONAN_REMOTE_NAME` — remote name (`conan-stable` or `conan-rc`)
- `CONAN_REMOTE_URL` — remote URL
- `CONAN_REMOTE_USERNAME` — username/token id
- `CONAN_REMOTE_PASSWORD` — password/token

Package registry was set up on GitLab, as they recently started rolling out support for Conan 2.

---

## PR checklist

Before opening a PR:
- [ ] Bump `X.Y.Z` in the authoritative version file
- [ ] Ensure formatting passes (`clang-format`)
- [ ] Ensure everything builds successfully and unit tests pass

To trigger additional CI behaviors:
- Add label **`verify`** to run consumer integration tests
- Add label **`publish`** to publish RC packages to `conan-rc` (and enforce stable-version uniqueness)

---

## Expected release flow (end-to-end)

1. Developer opens PR with a version bump
2. PR checks run and must pass (multi-OS matrix)
3. Reviewer adds `verify` → consumer integration tests run
4. Reviewer adds `publish` → RC packages appear in `conan-rc` as `tether_sum/X.Y.Z-dev-<short-sha>`
   - CI fails if `tether_sum/X.Y.Z` already exists in `conan-stable`
5. PR is approved and merged
6. Merge triggers release workflow:
   - uploads `tether_sum/X.Y.Z` to `conan-stable`
   - creates `vX.Y.Z` tag
   - creates GitHub Release
