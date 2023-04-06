from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
import c, threading


    
def do():
    root=Tk()
    wrapper=Frame(root)
    wrapper.pack(fill=BOTH, expand=1)

    mycanvas=Canvas(wrapper)
    mycanvas.pack(side=LEFT, fill=BOTH, expand=1)

    yscrollbars=ttk.Scrollbar(wrapper, orient=VERTICAL, command=mycanvas.yview)
    yscrollbars.pack(side=RIGHT, fill='y')

    mycanvas.configure(yscrollcommand=yscrollbars.set)

    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))


    frames=Frame(mycanvas)
    mycanvas.create_window((0,0), window=frames, anchor="nw")

    wrapper.pack(fill="both", expand="yes", padx=10, pady=10)
    #############################################################


    Button(frames, text="KESHI NOVUS STATS",width=55).pack()#
    wrapper1=LabelFrame(frames, height=100, width=200)
    wrapper2=LabelFrame(frames, height=100, width=200)
    wrapper3=LabelFrame(frames, height=100, width=200)
    wrapper4=LabelFrame(frames, height=100, width=200)

    mycanva=Canvas(wrapper1, height=125, width=360)
    mycanva.pack(side=LEFT)

    mycanva2=Canvas(wrapper2, height=125, width=360)
    mycanva2.pack(side=LEFT)

    mycanva3=Canvas(wrapper3, height=125, width=360)
    mycanva3.pack(side=LEFT)

    mycanva4=Canvas(wrapper4, height=125, width=360)
    mycanva4.pack(side=LEFT)


    yscrollbar=ttk.Scrollbar(wrapper1, orient="vertical", command=mycanva.yview)
    yscrollbar.pack(side=RIGHT, fill='y')

    yscrollbar2=ttk.Scrollbar(wrapper2, orient="vertical", command=mycanva2.yview)
    yscrollbar2.pack(side=RIGHT, fill='y')

    yscrollbar3=ttk.Scrollbar(wrapper3, orient="vertical", command=mycanva3.yview)
    yscrollbar3.pack(side=RIGHT, fill='y')

    yscrollbar4=ttk.Scrollbar(wrapper4, orient="vertical", command=mycanva4.yview)
    yscrollbar4.pack(side=RIGHT, fill='y')


    mycanva.configure(yscrollcommand=yscrollbar.set)

    mycanva.bind('<Configure>', lambda e: mycanva.configure(scrollregion=mycanva.bbox('all')))

    mycanva2.configure(yscrollcommand=yscrollbar2.set)

    mycanva2.bind('<Configure>', lambda e: mycanva2.configure(scrollregion=mycanva2.bbox('all')))

    mycanva3.configure(yscrollcommand=yscrollbar3.set)

    mycanva3.bind('<Configure>', lambda e: mycanva3.configure(scrollregion=mycanva3.bbox('all')))

    mycanva4.configure(yscrollcommand=yscrollbar4.set)

    mycanva4.bind('<Configure>', lambda e: mycanva4.configure(scrollregion=mycanva4.bbox('all')))


    def _on_mouse_wheel(event):
        mycanvas.yview_scroll(-1 * int((event.delta / 100)), "units")
        mycanva.yview_scroll(-1 * int((event.delta / 100)), "units")
        mycanva2.yview_scroll(-1 * int((event.delta / 100)), "units")
        mycanva3.yview_scroll(-1 * int((event.delta / 100)), "units")
        mycanva4.yview_scroll(-1 * int((event.delta / 100)), "units")

    mycanvas.bind_all("<MouseWheel>", _on_mouse_wheel)
    mycanva.bind_all("<MouseWheel>", _on_mouse_wheel)
    mycanva2.bind_all("<MouseWheel>", _on_mouse_wheel)
    mycanva3.bind_all("<MouseWheel>", _on_mouse_wheel)
    mycanva4.bind_all("<MouseWheel>", _on_mouse_wheel)


    frame=Frame(mycanva)
    mycanva.create_window((0,0), window=frame, anchor="nw")

    frame2=Frame(mycanva2)
    mycanva2.create_window((0,0), window=frame2, anchor="nw")

    frame3=Frame(mycanva3)
    mycanva3.create_window((0,0), window=frame3, anchor="nw")

    frame4=Frame(mycanva4)
    mycanva4.create_window((0,0), window=frame4, anchor="nw")

    wrapper1.pack(fill="both", expand="yes", padx=2, pady=2)
    wrapper2.pack(fill="both", expand="yes", padx=2, pady=2)
    wrapper3.pack(fill="both", expand="yes", padx=2, pady=2)
    wrapper4.pack(fill="both", expand="yes", padx=2, pady=2)
    #wrapper3.pack(fill="both", expand="yes", padx=7, pady=7)

    # Create text widget and specify size.
    T = Text(frame, height = 5, width = 52)
    #T.config(font=("Times New Roman", 8, "bold"))
    # Create label
    l = Label(frame, text = "1-HOUR CANDLESTICK")
    l.config(font =("Courier", 14))
    PG = c.strl
    l.pack()
    T.pack()
    T.insert(tk.END, PG)

    # Create text widget and specify size.
    T2 = Text(frame2, height = 5, width = 52)
    #T2.config(font=("Times New Roman", 8, "bold"))
    # Create label
    l2 = Label(frame2, text = "15-MIN CANDLESTICK")
    l2.config(font =("Courier", 14))
    PG2 = c.strl2
    l2.pack()
    T2.pack()
    T2.insert(tk.END, PG2)


    # Create text widget and specify size.
    T3 = Text(frame3, height = 5, width = 52)
    #T3.config(font=("Times New Roman", 8, "bold"))
    # Create label
    l3 = Label(frame3, text = "5-MIN CANDLESTICK")
    l3.config(font =("Courier", 14))
    PG3 = c.strl3
    l3.pack()
    T3.pack()
    T3.insert(tk.END, PG3)

    # Create text widget and specify size.
    T4 = Text(frame4, height = 5, width = 52)
    #T4.config(font=("Times New Roman", 8,"bold"))
    # Create label
    l4 = Label(frame4, text = "1-MIN CANDLESTICK")
    l4.config(font =("Courier", 14))
    PG4 = c.strl4
    l4.pack()
    T4.pack()
    T4.insert(tk.END, PG4)

        
    root.geometry("420x270")#420x270
    root.resizable(False, False)
    root.title("CormacKesh")
    root.mainloop()


    while True:
        T.delete(1.0,"end")
        T.insert(tk.END, c.strl)

        T2.delete(1.0,"end")
        T2.insert(tk.END, c.strl2)

        T3.delete(1.0,"end")
        T3.insert(tk.END, c.strl3)

        T4.delete(1.0,"end")
        T4.insert(tk.END, c.strl4)
        time.sleep(5)