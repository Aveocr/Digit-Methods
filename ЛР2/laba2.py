from sympy import *
import pandas as pd
import matplotlib.pyplot as plt
te
x, y = symbols('x y')

# Создание датафрейма
def create_table(solve_x):
    x_range = create_range(solve_x)
    dz_dx = [abs(round(dz_dx_value(i), 3)) for i in x_range]  # вычисление модуля dz/dx
    RE = [round(delta_abs_z(i), 3) * 100 for i in x_range]  # Вычисление погршености в процентах
    return pd.DataFrame({'x': x_range, 'abs(dz/dx)': dz_dx, 'delta_z, %': RE})


# создание промежутка
def create_range(x, step=1, k=5):
    midd = int(round(x, 1) * 10)
    # create range
    if midd < 0:
        x_range = [float(i) / 10 for i in range(midd - k * step, midd, step)]
        x_range += [x]
        x_range += [float(i) / 10 for i in range(midd, midd + 5 + k * step, step)]
    else:
        x_range = [float(i) / 10 for i in range(midd - k * step, midd, step)]
        x_range += [x]
        x_range += [float(i) / 10 for i in range(midd, midd + k * step, step)]
    return x_range


if __name__ == '__main__':
    print("Добро пожаловать в программу по решение лабы 2 и созданию отчета в LaTeX! ")
    print("Создатель Денис Мустафин")

    print("Введите вашу формулы в python формате: ")
    print("Степень: через **, то есть 2 в 5 степени 2**5")
    print("сложение, вычитание, умножение, деление через стандарные Python операторы: +, -, *, /")
    print("sin(5x): sin(5 * x)")
    print("tan(), cos(), cot(), log(фунция, N - степень, если ничего, то это натуральный логарифм)")
    print("atan(), acos(), asin(), acot(), exp()\n\n\n")
    print("Введите вашу формулу сюда: -> ")

    x, y = symbols('x y')
    z = eval(input().replace("import", "").replace("sys", "").replace("os", ""))
    # z = (x**3-4*x)*sin(y**3+1)
    print(z, end="\n\n\n")
    print("Введите значения x и y c погрешностью в таком формате: x погрешность y погрешность"
          "\nНапример: -1.2 0.05\n0.15 0.01")
    x_num = tuple(float(x) for x in input().split(" "))
    y_num = tuple(float(x) for x in input().split(" "))

    # x_num = (-1.2, 0.05)
    # y_num = (0.15, 0.01)
    print(f"Вы ввели: x={x_num[0]}±{x_num[1]}, y={y_num[0]}±{y_num[1]}")

    # Вычисляем частные производные
    dz_dx = z.diff(x)
    dz_dy = z.diff(y)

    # создаем функцию, где мы вычисляем производных функции в точках x_value и y
    dz_dx_value = lambda x_value: round(dz_dx.subs([(x, x_value), (y, y_num[0])]), 4)
    dz_dy_value = lambda x_value: round(dz_dy.subs([(x, x_value), (y, y_num[0])]), 4)

    # Формула Δz = |dz/dx|Δx + |dz/dy|Δy
    delta_z = lambda x_value: round(abs(dz_dx_value(x_value)) * x_num[1] + abs(dz_dy_value(x_value)) * y_num[1], 4)

    # Подставляем в исходную функцию x_value
    z_value = lambda x_value: round(z.subs([(x, x_value), (y, y_num[0])]), 4)

    # выводим результаты подсчета
    print("dz/dx=", dz_dx, f' | ({x_num[0]}, {y_num[0]}) | =\t', dz_dx_value(x_num[0]))
    print("\n\ndz/dy=", dz_dy, f' | ({x_num[0]}, {y_num[0]}) | =\t', dz_dy_value(x_num[0]))
    print(f"z({x_num[0]}, {y_num[0]})={z_value(x_num[0])}")

    # высчитываю абсолютную погрешность
    delta_abs_z = lambda x_value: round(delta_z(x_value) / abs(z_value(x_value)), 4)
    print(f"\n\nΔZ=|{dz_dx_value(x_num[0])}|*{x_num[1]} + |{dz_dy_value(x_num[0])}|*{y_num[1]} =\t{delta_z(x_num[0])}")
    print(f'δ_z=ΔZ/|Z|={delta_z(x_num[0])}/|{z_value(x_num[0])}| =\t{delta_abs_z(x_num[0])},\t',
          round(delta_abs_z(x_num[0]) * 100, 1), "%")

    # решаем уравнение
    ans = solve(dz_dx, x)
    print("Теперь надо решить уравнение dz/dx = 0")
    print("Мы имеем следующее корни: ", ans)

    # Вывод всех вычислений и генерация графика
    for i, elem in enumerate(ans):
        fig, ax = plt.subplots(ncols=2)
        plt.figure()
        df = create_table(elem)
        print("\n\nКорень: ", elem)
        print(df.transpose().style.to_latex())
        # сохранение транспонированного графика в эксель
        df.transpose().to_csv("tabel"+str(i)+".csv")

        # рисуем графики
        ax[0].plot(df['x'], df['abs(dz/dx)'])
        ax[0].set_xlabel('x', fontsize=15, loc="right", )
        ax[0].set_ylabel(r'|$\mathdefault{\frac{\partial z}{\partial x}}$|', fontsize=15, loc="top")
        ax[0].set_title("а)")

        ax[1].plot(df['x'], df['delta_z, %'])
        ax[1].set_xlabel('x', fontsize=15, loc="right")
        ax[1].set_ylabel(r'$\delta_z$, %', fontsize=15, loc="top")
        ax[1].set_title("б)")

        # задаем отступ между полотнами
        # fig.subplots_adjust(wspace=0.3)
        fig.tight_layout(pad=5.0)
        # сохраняем в полотно и указываем номер
        fig.savefig("Plot" + str(i) + ".png")
    # чтобы программа не закрывалась сразу
    input()
