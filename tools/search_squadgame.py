import os
import fnmatch


def find_file(filename, search_path):
    """
    Рекурсивно ищет файл с заданным именем в указанном пути поиска.

    :param filename: Имя файла для поиска
    :param search_path: Путь, в котором следует искать файл
    :return: Абсолютный путь к файлу, если найден, иначе None
    """
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def find_squad_exe():
    drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
    filename = "SquadGame.exe"

    for drive in drives:
        print(f"Searching in {drive}...")
        path = find_file(filename, drive)
        if path:
            return path
    return None


# Запуск поиска Squad.exe
squad_exe_path = find_squad_exe()
if squad_exe_path:
    print(f"Squad.exe found at: {squad_exe_path}")
else:
    print("Squad.exe not found.")
