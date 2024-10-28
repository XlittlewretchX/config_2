# Визуализатор зависимостей

Инструмент командной строки Python для визуализации графика зависимостей пакетов npm (Node.js) с помощью Graphviz.

## Функции

- Извлекает метаданные пакета из реестра npm.
- Рекурсивно извлекает зависимости до заданной глубины.
- Создает график зависимостей в Graphviz dotformat.
- Выводит код Graphviz как на консоль, так и в указанный файл.
- Комплексные тесты, охватывающие все функциональные возможности.

**Модули Python:** Установите через `pip install -r requirements.txt`.

## Использование

python main.py <graph_path> <package_name> <result_file_path> <max_depth> <repository_url>
- graph_path: Путь к исполняемому файлу Graphviz dot (например, a.dot).
- имя_пакета: имя пакета npm для анализа (например, express).
- result_file_path: путь к выходному файлу DOT (например, express_dependencies.dot).
- max_depth: Максимальная глубина для анализа зависимостей (например, 2).
- repository_url: URL-адрес хранилища пакета (например, https://github.com/expressjs/express).

Например:

python main.py a.dot express express_dependencies.dot 2 https://github.com/expressjs/express