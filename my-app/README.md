# my-app

## Запуск тестів локально

### Unit тест
pytest tests/unit

### API тест
pytest tests/integration/api

### DB тест
pytest tests/integration/database

### E2E тест
pytest tests/e2e

### Docker
docker-compose -f docker-compose.test.yml up -d

### CI/CD
Автоматичний запуск через GitHub Actions
