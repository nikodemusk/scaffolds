# Scaffolds

This repository contains minimal scaffolds for various project types.
Currently included:

* **C**
* **Lua**
* **Python**
* (planned) **LaTeX**

Each scaffold initially contains only basic formatting/configuration files.
The long-term goal is to provide fully structured, script-generated project
skeletons that can be deployed anywhere on the system.

---

## Goals

To maintain a unified and extensible structure for initializing new development
projects across multiple languages and tools.

---

## TODO — Future Improvements

### 1. Scaffold Generation Scripts

Create language-specific scripts that:

* Accept a destination path as argument
* Generate a project folder with predefined structure
* Copy the base files from the scaffold directory
* Optionally initialize Git and create a first commit

Proposed scripts:

* `generate_c_project.sh`
* `generate_lua_project.sh`
* `generate_python_project.sh`
* `generate_latex_project.sh` (once LaTeX scaffold is added)

### 2. Expand Project Structures

Add fuller directory trees inside each scaffold:

**C**

* `src/`
* `include/`
* `tests/`
* Optional: `CMakeLists.txt`

**Lua**

* `src/`
* `tests/`
* Optional: LuaRocks manifest

**Python**

* `src/<package_name>/`
* `tests/`
* Optional: `pyproject.toml`, virtual env setup

**LaTeX**

* `main.tex`
* `sections/`
* `figures/`
* `bib/`
* `Makefile` or `latexmkrc`

### 3. Script Enhancements

Eventually add:

* Interactive prompts (project name, license, include tests?)
* Template variable substitution (e.g. project name inserted into files)
* Optional flags (`--with-git`, `--minimal`, `--cmake`, `--poetry`, etc.)

### 4. Repository Improvements

* Add a top-level installation guide for using the scripts
* Document how each scaffold is structured
* Provide language-specific usage examples
* Add CI checks for scaffold scripts (shellcheck or similar)

### 5. Integrate LaTeX Scaffold

* Move existing LaTeX template folder into `scaffolds/latex/`
* Add formatting files (`latexmkrc`, stylings, Makefile)
* Prepare generation script similar to other languages

### 6. Optional: GitHub Template Repository

Convert this repo into a GitHub "Template repository"
→ making it directly forkable as a starting point for others.

---
