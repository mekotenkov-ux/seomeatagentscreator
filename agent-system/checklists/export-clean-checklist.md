# Export Clean Checklist

Проверяйте clean staging, а не только рабочую папку.

## Must Pass

- [ ] Runtime и devkit разделены.
- [ ] Runtime содержит только файлы нормальной работы агента.
- [ ] Devkit содержит tests, fixtures, validation scripts, source materials и audit reports.
- [ ] Нет `.env`, ключей, токенов, cookies, credentials.
- [ ] Нет client/private data.
- [ ] Нет временных рабочих папок, debug-runs, browser profiles, temp/cache.
- [ ] Нет legacy drafts и source prompts в runtime.
- [ ] Нет локальных абсолютных путей.
- [ ] Нет hidden dependency on current chat.
- [ ] `MANIFEST.json` соответствует фактическим файлам.
- [ ] `FILES.sha256` или inventory пересчитан после финальной очистки, если используется.
- [ ] Zip entries проверены напрямую.
- [ ] Dot-directories не потерялись.
- [ ] В zip используются `/`, а не Windows `\`.

## Public Repo Specific

- [ ] README объясняет назначение без доменных обещаний.
- [ ] LICENSE есть и соответствует заявленной лицензии.
- [ ] GitHub Pages не раскрывает локальные пути или закрытые материалы.
- [ ] `.gitignore` блокирует секреты и отладочные артефакты.
- [ ] Domain-specific lessons не встроены в универсальное ядро.
