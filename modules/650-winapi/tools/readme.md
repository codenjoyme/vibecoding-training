# WinAPI MCP — Hands-On Reproduction Guide (Snow on google.com)

> Это **человекочитаемый мануал** на русском по мотивам реального эксперимента
> "AI агент сам открывает Chrome и через DevTools Console устраивает снегопад
> на google.com". Если [SKILL.md](SKILL.md) — это для агента, то этот файл —
> для вас. Идите по шагам, скриншоты ниже служат ориентирами.

---

## Что вы получите в финале

![Финальный кадр: снег идёт на google.com, рядом видно как агент рассуждает](img/00-final-result.png)

Над страницей `google.com` поверх UI летят белые снежинки разного размера.
Логотип, поле поиска и кнопки продолжают работать (`pointer-events:none` у
canvas-а). В правой панели — чат с агентом, где он сам ищет процесс Chrome,
шлёт хоткеи, кладёт JS в буфер, разрешает paste-protection и снимает
финальный скриншот.

Чтобы повторить это, нужно:
1. Установить и зарегистрировать MCP-сервер `winapi-mcp` (один раз).
2. Включить его инструменты в чате.
3. Дать агенту задание словами — он сам прокликает.

---

## Шаг 1 — Установка сервера

Из корня репозитория, в **PowerShell**:

```powershell
pwsh -ExecutionPolicy Bypass -File ./modules/650-winapi/tools/scripts/install.ps1
```

Скрипт идемпотентный: создаст `.venv/` рядом с `server.py`, обновит pip,
поставит зависимости из `requirements.txt`. Если в вашей сборке Python
отсутствует модуль `venv` — он автоматически переключится на `virtualenv`.

> Требуется **Python 3.10+** и **Windows**. На macOS/Linux сервер не
> запустится (зависит от `pywin32` / `pywinauto`).

---

## Шаг 2 — Регистрация сервера в VS Code

Откройте `.vscode/mcp.json` в корне рабочего пространства и добавьте блок
`winapi-mcp`. Если файла нет — создайте; обратите внимание, что у VS Code
ключ `"servers"` (у Cursor было бы `"mcpServers"`). Готовый шаблон лежит в
[`config/.vscode/mcp.json`](config/.vscode/mcp.json) (для Cursor — в
[`config/.cursor/mcp.json`](config/.cursor/mcp.json)).

```jsonc
{
  "servers": {
    "winapi-mcp": {
      "type": "stdio",
      "command": "powershell",
      "args": [
        "-ExecutionPolicy", "Bypass",
        "-File", "./modules/650-winapi/tools/scripts/run.ps1"
      ]
    }
  }
}
```

Сохраните файл. Над JSON-блоком VS Code покажет инлайн-панель управления:
**Start | Stop | Restart | N tools**. Нажмите **Start**.

В логе **Output → Model Context Protocol** должно появиться
`Discovered 11 tools` — это сигнал что сервер запустился и MCP-handshake
прошёл успешно.

![mcp.json с winapi-mcp и логом "Discovered 11 tools"](img/06-mcp-server-registered.png)

На скриншоте подсвечены: запись `winapi-mcp` в `servers`, инлайн-кнопка
`Running | 11 tools` и строка `Discovered 11 tools` в логе.

---

## Шаг 3 — Включение инструментов в чате

Откройте Copilot Chat → переключите в **Agent Mode** → нажмите иконку
гаечного ключа (Configure Tools). В дереве найдите ветку `winapi-mcp` и
убедитесь что все 11 чекбоксов отмечены:

![Configure Tools — все 11 winapi-mcp инструментов включены](img/07-tools-enabled.png)

Список инструментов (см. [SKILL.md](SKILL.md) для подробностей):

- `screenshot_window`, `screenshot_area` — скриншоты
- `mouse_move`, `mouse_click`, `mouse_drag` — мышь
- `send_hotkey` — клавиатура (хоткеи / именованные клавиши / текст /
  последовательности)
- `clipboard_get`, `clipboard_set` — буфер обмена
- `list_processes`, `window_tree`, `get_window_content` — инспекция окон

> **Если только что добавили сервер, а в списке тулзов пусто** — VS Code
> подтягивает MCP-серверы при старте чат-сессии. Откройте новый чат
> (`+` рядом с моделью), либо через `Configure Tools` явно подтвердите
> новый сервер.

---

## Шаг 4 — Запуск демо

Откройте новый чат в Agent Mode и попросите агента:

> Открой Chrome на `google.com`, открой DevTools Console и вставь туда
> JavaScript, который рисует падающий снег поверх страницы. Делай скриншоты
> на каждом шаге, объясняй что видишь.

Дальше агент пройдёт примерно такой маршрут (каждый шаг → один MCP-вызов):

### 4.1. Найти и сфокусировать Chrome

```
list_processes filter=chrome only_with_windows=true
→ pid=78812
send_hotkey pid=78812 key=ESC      # побочный эффект _focus_pid → set_focus()+restore()
screenshot_window window_name="Google Chrome"
```

![01 — Chrome со страницей google.com на переднем плане](img/01-chrome-google-loaded.png)

### 4.2. Открыть DevTools, перейти на Console

```
send_hotkey hotkey="^+i"           # Ctrl+Shift+I — DevTools (вкладка Elements по умолчанию)
screenshot_window window_name="Google Chrome"
```

![02 — DevTools открыт, активна вкладка Elements](img/02-devtools-elements.png)

```
send_hotkey hotkey="^+j"           # Ctrl+Shift+J — переключение на Console
screenshot_window window_name="Google Chrome"
```

![03 — Активна вкладка Console, поле ввода готово](img/03-console-tab-ready.png)

> ⚠️ Если DevTools уже был открыт — `^+j` его закроет. Тогда нажмите ещё раз.

### 4.3. Подложить JS в буфер и вставить

JS-payload (569 символов, IIFE — рисует canvas и анимирует 200 снежинок):

```js
(()=>{const c=document.createElement('canvas');Object.assign(c.style,{position:'fixed',inset:'0',pointerEvents:'none',zIndex:'2147483647'});c.width=innerWidth;c.height=innerHeight;document.body.appendChild(c);const x=c.getContext('2d');const f=Array.from({length:200},()=>({x:Math.random()*c.width,y:Math.random()*c.height,r:1+Math.random()*3,s:0.5+Math.random()*1.5}));(function t(){x.clearRect(0,0,c.width,c.height);x.fillStyle='white';for(const k of f){x.beginPath();x.arc(k.x,k.y,k.r,0,7);x.fill();k.y+=k.s;if(k.y>c.height)k.y=0;}requestAnimationFrame(t);})();})();
```

```
clipboard_set text="<JS выше>"
send_hotkey pid=78812 sequence=[
  {type: hotkey, value: "^v"},
  {type: delay,  value: 400},
  {type: key,    value: "ENTER"}
]
```

### 4.4. Преодолеть paste-protection (один раз для origin)

Chrome по умолчанию не даёт первый paste в DevTools Console (защита от
self-XSS). На первом скриншоте Console выйдет жёлтая полоса:

![04 — предупреждение "Don't paste code into the DevTools Console"](img/04-paste-protection-warning.png)

Снимаем разрешением:

```
send_hotkey pid=78812 sequence=[
  {type: text,  value: "allow pasting"},
  {type: delay, value: 200},
  {type: key,   value: "ENTER"},
  {type: delay, value: 300},
  {type: hotkey, value: "^v"},
  {type: delay,  value: 400},
  {type: key,    value: "ENTER"}
]
```

### 4.5. Финальный скриншот — снег идёт

```
send_hotkey pid=78812 key=ESC      # снова сфокусировать Chrome поверх остального
screenshot_window window_name="Google - Google Chrome"
```

![05 — снег идёт на google.com](img/05-snow-running.png)

В консоли видно вставленный код, под ним `undefined` (IIFE ничего не
возвращает — это нормально), а поверх UI Google падают снежинки.

---

## Уроки, добытые на этом эксперименте

- **`screenshot_window` снимает экранный bbox окна, а не bitmap.** Если
  целевое окно перекрыто другим — на снимке будет то, что сверху.
  Перед каждым важным скриншотом фокусьте окно: `send_hotkey pid=...` (любой
  безопасный хоткей вроде ESC), у `_focus_pid` есть побочный эффект
  `set_focus()` + `restore()`.
- **Хоткей через `pid` стабильнее глобального.** При `pid` сервер сначала
  фокусит окно, и только потом отправляет клавиши — никаких "ушло не туда".
- **`Ctrl+Shift+J` тоглит Console.** Если DevTools уже открыт на Console,
  второе нажатие закроет его. Иногда нужно слать дважды — иногда не нужно
  слать вообще. Скриншотом проверяйте.
- **Paste-protection в Chrome — per-origin.** Один раз ввели `allow pasting`
  на `google.com` — дальше в этой сессии Chrome `^v` работает молча.
- **`sequence` с `delay` решает гонки.** Без `delay` ENTER может прилететь
  раньше, чем `^v` успел вставить длинный текст.

---

## Безопасность

Этот сервер **физически управляет вашей машиной**: двигает мышь, печатает
в любое сфокусированное окно, читает экран. Включайте его только для тех
чатов, где вы хотите UI-автоматизацию, и выключайте/удаляйте из `mcp.json`
когда закончили. У агента нет понятия "это окно с паролем" — если
менеджер паролей сфокусирован, и `send_hotkey` шлёт текст, текст уйдёт туда.

---

## Куда идти дальше

- [SKILL.md](SKILL.md) — полная справка по всем инструментам и их параметрам
  (для агента и для глубокого чтения).
- [walkthrough.md модуля](../walkthrough.md) — пошаговый разбор всего, от
  установки до собственных команд.
- [scripts/server.py](scripts/server.py) — посмотрите как добавить свой
  собственный MCP-инструмент рядом с существующими 11.
