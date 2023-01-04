from tkinter import *
from chat import get_response, bot_name


font = "Helvetica 14"
font_bold = "Helvetica 14 bold"


class chatapp:
    def __init__(self):
        self.window=Tk()
        self.setup_main_window()

    def run(self):
        self.window.mainloop()

    def setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False) # we dont want window to be sizeable
        self.window.configure(width=470, height=550, bg = 'white')

        head_label = Label(self.window, bg='#8B8B7D', fg='#F0F0FF', text="Welcome", font=font_bold, pady=10)
        head_label.place(relwidth=1)

        line = Label(self.window, width=450, bg = 'grey')
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        #instance variable to use the variable again
        self.text_widget = Text(self.window, width=20, height=2, bg='#F0F0F8', fg='black', font=font, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor='arrow', state=DISABLED)


        #scrollbar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx= 0.974)
        scrollbar.configure(command=self.text_widget.yview)

        bottom_label = Label(self.window, bg='#8B8B7D', height=80)
        bottom_label.place(relwidth=1, rely = 0.835)

        #message panel
        self.msg_entry = Entry(bottom_label, bg='#E0E0EE', fg='black', font=font)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>",self._on_enter_pressed)

        #send_button
        send_button = Button(bottom_label, text="Send", font=font_bold, width=20, bg='#F5F5F5', command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)



    def _on_enter_pressed(self,event):
        msg = self.msg_entry.get()
        self.insert_message(msg, "You")

    def insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0,END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(cursor='arrow', state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(cursor='arrow', state=DISABLED)

        bot_msg = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(cursor='arrow', state=NORMAL)
        self.text_widget.insert(END, bot_msg)
        self.text_widget.configure(cursor='arrow', state=DISABLED)

        self.text_widget.see(END)





if __name__ == "__main__":
    app = chatapp()
    app.run()
