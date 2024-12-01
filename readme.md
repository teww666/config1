# Shell Emulator

## Описание
Эмулятор оболочки ОС для работы с виртуальной файловой системой. Реализует базовые команды UNIX-подобной системы и работает с архивом виртуальной файловой системы в формате `.tar`. Предоставляет графический интерфейс (GUI) для взаимодействия.

---

## Возможности
- **Работа с виртуальной файловой системой**:
  - Открытие и редактирование архива `.tar` без необходимости распаковки пользователем.
- **Поддерживаемые команды**:
  - `ls` – отображение содержимого текущей директории.
  - `cd` – смена текущей директории.
  - `touch` – создание нового файла.
  - `chown` – изменение владельца и группы файла (эмулируется на Windows).
  - `find` – поиск файла по имени.
  - `exit` – завершение работы эмулятора.
- **Графический интерфейс (GUI)**:
  - Ввод команд в текстовом поле, аналогично терминалу.
  - Вывод результатов выполнения в окно вывода.
- **Логирование**:
  - Логирует все действия пользователя в XML-файл с указанием команды и времени выполнения.

---

## Установка и запуск

### Зависимости
Убедитесь, что установлены следующие зависимости:
- Python 3.8+
- PyQt5

Установить PyQt5 можно с помощью `pip`:
```bash
pip install PyQt5
```
Запуск эмулятора
Создайте XML-файл конфигурации, например, config.xml:
```xml
<config>
    <username>user</username>
    <hostname>localhost</hostname>
    <filesystem>filesystem.tar</filesystem>
    <logfile>log.xml</logfile>
</config>
```
Подготовьте архив виртуальной файловой системы, например:
```bash
mkdir -p home/user/docs
echo "Hello World" > home/user/docs/hello.txt
tar -cvf filesystem.tar home
```
Запустите эмулятор:
```bash
python shell_emulator.py
```
Структура проекта
```plaintext
.
├── shell_emulator.py      # Основной файл эмулятора
├── test_shell_emulator.py # Тесты для эмулятора
├── config.xml             # Конфигурационный файл
├── filesystem.tar         # Виртуальная файловая система
├── log.xml                # Лог-файл с действиями пользователя
```
Тестирование
Функции эмулятора покрыты тестами. Запустите тесты с помощью следующей команды:

```bash
python test_shell_emulator.py
```
Пример вывода успешных тестов:
```plaintext
Testing `ls` command...
✔ List root directory - PASSED
Testing `cd` command...
✔ Change to 'home' - PASSED
✔ Change to 'user' - PASSED
✔ Go back to parent directory - PASSED
Testing `touch` command...
✔ Create new file 'new_file.txt' - PASSED
✔ List directory after creating file - PASSED
Testing `find` command...
✔ Find 'file2.txt' - PASSED
Testing `chown` command...
✔ Change ownership of 'file1.txt' - PASSED
Cleaning up...
✔ Cleanup completed - PASSED
Поддерживаемые команды
Команда	Описание
ls	Вывод содержимого текущей директории.
cd	Смена текущей директории. Поддерживаются .. и абсолютные пути.
touch	Создание нового файла.
chown	Изменение владельца и группы файла. Эмулируется на Windows.
find	Поиск файла по имени в указанной директории.
exit	Завершение работы эмулятора.
```
![Скриншот результата](photo/Снимок%20экрана%202024-12-01%20005603.png)# config1
