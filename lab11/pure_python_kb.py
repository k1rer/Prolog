from pyswip import Prolog

def create_knowledge_base():
    prolog = Prolog()

    prolog.assertz(':- encoding(utf8)')
    prolog.assertz(':- dynamic технология/1')
    prolog.assertz(':- dynamic сложность/2')
    prolog.assertz(':- dynamic проект/3')
    prolog.assertz(':- dynamic стек/1')
    prolog.assertz(':- dynamic легкий_язык/1')

    technologies = ['python', 'prolog', 'java', 'javascript']
    for tech in technologies:
        prolog.assertz(f'технология({tech})')

    difficulties = [('python', 3), ('prolog', 4), ('java', 4), ('javascript', 2)]
    for tech, level in difficulties:
        prolog.assertz(f'сложность({tech}, {level})')

    projects = [
        ('веб_сайт', 'python', 30),
        ('ии_система', 'prolog', 45),
        ('мобильное_приложение', 'java', 60),
        ('интерфейс', 'javascript', 15)
    ]
    for name, lang, days in projects:
        prolog.assertz(f'проект({name}, {lang}, {days})')

    tech_stacks = [
        ['python', 'javascript', 'sql'],
        ['prolog', 'python', 'java'],
        ['java', 'kotlin', 'firebase'],
        ['javascript', 'html', 'css']
    ]
    for stack in tech_stacks:
        stack_str = ', '.join(stack)
        prolog.assertz(f'стек([{stack_str}])')

    prolog.assertz("""легкий_язык(Язык) :-
        технология(Язык),
        сложность(Язык, Уровень),
        Уровень < 4""")

    prolog.assertz("""подходящий_проект(Язык, Проект) :-
        проект(Проект, Язык, Срок),
        Срок < 50""")

    prolog.assertz("""использует_язык(Стек, Язык) :-
        стек(Стек), member(Язык, Стек)""")

    prolog.assertz('содержит_python([python])')
    prolog.assertz('содержит_python([_|Хвост]) :- содержит_python(Хвост)')

    return prolog

if __name__ == '__main__':
    kb = create_knowledge_base()

    print('Легкие языки:')
    for sol in kb.query('легкий_язык(Язык)'):
        print(sol['Язык'])

    print('\nПроекты для Python со сроком < 50 дней:')
    for sol in kb.query('подходящий_проект(python, Проект)'):
        print(sol['Проект'])

    print('\nСтеки, содержащие Python:')
    for sol in kb.query('стек(Стек), содержит_python(Стек)'):
        print(sol['Стек'])