import tkinter as tk
from tkinter import messagebox

cart = []

wallet_balance = 1000000

def place_order():
    if not cart:
        messagebox.showwarning("Предупреждение", "Пожалуйста, добавьте товары в корзину.")
    else:
        order_total = get_cart_total()

        if order_total >= 5000:
            messagebox.showinfo("Подтверждение", f"Ваш заказ:\n{get_cart_items()}"
                                                  f"\nБесплатная 1л Coca-Cola\n\nОбщая сумма заказа: {order_total} тг.")
        else:
            messagebox.showinfo("Подтверждение", f"Ваш заказ:\n{get_cart_items()}"
                                                 f"\nОбщая сумма заказа: {order_total} тг.")
        clear_cart()

def add_to_cart():
    global wallet_balance

    selected_item = item_var.get()
    selected_size = size_var.get()

    if selected_item == '':
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите товар.")
    elif selected_size == '':
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите размер.")
    else:
        item_price = get_item_price(selected_item)

        if item_price > wallet_balance:
            messagebox.showwarning("Предупреждение", "Недостаточно средств на кошельке.")
        else:
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Предупреждение", "Пожалуйста, введите корректное количество товара.")
            else:
                total_price = item_price * quantity  # Вычислить общую стоимость
                cart.append((selected_item, selected_size, quantity, total_price))  # Добавление товара в корзину
                wallet_balance -= total_price  # Списание стоимости товара с баланса кошелька
                wallet_label.config(text=f"Баланс кошелька: {wallet_balance} тг.")  # Обновление метки с балансом
                update_cart()

def get_item_price(item):
    item_prices = {
        'Пицца_Пепперони': {'Маленькая': 5000, 'Средняя': 6000, 'Большой': 700},
        'Пицца_Гавайская': {'Маленькая': 5500, 'Средняя': 6500, 'Большой': 7500},
        'Пицца_Маргарита': {'Маленькая': 4500, 'Средняя': 5500, 'Большой': 6500},
        'Пицца_Вегетарианская': {'Маленькая': 6000, 'Средняя': 7000, 'Большой': 8000},
        'БУРГЕР PRIME': {'Маленькая': 4000, 'Средняя': 5000, 'Большой': 6000},
        'Донер_Куриный': {'Маленькая': 3500, 'Средняя': 4500, 'Большой': 5050},
        'Донер_Говяжий': {'Маленькая': 3500, 'Средняя': 4500, 'Большой': 5500},
        'Донер_Ассорти': {'Маленькая': 3500, 'Средняя': 4500, 'Большой': 5500},
        'Фри': {'Маленькая': 400, 'Средняя': 600, 'Большой': 1000},
        'Coca-Cola': {'0.5л': 250, '1л': 500, '1.5л': 650, '2л': 800},
        'Fanta': {'0.5л': 250, '1л': 500, '1.5л': 650, '2л': 800},
        'Sprite': {'0.5л': 250, '1л': 500, '1.5л': 650, '2л': 800}
    }
    size_prices = item_prices.get(item, {})
    return size_prices.get(size_var.get(), 0)

def get_cart_total():
    total = sum(item[3] for item in cart)
    return total

def get_cart_items():
    items = ""
    for item in cart:
        items += f"- {item[0]} ({item[1]}): {item[2]}шт, {item[3]} тг.\n"
    cart_text.insert(tk.END, items)
    return items

def clear_cart():
    cart.clear()
    update_cart()

window = tk.Tk()
window.title("Центр быстрого питания")

balans_label = tk.Label(window, text=f"Добро пожаловать в Центр быстрого питания!", font=("Arial", 11, "bold"), fg="blue")
balans_label.pack()

wallet_label = tk.Label(window,text=f"Баланс кошелька:{wallet_balance} тг.", font=("Arial", 10, "bold"), fg="green")
wallet_label.pack()

item_label = tk.Label(window, text="Выберите товар:")
item_label.pack()

item_var = tk.StringVar(window)

item_choices = ['Пицца_Пепперони', 'Пицца_Гавайская', 'Пицца_Маргарита', 'Пицца_Вегетарианская', 'БУРГЕР PRIME', 'Донер_Куриный','Донер_Говяжий','Донер_Ассорти',
                'Фри','Coca-Cola','Fanta', 'Sprite']
item_dropdown = tk.OptionMenu(window, item_var, *item_choices)
item_dropdown.pack()

size_label = tk.Label(window, text="Выберите размер или объем:")
size_label.pack()

size_var = tk.StringVar(window)

size_choices = ['Маленькая', 'Средняя', 'Большой','0.5л','1л','1.5л','2л']
size_dropdown = tk.OptionMenu(window, size_var, *size_choices)
size_dropdown.pack()

quantity_label = tk.Label(window, text="Введите количество:")
quantity_label.pack()

quantity_entry = tk.Entry(window)
quantity_entry.pack()

add_to_cart_button = tk.Button(window, text="Добавить в корзину", command=add_to_cart)
add_to_cart_button.pack()

order_button = tk.Button(window, text="Заказать", command=place_order)
order_button.pack()

item_price_label = tk.Label(window, text="Меню:")
item_price_label.pack()

item_price_text = tk.Text(window, width=45, height=10)
item_price_text.pack()

def update_item_prices():
    item_price_text.delete('1.0', tk.END)
    for item, size_prices in item_prices.items():
        price_text = f"{item}:\n"
        for size, price in size_prices.items():
            price_text += f"  - {size}: {price} тг.\n"
        item_price_text.insert(tk.END, price_text + '\n')

item_prices = {
        'Пицца_Пепперони': {'Маленькая': 5000, 'Средняя': 6000, 'Большой': 700},
        'Пицца_Гавайская': {'Маленькая': 5500, 'Средняя': 6500, 'Большой': 7500},
        'Пицца_Маргарита': {'Маленькая': 4500, 'Средняя': 5500, 'Большой': 6500},
        'Пицца_Вегетарианская': {'Маленькая': 6000, 'Средняя': 7000, 'Большой': 8000},
        'БУРГЕР PRIME': {'Маленькая': 4000, 'Средняя': 5000, 'Большой': 6000},
        'Донер_Куриный': {'Маленькая': 3500, 'Средняя': 4500, 'Большой': 5050},
        'Донер_Говяжий': {'Маленькая': 3500, 'Средняя': 4500, 'Большой': 5500},
        'Донер_Ассорти': {'Маленькая': 3500, 'Средняя': 4500, 'Большой': 5500},
        'Фри': {'Маленькая': 400, 'Средняя': 600, 'Большой': 1000},
        'Coca-Cola': {'0.5л': 250, '1л': 500, '1.5л': 650, '2л': 800},
        'Fanta': {'0.5л': 250, '1л': 500, '1.5л': 650, '2л': 800},
        'Sprite': {'0.5л': 250, '1л': 500, '1.5л': 650, '2л': 800}
}
update_item_prices()

cart_label = tk.Label(window, text="Ваш заказ:")
cart_label.pack()

cart_text = tk.Text(window, width=45, height=10)
cart_text.pack()

def update_cart():
    cart_text.delete('1.0', tk.END)
    get_cart_items()


window.mainloop()