from pyswip import Prolog

prolog = Prolog()
prolog.consult('test_swi.pl') 

print("--- Все технологии ---")
for r in prolog.query('технология(Х)'):
    print(f"Технология: {r['Х']}")

print("\n--- Легкие языки ---")
for r in prolog.query('легкий_язык(Х)'):
    print(f"- {r['Х']}")


prolog.assertz('технология(go)')
prolog.assertz('сложность(go, 5)')
prolog.asserta('проект(микросервис, go, 90)')

prolog.retract('технология(java)')
prolog.retractall('сложность(java, _)')


prolog.assertz('''очень_легкий_язык(Язык) :-
    технология(Язык),
    сложность(Язык, Уровень),
    Уровень < 3''')

prolog.assertz('''быстрый_проект(Проект) :-
    проект(Проект, Язык, Срок),
    сложность(Язык, Уровень),
    Срок < 40,
    Уровень < 4''')

print("\n--- Очень легкие языки ---")
for r in prolog.query('очень_легкий_язык(Язык)'):
    print(r['Язык'])

print("\n--- Быстрые проекты ---")
for r in prolog.query('быстрый_проект(Проект)'):
    print(r['Проект'])