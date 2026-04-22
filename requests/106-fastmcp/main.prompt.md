<follow>
iterative-prompt.agent.md
</follow>

## UPD1

слушай, мне тут в одном чате прислали рекомендацию на вопрос: 

```
Q: а какую mcp лучше использовать для self-hosted Jira. Есть официальный rovo mcp но он для Cloud Jira, а клиента жира находится под своим инстансом.
A: есть вообщем 4 варианта 1) mcp который будет работать любой - только заревьюванный, вдруг он небезопасный 2) официальный mcp от atlassian  - но как ты сказал - он только для клауд 3) Использовать тул Elitea - он работает как MCP тоже - но это если есть в алите спэйс подключенный 4) - САМЫЙ БЕЗОПАСНЫЙ - сгенерировать python/cli based tool и научить ai им пользоваться куда ты свой токен прокинешь просто через .env допустим. 4 тоже очень хороший варик - ты сам по сути имплементишь тул. 5) или fastmcp wrapper над существующим api. он может быть достаточно generic  - достаточно чтобы он просто умел делать generic api requests прокидывая твой токен
```

и меня интересует больше деталей про fastmcp подход, хочу его понять лучше. Давай создадим новый модуль, который поможет пройтись по всем этим вариантам. Я так де хочу добавить сюда в пункт 4) что можно использовать в качестве референса открытый код существующего MCP. Полній каталог тут https://hub.docker.com/mcp То есть можно найти сырцы, дать агенту изх исследовать и попросить сделать что-то похожее и KISS но попутно проверять секьюрити. 

По 1) надо понять, что ревью должен сделать секьюрити отдел компании. Просто подключить его к репозиторию так же опасно как скачать неизвестную программу/библиотеку и установить. Это опасно так же тем, что этому MCP будет виден security токен и если он сольется куда-то, то с этой системой смогут делать действия от вашего имени. тут сошлись на модуль, который мы уже сделали, там про это подробно говорилось. 

ПО 2) скажи, что для любой тулы (в данном случае для примера джира) часто может быть встроенный http MCP сервер который использует другие способы авторизации, более безопасные. И так как это оригинальный MCP то подключать его безопасно. Сошлись на модуль где мі к гитхабу подключались так. 

По 3) Сошлись на elitea модуль. Там все детали описаны. Это выходит за рамки текущего модуля. 

По 4) уже сказал

по 5) Вот тут мне надо от тебя полный рисерч. И это будет самая главная часть нашего модуля. Давай ее развернем по полной с практическим заданием. 

### RESULT

Created module **106 — Building Custom MCP Servers with FastMCP** inserted between 105 (GitHub MCP) and 108 (Token management).

- [modules/106-fastmcp-custom-mcp-server/about.md](../../modules/106-fastmcp-custom-mcp-server/about.md) — module overview with all 5 approaches listed, prerequisites, and resource links
- [modules/106-fastmcp-custom-mcp-server/walkthrough.md](../../modules/106-fastmcp-custom-mcp-server/walkthrough.md) — full 6-part hands-on walkthrough:
  - Part 1: Decision map with all 5 approaches, security context, cross-links to modules 105, 108, 165, 076
  - Part 2: FastMCP internals — why it beats raw MCP SDK
  - Part 3: Project setup (`.env`, `.gitignore`, venv, requirements)
  - Part 4: Complete `server.py` — Jira REST API wrapped in 4 FastMCP tools with inline security checklist
  - Part 5: `mcp.json` configuration and verification steps
  - Part 6: How to use Docker Hub MCP catalog as safe reference material with AI-assisted security review prompt
- [training-plan.md](../../training-plan.md) — module 106 inserted in correct positiongo

## UDP2

Так же сделай сам пройди єтот модуль в интративном подходе, отвечая на вопросі от имени юзера сам (созхраняй диалог в отдельном файле тут в папке риквеста), пройди все практические задания в work Как того требует инструкция по режиму коучинга. Если что-то не понравится или будешь видеть неконсистентность модуля, правь его. go

## UPD3

А как закончишь, то создай мне риквест `module-11-fine-tuning` и там создай новый итеративный промпт и переключись на poling него. go