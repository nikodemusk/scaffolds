#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def patch_cmake(file_path: Path):
    text = file_path.read_text()

    m = re.search(r"project\(\s*([A-Za-z0-9_-]+)", text)
    if not m:
        raise RuntimeError("Kunde inte hitta projektets namn")
    project_name = m.group(1)

    m = re.search(r"add_executable\(\s*(" + re.escape(project_name) + r"_exe)\b", text)
    if not m:
        raise RuntimeError("Kunde inte hitta exe-target")
    exe_target = m.group(1)

    def add_include(match):
        block = match.group(0)
        return block.replace(
            ")", '    "\\$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"\n)'
        )

    text = re.sub(
        r"target_include_directories\([^)]*\)",
        add_include,
        text,
        count=1,
        flags=re.DOTALL,
    )

    insertion = f"""add_custom_target(
    run
    COMMAND $<TARGET_FILE:{exe_target}>
    DEPENDS {exe_target}
    WORKING_DIRECTORY ${{PROJECT_SOURCE_DIR}}
)
"""
    text = re.sub(
        r"(target_compile_features\(" + re.escape(exe_target) + r"[^\)]*\)\n)",
        r"\1" + insertion,
        text,
    )

    file_path.write_text(text)
    print(f"Patchat {file_path} för projektet {project_name}")


def patch_clang_format(file_path: Path):
    text = file_path.read_text().splitlines()
    if len(text) >= 2 and "Language:" in text[1]:
        text[1] = "Language: C"
    for i, line in enumerate(text):
        if "AfterFunction:" in line:
            text[i] = "  AfterFunction: false"
    for i, line in enumerate(text):
        if line.strip().startswith("BreakBeforeBraces:"):
            text[i] = "BreakBeforeBraces: Attach"
    text = [line for line in text if line.strip() != "..."]
    file_path.write_text("\n".join(text))
    print(f"Patchat {file_path}")


def patch_clang_tidy(file_path: Path):
    text = file_path.read_text().splitlines()
    if len(text) >= 4:
        text.insert(4, "  -readability-identifier-length,\\")
    for i, line in enumerate(text):
        if "readability-*" in line and not line.strip().startswith("-"):
            text[i] = line.replace("readability-*", "-readability-*")
    file_path.write_text("\n".join(text))
    print(f"Patchat {file_path}")


def patch_presets(file_path: Path):
    text = file_path.read_text().splitlines()

    preset_block = [
        "    {",
        '      "name": "default",',
        '      "description": "Default configure preset",',
        '      "generator": "Unix Makefiles",',
        '      "binaryDir": "${sourceDir}/build",',
        '      "cacheVariables": {',
        '        "CMAKE_EXPORT_COMPILE_COMMANDS": "ON",',
        '        "CMAKE_C_FLAGS": "-Wall -pedantic"',
        "      }",
        "    },",
    ]

    for i, line in enumerate(text):
        if '"configurePresets": [' in line:
            for j, block_line in enumerate(preset_block):
                text.insert(i + 1 + j, block_line)
            break

    file_path.write_text("\n".join(text))
    print(f"Patchat {file_path}")


if __name__ == "__main__":
    base_dir = Path.cwd()
    cmake_file = base_dir / "CMakeLists.txt"
    clang_format_file = base_dir / ".clang-format"
    clang_tidy_file = base_dir / ".clang-tidy"
    presets_file = base_dir / "CMakeUserPresets.json"

    print("Detta script kommer att patcha följande filer i katalogen:")
    print(f" - {cmake_file}")
    print(f" - {clang_format_file}")
    print(f" - {clang_tidy_file}")
    print(f" - {presets_file}")
    choice = input("Vill du fortsätta? (j/n): ").strip().lower()

    if choice == "j":
        patch_cmake(cmake_file)
        patch_clang_format(clang_format_file)
        patch_clang_tidy(clang_tidy_file)
        patch_presets(presets_file)
        print("Alla patchar är klara!")
    else:
        print("Avbrutet, inga ändringar gjorda.")
