from pyswip import Prolog


class LogicSystem:
    """Простая логическая система на Prolog"""

    def __init__(self):
        self.prolog = Prolog()
        self._setup_knowledge_base()

    def _setup_knowledge_base(self):
        """Настройка базы знаний"""
        # Динамические предикаты (необходимы для работы retractall)
        self.prolog.assertz(':- dynamic time/1')
        self.prolog.assertz(':- dynamic weather/1')
        self.prolog.assertz(':- dynamic location/2')
        self.prolog.assertz(':- dynamic temperature/2')

        # Факты о помещениях
        self.prolog.assertz('room(living_room)')
        self.prolog.assertz('room(kitchen)')
        self.prolog.assertz('room(hallway)')
        self.prolog.assertz('room(bedroom)')

        # Факты о пользователях
        self.prolog.assertz('user(alice)')
        self.prolog.assertz('user(bob)')
        self.prolog.assertz('user(charlie)')
        self.prolog.assertz('adult(alice)')
        self.prolog.assertz('adult(bob)')
        self.prolog.assertz('child(charlie)')

        # Факты об устройствах
        self.prolog.assertz('device(tv, living_room)')
        self.prolog.assertz('device(ac, living_room)')
        self.prolog.assertz('device(light, hallway)')
        self.prolog.assertz('device(umbrella, hallway)')
        self.prolog.assertz('device(night_light, bedroom)')

        # Правила системы
        self.prolog.assertz(
            """need_umbrella(P) :-
                weather(rain),
                location(P, hallway)"""
        )
        self.prolog.assertz(
            """turn_off_tv(K, R) :-
                child(K),
                time(night),
                location(K, R),
                device(tv, R)"""
        )
        self.prolog.assertz(
            """turn_on_light(P) :-
                time(morning),
                weather(rain),
                location(P, hallway)"""
        )
        self.prolog.assertz(
            """turn_on_ac(R) :-
                temperature(R, T),
                T > 28,
                device(ac, R)"""
        )
        self.prolog.assertz(
            """turn_on_night_light(K, R) :-
                child(K),
                time(night),
                location(K, R),
                device(night_light, R)"""
        )

    def query(self, query_string):
        """Выполняет запрос к базе знаний"""
        try:
            return list(self.prolog.query(query_string))
        except:
            return []

    def add_fact(self, fact):
        """Добавляет факт в базу знаний"""
        self.prolog.assertz(fact)

    def get_recommendations(self):
        """Возвращает рекомендации в стандартном формате"""
        recommendations = []
        # Проверяем условия для зонта
        if self.query('need_umbrella(alice)'):
            recommendations.append('turn_on umbrella hallway')

        # Проверяем условия для выключения TV
        tv_rooms = self.query('device(tv, Room)')
        for room in tv_rooms:
            room_name = room['Room']
            if self.query(f"turn_off_tv(charlie, '{room_name}')"):
                recommendations.append(f'turn_off tv {room_name}')

        # Проверяем условия для включения света
        if self.query('turn_on_light(alice)'):
            recommendations.append('turn_on light hallway')

        # Проверяем условия для кондиционера
        ac_rooms = self.query('device(ac, Room)')
        for room in ac_rooms:
            room_name = room['Room']
            if self.query(f"turn_on_ac('{room_name}')"):
                recommendations.append(f'turn_on ac {room_name}')

        # Проверяем условия для ночника
        night_light_rooms = self.query('device(night_light, Room)')
        for room in night_light_rooms:
            room_name = room['Room']
            if self.query(f"turn_on_night_light(charlie, '{room_name}')"):
                recommendations.append(f'turn_on night_light {room_name}')

        return recommendations

    def set_context(
        self,
        time=None,
        weather=None,
        location=None,
        temperature_data=None,
    ):
        """Устанавливает контекст для системы"""
        if time:
            self.prolog.retractall('time(_)')
            self.prolog.assertz(f'time({time})')
        if weather:
            self.prolog.retractall('weather(_)')
            self.prolog.assertz(f'weather({weather})')
        if location:
            user, room = location
            self.prolog.retractall(f'location({user}, _)')
            self.prolog.assertz(f'location({user}, {room})')
        if temperature_data:
            room, temp = temperature_data
            self.prolog.retractall(f'temperature({room}, _)')
            self.prolog.assertz(f'temperature({room}, {temp})')

    def print_state(self):
        """Печатает текущее состояние системы"""
        print('Логическая модель - Текущее состояние:')
        # Время и погода
        time_result = self.query('time(T)')
        if time_result:
            print(f" Время: {time_result[0]['T']}")
        weather_result = self.query('weather(W)')
        if weather_result:
            print(f" Погода: {weather_result[0]['W']}")
        # Локации пользователей
        locations = self.query('location(User, Room)')
        for loc in locations:
            print(f" {loc['User']} находится в {loc['Room']}")
        # Температуры
        temps = self.query('temperature(Room, Temp)')
        for temp in temps:
            print(f" Температура в {temp['Room']}: {temp['Temp']}°C")


def demo_predicate_logic():
    """Демонстрация логической модели"""
    system = LogicSystem()
    print('=== ДЕМО ЛОГИЧЕСКОЙ МОДЕЛИ ===')

    # Сценарий 1: Утро + дождь
    print('\n Сценарий 1: Утро + Дождь')
    system.set_context(
        time='morning', weather='rain', location=('alice', 'hallway')
    )
    system.print_state()
    print('Рекомендации:')
    for rec in system.get_recommendations():
        print(f' - {rec}')

    # Сценарий 2: Ночь + ребенок
    print('\n Сценарий 2: Ночь + Ребенок')
    system.set_context(
        time='night', weather='clear', location=('charlie', 'living_room')
    )
    system.print_state()
    print('Рекомендации:')
    for rec in system.get_recommendations():
        print(f' - {rec}')

    # Сценарий 3: Жаркий день
    print('\n Сценарий 3: Жаркий день')
    system.set_context(
        time='day', weather='sunny', location=('alice', 'living_room'), temperature_data=('living_room', 30),
    )
    system.print_state()
    print('Рекомендации:')
    for rec in system.get_recommendations():
        print(f' - {rec}')


if __name__ == '__main__':
    demo_predicate_logic()