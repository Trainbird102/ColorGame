import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from collections import deque


class ColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Раскраска по номерам")
        self.root.geometry("900x700")

        # Цвета радуги
        self.colors = {
            1: '#FF0000',  # красный
            2: '#FF7F00',  # оранжевый
            3: '#FFFF00',  # желтый
            4: '#00FF00',  # зеленый
            5: '#0000FF',  # синий
            6: '#4B0082',  # индиго
            7: '#8B00FF'  # фиолетовый
        }

        # Создаем изображения для раскраски
        self.create_template_images()

        self.setup_ui()

    def create_template_images(self):
        """Создает шаблонные изображения с номерами"""
        self.images = {}

        # Машина
        car_img = Image.new('RGB', (400, 300), 'white')
        draw = ImageDraw.Draw(car_img)

        # Рисуем простую машину с разными областями и ЗАЛИВАЕМ ИХ СЕРЫМ для тестирования
        draw.rectangle([100, 180, 350, 220], outline='black', fill='lightgray')  # кузов
        draw.rectangle([150, 150, 250, 180], outline='black', fill='lightgray')  # кабина
        draw.ellipse([120, 200, 180, 260], outline='black', fill='lightgray')  # колесо 1
        draw.ellipse([270, 200, 330, 260], outline='black', fill='lightgray')  # колесо 2

        # Добавляем номера
        draw.text((200, 160), "1", fill='black', font=None)  # кабина
        draw.text((180, 190), "2", fill='black', font=None)  # кузов перед
        draw.text((220, 190), "3", fill='black', font=None)  # кубов центр
        draw.text((140, 220), "4", fill='black', font=None)  # колесо 1
        draw.text((280, 220), "5", fill='black', font=None)  # колесо 2

        self.images['car'] = car_img

        # Ракета
        rocket_img = Image.new('RGB', (400, 300), 'white')
        draw = ImageDraw.Draw(rocket_img)

        # Рисуем ракету с заливкой серым
        draw.polygon([200, 80, 130, 220, 270, 220], outline='black', fill='lightgray')  # корпус
        draw.rectangle([160, 220, 240, 260], outline='black', fill='lightgray')  # основание
        draw.polygon([160, 260, 130, 280, 160, 300], outline='black', fill='lightgray')  # стабилизатор 1
        draw.polygon([240, 260, 270, 280, 240, 300], outline='black', fill='lightgray')  # стабилизатор 2

        # Номера
        draw.text((190, 150), "1", fill='black', font=None)  # нос
        draw.text((190, 190), "2", fill='black', font=None)  # середина
        draw.text((190, 230), "3", fill='black', font=None)  # основание
        draw.text((140, 270), "4", fill='black', font=None)  # стаб. 1
        draw.text((230, 270), "5", fill='black', font=None)  # стаб. 2

        self.images['rocket'] = rocket_img

        # Дом
        house_img = Image.new('RGB', (400, 300), 'white')
        draw = ImageDraw.Draw(house_img)

        # Рисуем дом с заливкой серым
        draw.rectangle([150, 150, 350, 270], outline='black', fill='lightgray')  # основная часть
        draw.polygon([130, 150, 250, 90, 370, 150], outline='black', fill='lightgray')  # крыша
        draw.rectangle([200, 200, 300, 270], outline='black', fill='lightgray')  # дверь
        draw.rectangle([170, 170, 190, 190], outline='black', fill='lightgray')  # окно 1
        draw.rectangle([310, 170, 330, 190], outline='black', fill='lightgray')  # окно 2

        # Номера
        draw.text((250, 120), "1", fill='black', font=None)  # крыша
        draw.text((240, 200), "2", fill='black', font=None)  # стена
        draw.text((250, 230), "3", fill='black', font=None)  # дверь
        draw.text((175, 175), "4", fill='black', font=None)  # окно 1
        draw.text((315, 175), "5", fill='black', font=None)  # окно 2

        self.images['house'] = house_img

        # Создаем копии для раскрашивания
        self.current_image = car_img.copy()
        self.current_image_type = 'car'
        self.original_images = {key: img.copy() for key, img in self.images.items()}

    def setup_ui(self):
        """Создает интерфейс пользователя"""
        # Фрейм для выбора изображения
        selection_frame = tk.Frame(self.root)
        selection_frame.pack(pady=10)

        tk.Label(selection_frame, text="Выберите картинку:", font=('Arial', 12)).pack(side=tk.LEFT)

        self.image_var = tk.StringVar(value="car")
        tk.Radiobutton(selection_frame, text="Машина", variable=self.image_var,
                       value="car", command=self.change_image).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(selection_frame, text="Ракета", variable=self.image_var,
                       value="rocket", command=self.change_image).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(selection_frame, text="Дом", variable=self.image_var,
                       value="house", command=self.change_image).pack(side=tk.LEFT, padx=5)

        # Основной фрейм с изображением и палитрой
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Холст для изображения
        self.canvas = tk.Canvas(main_frame, width=500, height=400, bg='white',
                                cursor="crosshair", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(side=tk.TOP, pady=10)

        # Привязываем обработчики событий
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Подсказка для пользователя
        self.hint_label = tk.Label(main_frame,
                                   text="Выберите цвет и кликните на область для закрашивания",
                                   font=('Arial', 10), fg='gray')
        self.hint_label.pack(side=tk.TOP)

        # Статусная строка
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_label = tk.Label(main_frame, textvariable=self.status_var,
                                font=('Arial', 9), fg='blue')
        status_label.pack(side=tk.TOP, pady=5)

        # Отображаем текущее изображение
        self.display_image()

        # Палитра цветов
        palette_frame = tk.Frame(main_frame)
        palette_frame.pack(side=tk.TOP, pady=10)

        tk.Label(palette_frame, text="Палитра цветов:", font=('Arial', 12)).pack()

        colors_frame = tk.Frame(palette_frame)
        colors_frame.pack(pady=5)

        self.selected_color = tk.IntVar(value=1)

        # Создаем кнопки цветов с отображением hex-кода
        for i, (num, color) in enumerate(self.colors.items()):
            color_frame = tk.Frame(colors_frame)
            color_frame.pack(side=tk.LEFT, padx=5)

            # Показываем цвет с рамкой
            color_canvas = tk.Canvas(color_frame, width=40, height=40, bg=color,
                                     relief="solid", borderwidth=2)
            color_canvas.pack()

            # Подписываем цвет hex-кодом
            tk.Label(color_frame, text=color, font=('Arial', 8)).pack()

            # Радиокнопка для выбора цвета
            tk.Radiobutton(color_frame, text=f"Цвет {num}", variable=self.selected_color,
                           value=num, font=('Arial', 9)).pack()

        # Кнопки управления
        control_frame = tk.Frame(main_frame)
        control_frame.pack(side=tk.TOP, pady=10)

        tk.Button(control_frame, text="Очистить", command=self.clear_image,
                  font=('Arial', 10), bg='#f0f0f0', width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Сохранить", command=self.save_image,
                  font=('Arial', 10), bg='#f0f0f0', width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Показать подсказку", command=self.show_color_hint,
                  font=('Arial', 10), bg='#f0f0f0', width=15).pack(side=tk.LEFT, padx=5)

    def display_image(self):
        """Отображает текущее изображение на холсте"""
        try:
            # Конвертируем PIL Image в PhotoImage
            self.tk_image = ImageTk.PhotoImage(self.current_image)

            # Очищаем холст и отображаем изображение
            self.canvas.delete("all")
            self.canvas.create_image(250, 200, image=self.tk_image, anchor=tk.CENTER)
            self.status_var.set("Изображение загружено")

        except Exception as e:
            print(f"Ошибка при отображении изображения: {e}")
            self.status_var.set(f"Ошибка: {e}")

    def change_image(self):
        """Меняет текущее изображение"""
        image_type = self.image_var.get()
        self.current_image = self.images[image_type].copy()
        self.current_image_type = image_type
        self.display_image()
        self.status_var.set(f"Загружено: {image_type}")

    def on_canvas_click(self, event):
        """Обрабатывает клик по холсту - закрашивает область выбранным цветом"""
        # Получаем координаты клика
        x, y = event.x, event.y

        # Проверяем, что клик внутри области изображения (примерные границы)
        if 50 <= x <= 450 and 50 <= y <= 350:
            # Преобразуем координаты холста в координаты изображения
            img_x = x - 50
            img_y = y - 50

            # Ограничиваем координаты размерами изображения
            img_x = max(0, min(img_x, 399))
            img_y = max(0, min(img_y, 299))

            self.status_var.set(f"Клик по координатам: ({img_x}, {img_y})")

            # Заливаем область выбранным цветом
            self.fill_area(img_x, img_y)
            # Обновляем отображение
            self.display_image()
        else:
            self.status_var.set("Клик вне изображения")

    def fill_area(self, x, y):
        """Заливка всей ограниченной области с использованием алгоритма flood fill"""
        try:
            # Получаем выбранный цвет
            selected_color_num = self.selected_color.get()
            new_color_hex = self.colors[selected_color_num]
            new_color_rgb = tuple(int(new_color_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))

            # Получаем исходный цвет в точке клика
            target_color = self.current_image.getpixel((x, y))

            # Если кликнули по черному контуру или уже закрашенной области, игнорируем
            if target_color == (0, 0, 0) or target_color == new_color_rgb:
                return

            # Используем BFS для заливки области
            pixels = self.current_image.load()
            width, height = self.current_image.size

            queue = deque([(x, y)])
            visited = set()

            while queue:
                cx, cy = queue.popleft()

                if (cx, cy) in visited:
                    continue

                visited.add((cx, cy))

                # Проверяем границы и совпадение цвета
                if (0 <= cx < width and 0 <= cy < height and
                        pixels[cx, cy] == target_color):

                    # Закрашиваем пиксель
                    pixels[cx, cy] = new_color_rgb

                    # Добавляем соседние пиксели
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        queue.append((cx + dx, cy + dy))

            self.status_var.set(f"Область закрашена. Закрашено пикселей: {len(visited)}")

        except Exception as e:
            print(f"Ошибка при заливке: {e}")
            self.status_var.set(f"Ошибка заливки: {e}")

    def clear_image(self):
        """Очищает изображение (возвращает к исходному состоянию)"""
        # Восстанавливаем исходное изображение
        self.current_image = self.original_images[self.current_image_type].copy()
        # Также обновляем основное изображение в словаре
        self.images[self.current_image_type] = self.current_image.copy()
        self.display_image()
        self.status_var.set("Изображение очищено")

    def save_image(self):
        """Сохраняет раскрашенное изображение"""
        try:
            filename = f"colored_{self.current_image_type}.png"
            self.current_image.save(filename)
            messagebox.showinfo("Успех", f"Изображение сохранено как {filename}")
            self.status_var.set(f"Сохранено: {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")
            self.status_var.set(f"Ошибка сохранения: {e}")

    def show_color_hint(self):
        """Показывает подсказку по цветам"""
        color_info = "\n".join([f"Цвет {num}: {color}" for num, color in self.colors.items()])
        messagebox.showinfo("Палитра цветов",
                            f"Доступные цвета:\n\n{color_info}\n\n"
                            f"Выберите цвет и кликайте на области изображения для закрашивания")


if __name__ == "__main__":
    root = tk.Tk()
    app = ColoringApp(root)
    root.mainloop()