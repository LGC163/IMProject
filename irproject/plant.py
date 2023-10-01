from aip import AipImageClassify
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.filedialog
import webbrowser
import os

""" 你的 APPID AK SK """
APP_ID = '33535559'
API_KEY = '2nnyZrGTf8sIwDlNQKi9mAy4'
SECRET_KEY = 'IAlMMcHYGZ4I4W1g1xP8DhpUkXX5yglC'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

# 创建GUI窗口
window = tk.Tk()
window.title("AI图像识别")
window.geometry("750x600")
window.configure(bg="#00BFFF")  # 修改窗口背景色

# 添加标题标签
title_label = tk.Label(window, text="欢迎进入植物识别系统", font=("宋体", 32, "bold"), bg="#00BFFF", fg="#FFFFFF")
title_label.grid(row=0, column=0, padx=20, pady=10, columnspan=3)

# 创建标签和按钮
upload_icon = Image.open('../image/upload.png').resize((25, 25))
upload_image = ImageTk.PhotoImage(upload_icon)
upload_label = tk.Label(window, text="请选择要识别的图片:", font=("Arial", 18, "bold"), bg="#00BFFF", fg="#FFFFFF", image=upload_image, compound="left")
upload_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
path_button_icon = Image.open('../image/folder.png').resize((25, 25))
path_button_image = ImageTk.PhotoImage(path_button_icon)

path_button = tk.Button(window, text="选择图片", font=("Arial", 14), bg="#FFFFFF", fg="#000000", bd=0, padx=10, pady=5, activeforeground="#000000", activebackground="#FFDAB9", cursor="hand2", image=path_button_image, compound="left")
path_button.grid(row=1, column=1, padx=5, pady=10, sticky="w")

# 创建图片预览标签
img_preview_label = tk.Label(window, text="图片预览:", font=("Arial", 18, "bold"), bg="#00BFFF", fg="#FFFFFF")
img_preview_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

# 创建图片预览框架
img_preview_frame = tk.Frame(window, width=300, height=300, bg="white")
img_preview_frame.grid(row=3, column=0, padx=20, pady=10)

# 创建文本标签和清除按钮，并将其放置在窗口上
result_label = tk.Label(window, text="识别结果：", font=("Arial", 18, "bold"), bg="#00BFFF", fg="#FFFFFF")
result_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")

result_treeview = ttk.Treeview(window, columns=('序号', '类别', '置信度'), show='headings')
result_treeview.column('序号', width=50, anchor="center")
result_treeview.column('类别', width=150, anchor="center")
result_treeview.column('置信度', width=80, anchor="center")
result_treeview.heading('序号', text='序号')
result_treeview.heading('类别', text='类别')
result_treeview.heading('置信度', text='置信度')
result_treeview.grid(row=3, column=1, padx=20, pady=10)

clear_icon = Image.open('../image/clear.png').resize((25, 25))
clear_image = ImageTk.PhotoImage(clear_icon)
clear_button = tk.Button(window, text="清除", font=("Arial", 14), bg="#FFFFFF", fg="#000000", bd=0, padx=10, pady=5, activeforeground="#000000", activebackground="#FFDAB9", cursor="hand2", image=clear_image, compound="left")
clear_button.grid(row=4, column=1, padx=20, pady=10)

# 定义函数进行图像识别并显示结果
def recognize_and_preview():
    # 弹出文件对话框，选择要识别的图片
    img_path = tkinter.filedialog.askopenfilename()
    # 读取图片文件
    with open(img_path, 'rb') as fp:
        image = fp.read()

    # 清空之前的预览和识别结果
    clear_preview_and_result()

    # 显示图片预览
    img = Image.open(img_path)
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    img_preview_frame.configure(bg="white")
    img_preview = tk.Label(img_preview_frame, image=img)
    img_preview.image = img
    img_preview.pack()

    # 调用Baidu AI图像识别API进行识别
    result = client.plantDetect(image)
    print(result)

    # 显示识别结果
    i = 1  # 初始化 i
    for item in result['result']:
        index = i
        result_treeview.insert('', 'end', values=(i, item['name'], f"{round(float(item['score']) * 100, 2)}%"))
        result_treeview.bind(f'<Double-Button-1>',
                             lambda event, index=index, name=item['name']: open_browser_for_search(name))
        i += 1

    # 设置识别结果表格样式
    style = ttk.Style()
    style.configure('Treeview.Heading', font=('Arial', 16, 'bold'))
    style.configure('Treeview', font=('Arial', 14))

    # 定义单元格样式
    style.map('Treeview', foreground=[('selected', 'black')], background=[('selected', '#DDD')])

# 定义清除函数，用于清除预览和识别结果
def clear_preview_and_result():
    # 清空图片预览
    for widget in img_preview_frame.winfo_children():
        widget.destroy()
        # 清空识别结果
        result_treeview.delete(*result_treeview.get_children())

# 添加按钮和文本框
path_button.configure(command=recognize_and_preview)
clear_button.configure(command=clear_preview_and_result)

def back():
    window.destroy()
    os.system("python main.py")

# 添加返回按钮
back_icon = Image.open('../image/back.png').resize((25, 25))
back_image = ImageTk.PhotoImage(back_icon)
back_button = tk.Button(window, text="返回", command=back, font=("Arial", 14), bg="#FFFFFF", fg="#000000", bd=0, padx=10, pady=5, activeforeground="#000000", activebackground="#FFDAB9", cursor="hand2", image=back_image, compound="left")
back_button.place(x=650, y=550)

# 添加元素标签
element_label = tk.Label(window, text="“AI是人类智慧的延伸，而不是取代。”", font=("Arial", 12), bg="#00BFFF", fg="#FFFFFF")
element_label.place(x=20, y=570)

def open_browser_for_search(event):
    item = result_treeview.item(result_treeview.selection())
    name = item['values'][1]
    if name:
        url = 'https://www.baidu.com/s?wd=' + name
        webbrowser.open(url)
        print(name)

result_treeview.bind('<Double-Button-1>', open_browser_for_search)

# 运行GUI窗口
window.mainloop()