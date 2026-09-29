from pyswip import Prolog
try:
    prolog = Prolog()
    prolog.assertz('тест(1)')
    results = list(prolog.query('тест(X)'))
    print('Установка прошла успешно:', results)
except Exception as e:
    print('Ошибка установки:', e)