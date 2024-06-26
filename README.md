GUI --- main.py

# SEED RFS

SEED RFS - это проект, который позволяет автоматически запускать игру Squad, подключаться к указанным серверам и выполнять определенные действия с использованием библиотеки pyautogui.

## Функции

- Автоматический поиск и запуск SquadGame.exe.
- Подключение к серверам по их ID.
- Автоматизация ввода текста и кликов мыши.
- Возможность создания исполняемого файла для автоматического запуска скрипта.
- Логи выполнения отображаются в графическом интерфейсе.
- Возможность включения или выключения автоматического завершения работы системы.

## Требования

- Python 3.8 или выше
- Библиотеки:
  - `tkinter`
  - `pyautogui`
  - `pyperclip`
  - `requests`
  - `pygame`
  - `Pillow`
  - `pyinstaller`

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/miskam-gg/seed_script.git
   ```

2. Перейдите в каталог проекта:
   ```bash
   cd seed_script
   ```

3. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   ```

4. Активируйте виртуальное окружение:

   - Windows:
     ```bash
     .venv\Scripts\activate
     ```

   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

5. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

1. Запустите графический интерфейс:
   ```bash
   python GUI/main.py
   ```

2. В графическом интерфейсе выполните следующие шаги:
   - Укажите путь к файлу `SquadGame.exe`.
   - Выберите разрешение экрана.
   - Включите или выключите автоматическое завершение работы системы (shutdown).
   - Нажмите кнопку "Start Seed Script" для запуска скрипта.

## Создание исполняемого файла

1. В графическом интерфейсе нажмите кнопку "Create Seed EXE".
2. Укажите путь для сохранения исполняемого файла.

## Логи

Логи выполнения скрипта отображаются во вкладке "Logs" графического интерфейса.


## Авторы

- [miskam-gg](https://github.com/miskam-gg)

## Лицензия

Этот проект лицензирован под лицензией MIT.
