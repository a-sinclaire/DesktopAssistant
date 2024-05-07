from tkinter import *
import time
import schedule

timeout = 6*60*60


def job():
    start = time.time()
    root = Tk()
    root.title("DesktopAssistant")
    root.attributes('-fullscreen', 'true')
    root.configure(background='black')
    root.attributes('-transparentcolor', '#000000')
    root.attributes('-topmost', 'true')

    frame = Frame(root)
    frame.pack()

    frameCnt = 2
    frames = [PhotoImage(file='sleepy_claire_small.gif', format='gif -index %i' % i) for i in range(frameCnt)]

    def update(ind):
        global done
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        label.configure(image=frame)
        root.after(400, update, ind)

        if time.time() - start > timeout:
            root.destroy()
        return

    label = Label(root, bg='black', bd=0, highlightthickness=0)
    label.place(relx=1.0, rely=0.0, anchor='ne')
    root.after(0, update, 0)

    root.mainloop()


schedule.every().day.at('23:00').do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
