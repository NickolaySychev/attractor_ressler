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

# Создаем фигуру
fig = plt.figure(figsize=(18, 12))
plt.subplots_adjust(bottom=0.2)

# Графики фазового пространства
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
ax3 = fig.add_subplot(2, 2, 3, projection='3d')

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

# Графические объекты
line_rk4, = ax1.plot([], [], [], 'b-', lw=0.5)
line_dopri5, = ax2.plot([], [], [], 'r-', lw=0.5)
line_euler, = ax3.plot([], [], [], 'g-', lw=0.5)

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
    line_rk4.set_data(x_rk4[:frame], y_rk4[:frame])
    line_rk4.set_3d_properties(z_rk4[:frame])
    line_dopri5.set_data(x_dopri5[:frame], y_dopri5[:frame])
    line_dopri5.set_3d_properties(z_dopri5[:frame])
    line_euler.set_data(x_euler[:frame], y_euler[:frame])
    line_euler.set_3d_properties(z_euler[:frame])
    slider.set_val(frame)
    return line_rk4, line_dopri5, line_euler

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