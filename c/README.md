# Skapa ett nytt C-projekt

## Förutsättningar

* Pythonpaketet `cmake-init`
* cmake
* Valfritt: `clangd` 

## Procedur

* Exekvera `cmake-init --c <Projektnamn>`-.
* Kopiera scriptet`patch-all.py` till projektroten och exekvera det (exakt en gång).
* Valfritt: Skapa mappen `include` i projektroten. Där kan header-filer läggas om den strukturen önskas.
* Exekvera `cmake --preset default`
* Ta bort filen `.clangd`. Den ersätts av `compile_commands.json`, som `cmake` skapar efter patchen och som används av editorns LSP-integration.
* Gå till mappen `./build` och exekvera `make` elle `make run`.
