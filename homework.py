from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = ('Тип тренировки: {training_type}; '
                    + 'Длительность: {duration:.3f} ч.; '
                    + 'Дистанция: {distance:.3f} км; '
                    + 'Ср. скорость: {speed:.3f} км/ч; '
                    + 'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    SECOND: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(training_type=type(self).__name__,
                              duration=self.duration,
                              distance=self.get_distance(),
                              speed=self.get_mean_speed(),
                              calories=self.get_spent_calories())

        return message


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self):
        calories = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                    - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                    * (self.SECOND * self.duration))

        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        calories = ((self.COEFF_CALORIE_1 * self.weight
                    + (self.get_mean_speed()**2 // self.height)
                    * self.COEFF_CALORIE_2 * self.weight)
                    * (self.SECOND * self.duration))

        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_COLORIE_1: float = 1.1
    COEFF_COLORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self):
        calories = ((self.get_mean_speed() + self.COEFF_COLORIE_1)
                    * self.COEFF_COLORIE_2 * self.weight)

        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in types:
        return types[workout_type](*data)
    else:
        raise KeyError(f'{workout_type} not found in dict')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
