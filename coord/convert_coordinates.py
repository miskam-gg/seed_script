def convert_coordinates(x, y, original_resolution, target_resolution):
    """
    Преобразует координаты (x, y) из исходного разрешения в целевое разрешение.

    :param x: Координата x в исходном разрешении
    :param y: Координата y в исходном разрешении
    :param original_resolution: Кортеж (width, height) исходного разрешения
    :param target_resolution: Кортеж (width, height) целевого разрешения
    :return: Кортеж (new_x, new_y) преобразованных координат
    """
    original_width, original_height = original_resolution
    target_width, target_height = target_resolution

    # Рассчитываем соотношение
    width_ratio = target_width / original_width
    height_ratio = target_height / original_height

    # Преобразуем координаты
    new_x = int(x * width_ratio)
    new_y = int(y * height_ratio)

    return new_x, new_y

def main():
    # Запрос ввода координат
    original_x = int(input("Введите координату x в исходном разрешении: "))
    original_y = int(input("Введите координату y в исходном разрешении: "))

    original_resolution = (1920, 1080)  # Full HD
    target_resolution_2k = (2560, 1440)  # 2K
    target_resolution_low = (1280, 720)  # Low resolution

    # Преобразование координат для 2K монитора
    new_x_2k, new_y_2k = convert_coordinates(original_x, original_y, original_resolution, target_resolution_2k)
    print(f"Coordinates on 2K monitor: ({new_x_2k}, {new_y_2k})")

    # Преобразование координат для Low resolution монитора
    new_x_low, new_y_low = convert_coordinates(original_x, original_y, original_resolution, target_resolution_low)
    print(f"Coordinates on Low resolution monitor: ({new_x_low}, {new_y_low})")

if __name__ == "__main__":
    main()
