from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        """Вывод сообщения о тренировке."""
        return self.MESSAGE.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self. weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration
                * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    LEN_STEP = 0.65
    CM_TO_METERS = 100
    weight_coef = 0.029
    weight_coef_2 = 0.035
    SEC_IN_HOUR = 3600
    KMH_IN_MS = round(Training.M_IN_KM / SEC_IN_HOUR, 3)
    SQUARE = 2

    def __init__(self, action: int, duration: float, weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return ((self.weight_coef_2 * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MS) ** self.SQUARE)
                / (self.height / self.CM_TO_METERS)
                * self.weight_coef * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CONST_WT = 1.1
    CONST_WT2 = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CONST_WT) * self.CONST_WT2
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TRAINING_TYPES = {
        'SWM': (Swimming, 5),
        'RUN': (Running, 3),
        'WLK': (SportsWalking, 4),
    }
    if workout_type not in TRAINING_TYPES:
        raise ValueError(
            f'Неизвестная треннировка {workout_type}.'
            'Доступные треннировки: SWM, RUN, WLK.'
        )
    if len(data) != TRAINING_TYPES[workout_type][1]:
        raise ValueError(
            f'Для тренировки {workout_type} неверно переданы данные.'
        )
    return TRAINING_TYPES[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))