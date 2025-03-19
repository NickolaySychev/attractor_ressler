import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Для 3D графиков
from scipy.interpolate import interp1d  # Для интерполяции

# Загрузка данных из CSV файлов для обоих методов
data_rk4 = np.loadtxt('rk4_trajectory.csv', delimiter=',', skiprows=1)
data_dopri5 = np.loadtxt('dopri5_trajectory.csv', delimiter=',', skiprows=1)
data_euler = np.loadtxt('euler_trajectory.csv', delimiter=',', skiprows=1)

# Разделение данных на x, y, z и t для обоих методов
x_rk4 = data_rk4[:, 0]
y_rk4 = data_rk4[:, 1]
z_rk4 = data_rk4[:, 2]
t_rk4 = data_rk4[:, 3]

x_dopri5 = data_dopri5[:, 0]
y_dopri5 = data_dopri5[:, 1]
z_dopri5 = data_dopri5[:, 2]
t_dopri5 = data_dopri5[:, 3]

x_euler = data_euler[:, 0]
y_euler = data_euler[:, 1]
z_euler = data_euler[:, 2]
t_euler = data_euler[:, 3]

# Проверка длины данных
print(f"Размеры данных RK4: {len(x_rk4)}, {len(y_rk4)}, {len(z_rk4)}")
print(f"Размеры данных Dopri5: {len(x_dopri5)}, {len(y_dopri5)}, {len(z_dopri5)}")
print(f"Размеры данных Eulere: {len(x_euler)}, {len(y_euler)}, {len(z_euler)}")

# Построение 2D графиков для x-y
plt.figure(figsize=(15, 5))

# График Euler
plt.subplot(1, 3, 1)
plt.plot(x_euler, y_euler, label='Euler', color='g')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Euler: x-y')
plt.legend()


# График RK4
plt.subplot(1, 3, 2)
plt.plot(x_rk4, y_rk4, label='RK4', color='b')
plt.xlabel('x')
plt.ylabel('y')
plt.title('RK4: x-y')
plt.legend()

# График Dopri5
plt.subplot(1, 3, 3)
plt.plot(x_dopri5, y_dopri5, label='Dopri5', color='r')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Dopri5: x-y')
plt.legend()

# Сохранение 2D графиков
plt.tight_layout()
plt.savefig('individual_2d_plots.png', dpi=600)
plt.show()

# Построение наложенных 2D графиков для x-y
plt.figure(figsize=(10, 5))
plt.plot(x_rk4, y_rk4, label='RK4', color='b')
plt.plot(x_dopri5, y_dopri5, label='Dopri5', color='r')
plt.plot(x_euler, y_euler, label='Euler', color='g')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Наложение траекторий x-y')
plt.legend()

# Сохранение наложенного 2D графика
plt.tight_layout()
plt.savefig('overlay_2d_plots.png', dpi=600)
plt.show()


# Построение 3D графиков для траектории
fig = plt.figure(figsize=(15, 5))

# График Euler
ax3 = fig.add_subplot(131, projection='3d')
ax3.plot(x_euler, y_euler, z_euler, label='Euler', color='g')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
ax3.set_title('Euler: Аттрактор Рёсслера')

# График RK4
ax = fig.add_subplot(132, projection='3d')
ax.plot(x_rk4, y_rk4, z_rk4, label='RK4', color='b')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('RK4: Аттрактор Рёсслера')

# График Dopri5
ax2 = fig.add_subplot(133, projection='3d')
ax2.plot(x_dopri5, y_dopri5, z_dopri5, label='Dopri5', color='r')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Dopri5: Аттрактор Рёсслера')

# Сохранение общего графика
plt.tight_layout()
plt.savefig('rossler_comparison.png', dpi=600)
plt.show()

# Оценка ошибки между двумя траекториями
def compute_error(x1, y1, z1, x2, y2, z2):
    # Можно использовать среднюю квадратичную ошибку
    error = np.sqrt(np.mean((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2))
    return error

# Вычисление ошибки между методами
error = compute_error(x_rk4, y_rk4, z_rk4, x_dopri5, y_dopri5, z_dopri5)
print(f"Средняя ошибка между методами RK4 и Dopri5: {error}")

# Визуализация ошибки между траекториями по времени
plt.figure(figsize=(10, 5))
plt.plot(t_rk4, np.sqrt((x_rk4 - x_dopri5) ** 2 + (y_rk4 - y_dopri5) ** 2 + (z_rk4 - z_dopri5) ** 2), label='Ошибка', color='purple')
plt.xlabel('Время')
plt.ylabel('Ошибка')
plt.title('Ошибка между методами RK4 и Dopri5 по времени')
plt.legend()
plt.tight_layout()
plt.show()
