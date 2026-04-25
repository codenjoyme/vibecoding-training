<follow>
iterative-prompt.agent.md
</follow>

## UPD1

Давай сделаем модуль тренинговый, следуя инструкции по созданию модулей, который будет с индексом 650 и делать следующее. Вот у нас есть целый модуль про [400-installing-mcpyrex-mcp-python-toolbox](../../modules/400-installing-mcpyrex-mcp-python-toolbox/about.md) но там мне интересно только пару тулов, которые про `winapi` давай сделаем для них тут `skill.md` внутри модуля в на основе тех же скриптов, этот `skill` будет настраивать `MCP` сервер для работы через `MCP` как сделано в `mcpyrex`, `virtualenv` ставить питон и все такое прочее. Прям в папке скила (весь питоновский стафф пусть будет загитигнорен). Все что делают те тулы в `mcpyrex` пусть делает и тут. С минимумом изменений. Для этого форкни `mcpyrex` в `work` папку и исследуй его там как референс. Потом создай `modules/650-winapi/tools/SKILL.md` и рядом с ним весь остальной стафф в папке `modules/650-winapi/tools/scipts/`. Ну и пропиши в `skill.md` как настраивать `mcp.json` файл для `cursor` и `copilot` на `vscode` помня что там `mcpServers` и `servers` отличия в имени поля. И инструцию по запуску `MCP` в идеешках тоже надо, но это уже все пойдет в `walkthrough.md` модуля.   

`Tool` по производству скриншотов сделай таким, который сможет делать скриншоты не всего экрана, а либо заданного `child window`, либо в заданных координатах (`x1`, `x2`, `y1`, `y2`). Ну чтобы я мог универсально делать скриншоты в разных местах. Приатачивай скриншоты так, как мы это делали в [107-mcp-image-viewer](../../modules/107-mcp-image-viewer/about.md), атачем к ответу `MCP`. Пусть будет 2 команды: `screenshot window <window_name>` и `screenshot area <x1> <y1> <x2> <y2>`. И там и там результатом будет сохраненный в папку `output` скриншот с именем, включающим название окна или координаты. И приатаченный к ответу. 

Так же мне в дополнение к тем `tools` что есть нужны тулы для работы с мышью и клавиатурой (с клавиатурой вроде как там есть что-то по хоткеям, даже сценарии писать можно - мне то все точно надо). По мыши - прям всякие `drag and drop` чтобы можно было сделать. 

Короче главная идея, чтобы я могу дать тебе возможность через `MCP` давать доступ к моей операционке, и ты все мог прокликать сам, глядя за скриншотами. 

Тестируй все сам, я наблюдаю за твоей работой. Go.

### RESULT

Created module **650-winapi** — a self-contained Python MCP server that exposes
WinAPI tools (screenshots, mouse, keyboard, clipboard, process & window
inspection) over stdio. Used `work/400-task/mcp_server/tools/lng_winapi/` as
reference and ported the relevant tools into a single `server.py`.

Files created:

- [modules/650-winapi/about.md](../../modules/650-winapi/about.md) — module overview, prerequisites, learning outcome
- [modules/650-winapi/walkthrough.md](../../modules/650-winapi/walkthrough.md) — 6-part hands-on (inspect → install → boot test → register VS Code → register Cursor → drive desktop)
- [modules/650-winapi/tools/SKILL.md](../../modules/650-winapi/tools/SKILL.md) — AI-facing skill reference with both `servers` (VS Code) and `mcpServers` (Cursor) config blocks
- [modules/650-winapi/tools/scripts/server.py](../../modules/650-winapi/tools/scripts/server.py) — single-file MCP server with 11 tools registered through a `TOOLS` dict
- [modules/650-winapi/tools/scripts/install.ps1](../../modules/650-winapi/tools/scripts/install.ps1) — bootstrap (creates `.venv`, falls back to `virtualenv` if `venv` module is unavailable, idempotent)
- [modules/650-winapi/tools/scripts/run.ps1](../../modules/650-winapi/tools/scripts/run.ps1) — launcher used by `mcp.json` (forces UTF-8 stdio)
- [modules/650-winapi/tools/scripts/requirements.txt](../../modules/650-winapi/tools/scripts/requirements.txt) — `mcp`, `mss`, `pywin32`, `psutil`, `pyautogui`, `pyperclip`, `pywinauto`, `Pillow`
- [modules/650-winapi/tools/scripts/test_client.py](../../modules/650-winapi/tools/scripts/test_client.py) — Python smoke-test client (initialize → tools/list → screenshot_area → list_processes → clipboard round-trip)
- [modules/650-winapi/tools/scripts/output/](../../modules/650-winapi/tools/scripts/output/) — auto-created folder for saved screenshots (gitignored except `.gitkeep`)
- [modules/650-winapi/tools/.vscode/mcp.json](../../modules/650-winapi/tools/.vscode/mcp.json), [modules/650-winapi/tools/.cursor/mcp.json](../../modules/650-winapi/tools/.cursor/mcp.json) — ready-to-copy IDE configs
- [modules/650-winapi/tools/.gitignore](../../modules/650-winapi/tools/.gitignore) — keeps `.venv/`, `__pycache__/`, `output/` out of git
- [training-plan.md](../../training-plan.md) — added entry for module 650 between 620 and 900

Tools exposed by the server:
1. `screenshot_window` — capture window by title/class substring → MCP image content + saved PNG
2. `screenshot_area` — capture rectangle `(x1,y1)-(x2,y2)` → MCP image content + saved PNG
3. `mouse_move`, `mouse_click`, `mouse_drag` (drag-and-drop) — pyautogui-based
4. `send_hotkey` — port of mcpyrex's hotkey tool: hotkeys (`^t`, `%{F4}`), named keys, text, sequences (`[{type, value}, ...]`); optional `pid` to focus a process first
5. `clipboard_get` / `clipboard_set` — pyperclip
6. `list_processes`, `window_tree`, `get_window_content` — direct ports of mcpyrex tools (psutil + ctypes/pywinauto)

End-to-end test verified:
- `install.ps1` succeeds (after fallback to `virtualenv` for embedded Python)
- `test_client.py` confirms `initialize` returns `serverInfo: winapi-mcp`, `tools/list` returns all 11 tools, `screenshot_area` returns a 13 KB base64 PNG saved to `output/`, `list_processes filter=python` returns matches, clipboard round-trip works
