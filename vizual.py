import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation

# Загружаем данные
data_rk4 = np.loadtxt("rk4_trajectory.csv", delimiter=',', skiprows=1)
data_dopri5 = np.loadtxt("dopri5_trajectory.csv", delimiter=',', skiprows=1)
data_euler = np.loadtxt("euler_trajectory.csv", delimiter=',', skiprows=1)

# Извлекаем данные
x_rk4, y_rk4, z_rk4, t_rk4 = data_rk4[:, 0], data_rk4[:, 1], data_rk4[:, 2], data_rk4[:, 3]
x_dopri5, y_dopri5, z_dopri5, t_dopri5 = data_dopri5[:, 0], data_dopri5[:, 1], data_dopri5[:, 2], data_dopri5[:, 3]
x_euler, y_euler, z_euler, t_euler = data_euler[:, 0], data_euler[:, 1], data_euler[:, 2], data_euler[:, 3]

# Вычисляем ошибки между методами
error_x_rk4_euler = np.abs(x_rk4 - x_euler)  # Ошибка по x между RK4 и Эйлером
error_y_rk4_euler = np.abs(y_rk4 - y_euler)  # Ошибка по y между RK4 и Эйлером
error_z_rk4_euler = np.abs(z_rk4 - z_euler)  # Ошибка по z между RK4 и Эйлером

error_x_dopri5_euler = np.abs(x_dopri5 - x_euler)  # Ошибка по x между Dopri5 и Эйлером
error_y_dopri5_euler = np.abs(y_dopri5 - y_euler)  # Ошибка по y между Dopri5 и Эйлером
error_z_dopri5_euler = np.abs(z_dopri5 - z_euler)  # Ошибка по z между Dopri5 и Эйлером

# Создаем фигуру
fig = plt.figure(figsize=(18, 12))
plt.subplots_adjust(bottom=0.2)

# Графики фазового пространства
ax1 = fig.add_subplot(2, 3, 1, projection='3d')
ax2 = fig.add_subplot(2, 3, 2, projection='3d')
ax3 = fig.add_subplot(2, 3, 3, projection='3d')

# Графики ошибок
ax4 = fig.add_subplot(2, 3, 4)
ax5 = fig.add_subplot(2, 3, 5)
ax6 = fig.add_subplot(2, 3, 6)

# Настройка фазовых графиков
for ax in (ax1, ax2, ax3):
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(np.min([x_rk4, x_dopri5, x_euler]) - 0.5, np.max([x_rk4, x_dopri5, x_euler]) + 0.5)
    ax.set_ylim(np.min([y_rk4, y_dopri5, y_euler]) - 0.5, np.max([y_rk4, y_dopri5, y_euler]) + 0.5)
    ax.set_zlim(np.min([z_rk4, z_dopri5, z_euler]) - 0.5, np.max([z_rk4, z_dopri5, z_euler]) + 0.5)

ax1.set_title("RK4")
ax2.set_title("Dopri5")
ax3.set_title("Euler")

# Настройка графиков ошибок
ax4.set_xlabel("Time")
ax4.set_ylabel("Error in x")
ax4.set_title("Error in x (RK4 vs Euler)")
ax4.set_xlim(0, t_rk4[-1])
ax4.set_ylim(0, np.max(error_x_rk4_euler) + 0.1)

ax5.set_xlabel("Time")
ax5.set_ylabel("Error in y")
ax5.set_title("Error in y (RK4 vs Euler)")
ax5.set_xlim(0, t_rk4[-1])
ax5.set_ylim(0, np.max(error_y_rk4_euler) + 0.1)

ax6.set_xlabel("Time")
ax6.set_ylabel("Error in z")
ax6.set_title("Error in z (RK4 vs Euler)")
ax6.set_xlim(0, t_rk4[-1])
ax6.set_ylim(0, np.max(error_z_rk4_euler) + 0.1)

# Графические объекты
line_rk4, = ax1.plot([], [], [], 'b-', lw=0.5)
line_dopri5, = ax2.plot([], [], [], 'r-', lw=0.5)
line_euler, = ax3.plot([], [], [], 'g-', lw=0.5)

line_error_x, = ax4.plot([], [], 'b-', label='Error in x')
line_error_y, = ax5.plot([], [], 'r-', label='Error in y')
line_error_z, = ax6.plot([], [], 'g-', label='Error in z')

ax4.legend()
ax5.legend()
ax6.legend()

# Добавляем виджеты
ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03])
ax_play = plt.axes([0.15, 0.01, 0.1, 0.03])
ax_stop = plt.axes([0.3, 0.01, 0.1, 0.03])

slider = Slider(ax_slider, 'Time', 0, len(t_rk4) - 1, valinit=0, valstep=1)
button_play = Button(ax_play, 'Play')
button_stop = Button(ax_stop, 'Stop')

anim = None
current_frame = 0

# Функция обновления графиков
def update(frame):
    line_rk4.set_data(x_rk4[:frame], y_rk4[:frame])
    line_rk4.set_3d_properties(z_rk4[:frame])
    line_dopri5.set_data(x_dopri5[:frame], y_dopri5[:frame])
    line_dopri5.set_3d_properties(z_dopri5[:frame])
    line_euler.set_data(x_euler[:frame], y_euler[:frame])
    line_euler.set_3d_properties(z_euler[:frame])

    line_error_x.set_data(t_rk4[:frame], error_x_rk4_euler[:frame])
    line_error_y.set_data(t_rk4[:frame], error_y_rk4_euler[:frame])
    line_error_z.set_data(t_rk4[:frame], error_z_rk4_euler[:frame])

    fig.canvas.draw_idle()

# Функция для слайдера
def update_slider(val):
    global current_frame
    current_frame = int(val)
    update(current_frame)

# Функция анимации
def animate(frame):
    global current_frame
    current_frame = frame
    update(frame)
    slider.set_val(frame)
    return line_rk4, line_dopri5, line_euler, line_error_x, line_error_y, line_error_z

# Функция запуска анимации
def play(event):
    global anim
    if anim is None or anim.event_source is None:
        anim = animation.FuncAnimation(
            fig, animate, frames=range(current_frame, len(t_rk4)), interval=5, blit=False, repeat=True
        )
    fig.canvas.draw_idle()

# Функция остановки анимации
def stop(event):
    global anim
    if anim is not None:
        anim.event_source.stop()
        anim = None
    update(current_frame)

slider.on_changed(update_slider)
button_play.on_clicked(play)
button_stop.on_clicked(stop)

update(0)

plt.show()