# todo: making a clean sign in/register window | DONE todo: link them above (one "buttonlike" for sign in and one for
#  register) | DONE --> if you click on them the window should switch to log in/register | DONE todo: you should be
#   able to put you data in (register) | DONE todo: save the user | DONE --> in an extern file | DONE --> decode data
#    | IN WORK todo: you should be able to log in | DONE todo: a button which automatically can save the password etc
#     (with the Passwordmanager) | IN WORK todo: if you are logged in (or just registered) there should be a new
#      window (theme isn't important but it should match) | WORKING ON IT todo: button for log out/profile | DONE


# -------
# IMPORTS
# -------
import tkinter as tk
import tkmacosx as tkm
from tkinter import ttk
from PIL import Image, ImageTk
import Decoding_Encoding as de
import random

# ---------
# CONSTANTS
# ----------
width = 1000
height = 600
users = {'Username': ['E-Mail', 'Password', 'Permission', 'Balance', 'Indicator']}
ranks = {"User": "#678983", "Premium": "#FBD148", "VIP": "#4E9F3D", "Moderator": "#32C1CD", "Admin": "#C37B89",
         "Owner": "#8E0505"}
code_ranks = {}
current_user = None

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
numbers = "1234567890"
symbols = "!§$%&/()=?@€{[]}+*~#'-_.:,;<>|"
available_symbols = (letters + numbers + symbols)

# ------
# COLORS
# ------
bg_color = '#333'
fg_color = '#FEC260'

bg_color_startscreen = '#333'
fg_color_startscreen = '#FEC260'

bg_color_extra_frame = '#142F43'

# for buttons
bg_button_active = '#A12568'
bg_button_passive = '#333'
fg_button_active = '#A12568'
fg_button_passive = '#FEC260'
bg_button_hover = '#2A0944'

bg_button_selected = '#684A94'

# for entry
bg_color_entry = "#565656"

# -----
# FONTS
# -----


# -------
# IMAGES
# -------
youtube_path = "youtube_img.png"


class MainSystem(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Login_Register_System_by_Wotan")
        self.geometry(f"{width}x{height}")
        container = tk.Frame(self)
        self.frames = {
            "log_in": LogIn(self, self),
            "sign_up": SignUp(self, self),
            "startscreen": StartScreen(self, self)
        }
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.config(bg=bg_color)
        container.grid(row=0, column=0, stick="nsew")

        # style for notebook (from ttk)
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('URW Gothic', '20'))

        # creates the nav bar
        self.notebook = ttk.Notebook(self, style="TNotebook.Tab")

        self.sign_up = SignUp(self.notebook, self)
        self.log_in = LogIn(self.notebook, self)
        self.start_screen = StartScreen(self.notebook, self)

        # check if tab has changed
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        self.notebook.add(self.log_in, text="Log In", underline=0, )
        self.notebook.add(self.sign_up, text="Sign Up")
        self.notebook.add(self.start_screen, text="Startscreen", state="hidden")

        self.notebook.grid(row=0, column=0, sticky="nswe")

    # hides startscreen tab, if switched to log in or sign up tab
    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "Log In" or tab_text == "Sign Up":
            self.notebook.hide(2)

    # I think I don't need this cause I am using a notebook but maybe for the Startscreen

    def show_frame(self, name):
        frame = self.frames[name]

        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_log_in(self):
        self.show_frame("log_in")

    def show_sign_up(self):
        self.show_frame("sign_up")

    def show_start_screen(self):
        self.show_frame("startscreen")


class LogIn(tk.Frame):
    def __init__(self, master, root):
        tk.Frame.__init__(self, master)

        make_grid(self, 9, 9, )

        self.config(bg=bg_color)

        # general
        self.master = master
        self.root = root

        # Labels
        tk.Label(self, text="Username:", bg=bg_color, fg=fg_color).grid(row=1, column=4, stick="w")
        tk.Label(self, text="Password:", bg=bg_color, fg=fg_color).grid(row=3, column=4, sticky="w")
        self.wrong_password = tk.Label(self, text="Sorry, wrong password!", bg=bg_color, fg="red")
        self.wrong_username = tk.Label(self, text="Sorry, username doesn't exist!", bg=bg_color, fg="red")

        # Entry
        self.username_entry = tk.Entry(self, bg=bg_color, fg=fg_color)
        self.password_entry = tk.Entry(self, show="*", bg=bg_color, fg=fg_color)
        self.username_entry.config(highlightbackground=bg_color_entry, highlightcolor=bg_color_entry)
        self.password_entry.config(highlightbackground=bg_color_entry, highlightcolor=bg_color_entry)
        # Buttons
        self.submit_button = tkm.Button(self, text="Submit", command=lambda: self.logInsubmit(), bg=bg_button_passive,
                                        fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                        overbackground=bg_button_hover)
        self.show_button1 = tkm.CircleButton(self, text="S", radius=18, bg=bg_button_passive,
                                             fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                             overbackground=bg_button_hover)
        exit_button(self)

        # todo: delete this button as soon as the startscreen is finished
        self.insta_log_in = tkm.Button(self, text="Go to start",
                                       command=lambda: [self.master.select(2), insta_log_in_meth()],
                                       bg=bg_button_passive,
                                       fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                       overbackground=bg_button_hover)

        def insta_log_in_meth():
            global current_user
            current_user = list(users)[1]

        # placing widgets
        self.username_entry.grid(row=2, column=4, columnspan=2, sticky="wn")
        self.password_entry.grid(row=4, column=4, columnspan=2, sticky="wn")
        self.submit_button.grid(row=5, column=4)
        self.show_button1.grid(row=4, column=3, sticky="wn")

        self.insta_log_in.grid(row=8, column=0, sticky="n")

        # check if button is pressed/released
        self.show_button1.bind("<ButtonPress-1>", lambda event: self.show_pass(self.password_entry))
        self.show_button1.bind("<ButtonRelease-1>", lambda event: self.hide_pass(self.password_entry))

        # enables to press enter in password entry
        self.password_entry.bind("<Return>", self.logInsubmit)

    def logInsubmit(self, event=None):
        global current_user

        def hide_error_message(label):
            label.grid_remove()

        def grid_error_message(label, row: int = 2, column: int = 3, sticky="n"):
            label.grid(row=row, column=column, sticky=sticky)

        if self.username_entry.get() in users:
            self.wrong_username.grid_remove()
            current_user = self.username_entry.get()
            if users[self.username_entry.get()][1] == self.password_entry.get():
                print(current_user)
                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")
                self.wrong_password.grid_remove()
                self.master.select(2)

        else:
            self.username_entry.delete(0, "end")
            self.wrong_username.grid(row=2, column=6, sticky="n")
            self.after(2000, lambda: hide_error_message(self.wrong_username))
        if users[current_user][1] != self.password_entry:
            self.password_entry.delete(0, "end")
            self.wrong_password.grid(row=4, column=6, sticky="n")
            self.after(2000, lambda: hide_error_message(self.wrong_password))

    def show_pass(self, entry):
        entry.config(show="")  # makes the symbols back normal

    def hide_pass(self, entry):
        entry.config(show="*")  # makes all symbols to '*'


class SignUp(tk.Frame):
    def __init__(self, master, root):
        tk.Frame.__init__(self, master)

        make_grid(self, 9, 9)

        self.config(bg=bg_color)

        # Images
        # self.show_pass_img, self.hide_pass_img = create_imgs()

        # Labels
        self.username_label = tk.Label(self, text="Username:", bg=bg_color, fg=fg_color)
        self.email_label = tk.Label(self, text="E-Mail:", bg=bg_color, fg=fg_color)
        self.password_label = tk.Label(self, text="Password:", bg=bg_color, fg=fg_color)
        self.password_confirm_label = tk.Label(self, text="Confirm Password: ", bg=bg_color, fg=fg_color)

        self.no_username = tk.Label(self, text="Sorry, username is missing or already taken", fg="red", bg=bg_color)
        self.no_email = tk.Label(self, text="Sorry, E-Mail is missing or already taken", fg="red", bg=bg_color)
        self.no_password = tk.Label(self, text="Sorry, password is missing", fg="red", bg=bg_color)
        self.no_password_conf = tk.Label(self, text="Sorry, password is wrong", fg="red", bg=bg_color)

        self.acc_created = tk.Label(self, text="Your account has been created", bg=bg_color, fg=fg_color)

        # Entry
        self.username_entry = tk.Entry(self, bg=bg_color, fg=fg_color)

        self.password_entry = tk.Entry(self, show="*", bg=bg_color, fg=fg_color)
        self.password_confirm_entry = tk.Entry(self, show="*", bg=bg_color, fg=fg_color)
        self.email_entry = tk.Entry(self, bg=bg_color, fg=fg_color)
        self.username_entry.config(highlightbackground=bg_color_entry, highlightcolor=bg_color_entry)
        self.password_entry.config(highlightbackground=bg_color_entry, highlightcolor=bg_color_entry)
        self.password_confirm_entry.config(highlightbackground=bg_color_entry, highlightcolor=bg_color_entry)
        self.email_entry.config(highlightbackground=bg_color_entry, highlightcolor=bg_color_entry)

        # Buttons
        self.submit_button = tkm.Button(self, text="Submit", command=lambda: self.signUp_button(), bg=bg_button_passive,
                                        fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                        overbackground=bg_button_hover)
        self.show_button1 = tkm.CircleButton(self, text="S", radius=18, bg=bg_button_passive,
                                             fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                             overbackground=bg_button_hover)
        self.show_button2 = tkm.CircleButton(self, text="S", radius=18, bg=bg_button_passive,
                                             fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                             overbackground=bg_button_hover)

        exit_button(self)

        # Checkboxes

        # grid widgets
        self.username_label.grid(row=1, column=4, sticky="ws")
        self.username_entry.grid(row=2, column=4, sticky="wn")
        self.email_label.grid(row=2, column=4, sticky="ws")
        self.email_entry.grid(row=3, column=4, sticky="wn")
        self.password_label.grid(row=3, column=4, sticky="ws")
        self.password_entry.grid(row=4, column=4, sticky="wn")
        self.password_confirm_label.grid(row=4, column=4, sticky="ws")
        self.password_confirm_entry.grid(row=5, column=4, sticky="wn")

        self.submit_button.grid(row=6, column=4, sticky="w")

        self.show_button1.grid(row=4, column=3, sticky="wn")
        self.show_button2.grid(row=5, column=3, sticky="wn")

        # check if button is pressed/released
        self.show_button1.bind("<ButtonPress-1>", lambda event: self.show_pass(self.password_entry))
        self.show_button1.bind("<ButtonRelease-1>", lambda event: self.hide_pass(self.password_entry))
        self.show_button2.bind("<ButtonPress-1>", lambda event: self.show_pass(self.password_confirm_entry))
        self.show_button2.bind("<ButtonRelease-1>", lambda event: self.hide_pass(self.password_confirm_entry))

    def signUp_button(self):
        global users

        n = 0

        def hide_label(label, final=False):
            label.grid_remove()
            if final:
                self.master.select(0)

        def check_for_spaces(entry, label, row, column):
            if " " in entry.get():
                label.config(text="You're not allowed to use spaces")
                label.grid(row=row, column=column, sticky="n")
                entry.delete(0, "end")
                self.after(2000, lambda: hide_label(label))

        if self.username_entry.get() == "" or self.username_entry.get() in users:
            self.no_username.config(text="Sorry, username is missing or already taken")
            self.no_username.grid(row=2, column=5, stick="n")
            self.after(2000, lambda: hide_label(self.no_username))

        check_for_spaces(self.username_entry, self.no_username, 2, 5)

        for i in users:
            n += 1 if self.email_entry.get() == users[i][0] else 0

        if self.email_entry.get() == "" or n > 0:
            self.no_email.config(text="Sorry, E-Mail is missing or already taken")
            self.no_email.grid(row=3, column=5, sticky="n")
            self.after(2000, lambda: hide_label(self.no_email))

        check_for_spaces(self.email_entry, self.no_email, 3, 5)

        if self.password_entry.get() == "":
            self.no_password.config(text="Sorry, password is missing")
            self.no_password.grid(row=4, column=5, sticky="n")
            self.after(2000, lambda: hide_label(self.no_password))

        check_for_spaces(self.password_entry, self.no_password, 4, 5)

        if self.password_confirm_entry.get() != "":
            self.no_password_conf.config(text="Sorry, password is wrong")

            if self.password_entry.get() == self.password_confirm_entry.get() and " " not in self.password_entry.get():
                self.no_password_conf.grid_remove()

                if self.username_entry.get() != "" and self.username_entry.get() not in users and self.email_entry.get() != "" and n == 0 and self.password_entry.get() != "":
                    users[self.username_entry.get()] = [self.email_entry.get(), self.password_entry.get(), "User", 100]
                    self.username_entry.delete(0, "end")
                    self.email_entry.delete(0, "end")
                    self.password_entry.delete(0, "end")
                    self.password_confirm_entry.delete(0, "end")

                    print(users)
                    self.acc_created.grid(row=5, column=4, sticky="sw")
                    self.after(2000, lambda: hide_label(self.acc_created, True))

                else:
                    self.password_confirm_entry.delete(0, "end")

            else:
                self.password_confirm_entry.delete(0, "end")
                self.no_password_conf.grid(row=5, column=5, sticky="n")
                self.after(2000, lambda: hide_label(self.no_password_conf))

        else:
            self.no_password_conf.config(text="Sorry but password is missing")
            self.no_password_conf.grid(row=5, column=5, sticky="n")
            self.after(2000, lambda: hide_label(self.no_password_conf))

    def show_pass(self, entry):
        entry.config(show="")  # makes the symbols back normal

    def hide_pass(self, entry):
        entry.config(show="*")  # makes all symbols to '*'


# noinspection PyUnboundLocalVariable
class StartScreen(tk.Frame):
    def __init__(self, master, root):
        tk.Frame.__init__(self, master)

        self.callback_rank_options = None
        self.callback_rank_variable = None
        self.callback_rank_option_menu = tk.OptionMenu(None, None, None)
        self.callback_balance_entry = None
        self.callback_balance_entry = None
        self.callback_password_entry = None
        self.callback_email_entry = None
        self.callback_username_entry = None
        self.active = None
        self.master = master

        make_grid(self, 9, 9)

        self.config(bg=bg_color_startscreen)

        self.buyable_ranks = {}
        for n in ranks:
            if n not in ["Moderator", "Admin", "Owner"]:
                price = 0
                if users[current_user][0] != n:
                    self.buyable_ranks[n] = [price, 0]
                else:
                    self.buyable_ranks[n] = [price, 1]
                price += 10

        # profile
        self.rank_selected = "User"

        # Fonts
        self.copperplate = ("Copperplate Gothic Bold", "15")

        # styles
        self.style = ttk.Style(self)
        self.style.theme_use(
            'classic')  # Problem cause the theme is 'aqua', so the bg does not have the right color (has to be
        # 'classic')

        self.style.configure("Message.TLabel", background=bg_color, foreground=fg_color, font=self.copperplate)
        self.style.configure("Error.Message.TLabel", foreground="red", font=("Copperplate Gothic Bold", "12"))
        self.style.configure("Success.Message.TLabel", font=("Copperplate Gothic Bold", "12"))

        # Frames
        self.start_frame = tk.Frame(self, bg="white")
        self.profile_frame = tk.Frame(self, bg=bg_color)
        self.settings_frame = tk.Frame(self, bg=bg_color)

        self.bind("<Enter>", lambda event: self.update_current_user_widgets())

        # startpage
        self.owner_frame = tk.Frame(self.start_frame, bg=bg_color)

        # profile
        self.button_frame = tk.Frame(self.profile_frame, bg=bg_color)
        self.buy_frame = tk.Frame(self.profile_frame, bg=bg_color)
        self.delete_frame = tk.Frame(self.profile_frame, bg=bg_color)
        self.email_frame = tk.Frame(self.profile_frame, bg=bg_color)

        make_grid(self.start_frame)
        make_grid(self.profile_frame)
        make_grid(self.settings_frame)

        make_grid(self.buy_frame, 2, 2)
        make_grid(self.delete_frame, 6, 2)

        self.owner_frame.columnconfigure(0, weight=1)
        self.owner_frame.rowconfigure(0, weight=1)

        # Labels
        brand_label = tk.Label(self, text="Your Brand", font=("Copperplate Gothic Bold", "30", "underline"),
                               bg=bg_color, fg=fg_color)

        # for startpage
        self.welcome_message = tk.Label(self.start_frame, text=f"Welcome {current_user}",
                                        font=("Copperplate Gothic Bold", "20"),
                                        bg=bg_color, fg=fg_color)
        self.balance_label = tk.Label(self.start_frame, text="Your balance:", bg=bg_color, fg=fg_color,
                                      font=("Copperplate Gothic Bold", 12))
        # for profile
        self.rank_message = tk.Label(self.profile_frame, text="Your rank is:", fg=fg_color, bg=bg_color,
                                     font=self.copperplate)
        self.rank_label = tk.Label(self.profile_frame, text="", bg=bg_color,
                                   fg=ranks[users[current_user][2]], font=self.copperplate)
        self.username_error = tk.Label(self.profile_frame, text="No username", bg=bg_color, fg="red",
                                       font=("Copperplate Gothic Bold", "12"))
        self.username_label = tk.Label(self.profile_frame, text="Username:", bg=bg_color, fg=fg_color,
                                       font=self.copperplate)

        self.change_password_label = tk.Label(self.profile_frame, text="Change password:", bg=bg_color, fg=fg_color,
                                              font=self.copperplate)
        self.password_error_message = tk.Label(self.profile_frame, text="Wrong password", bg=bg_color, fg="red",
                                               font=("Copperplate Gothic Bold", "12"))

        self.buy_rank_label = tk.Label(self.profile_frame, text="Buy ranks", bg=bg_color, fg=fg_color,
                                       font=self.copperplate)
        self.rank_buy_error_label = tk.Label(self.profile_frame, text="Sorry, your rank is higher or the same",
                                             bg=bg_color, fg="red",
                                             font=self.copperplate)

        self.rank_buy_label_price = tk.Label(self.buy_frame, bg=bg_color, fg=fg_color,
                                             font=self.copperplate)
        self.rank_buy_money = tk.Label(self.buy_frame, bg=bg_color, fg=fg_color,
                                       font=("Copperplate Gothic Bold", 12))

        self.delete_account_label = tk.Label(self.delete_frame, text="Delete your account\npermanently?", bg=bg_color,
                                             fg=fg_color, font=("Copperplate Gothic Bold", 12))
        self.delete_message_label = tk.Label(self.delete_frame, text="Successfully deleted", bg=bg_color,
                                             fg=fg_color, font=("Copperplate Gothic Bold", 13))

        self.email_error = tk.Label(self.profile_frame, text="No E-Mail", bg=bg_color, fg="red",
                                    font=("Copperplate Gothic Bold", "12"))
        self.email_label = tk.Label(self.profile_frame, text="E-Mail:", bg=bg_color, fg=fg_color, font=self.copperplate)

        # for settings
        self.rank_code_label = tk.Label(self.settings_frame, text="Type in your code:", bg=bg_color, fg=fg_color,
                                        font=self.copperplate)
        self.rank_code_error_label = tk.Label(self.settings_frame, text="Sorry, this code is does not exist",
                                              bg=bg_color,
                                              fg="red",
                                              font=self.copperplate)

        # Entry

        # for startpage

        # for profile
        self.username_entry = tk.Entry(self.profile_frame, bg=bg_color_entry, fg=fg_color, borderwidth=0,
                                       highlightthickness=0, justify="center", font=("Courier", "18"))

        self.email_entry = tk.Entry(self.profile_frame, bg=bg_color_entry, fg=fg_color, borderwidth=0,
                                    highlightthickness=0, justify="center", font=("Courier", "18"),
                                    disabledforeground=fg_color, disabledbackground=bg_color,
                                    state="disabled")

        self.password_entry = tk.Entry(self.profile_frame, bg=bg_color_entry, fg=fg_color, borderwidth=0,
                                       highlightthickness=0, justify="center", font=("Courier", "18"),
                                       disabledforeground=fg_color, disabledbackground=bg_color)
        self.password_entry.insert(0, "Enter old password")
        self.password_entry.config(state="disabled")
        self.password_entry.bind("<1>", self.activate_pass_entry)
        self.password_entry.bind("<Double-Button-1>", self.deactivate_pass_entry)

        # for settings
        self.rank_code_entry = tk.Entry(self.settings_frame, bg=bg_color_entry, fg=fg_color, borderwidth=0,
                                        highlightthickness=0, justify="center", font=("Courier", "18"),
                                        disabledforeground=fg_color, disabledbackground=bg_color)

        # Buttons
        self.start_page_button = tkm.Button(self, text="Startpage",
                                            command=lambda: [self.selected_button(self.start_page_button),
                                                             self.switching_frame(self.start_frame),
                                                             self.update_current_user_widgets()],
                                            bg=bg_button_selected,
                                            fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                            overbackground=bg_button_hover)
        self.profile_button = tkm.Button(self, text="Your Profile",
                                         command=lambda: [self.selected_button(self.profile_button),
                                                          self.switching_frame(self.profile_frame),
                                                          self.update_current_user_widgets()],
                                         bg=bg_button_passive,
                                         fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                         overbackground=bg_button_hover)
        self.settings_button = tkm.Button(self, text="Settings",
                                          command=lambda: [self.selected_button(self.settings_button),
                                                           self.switching_frame(self.settings_frame)],
                                          bg=bg_button_passive,
                                          fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                          overbackground=bg_button_hover)
        self.log_out_button = tkm.Button(self, text="Log Out", command=lambda: self.log_out(),
                                         bg=bg_button_passive,
                                         fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                         overbackground=bg_button_hover)

        exit_button(self, "Exit", 8, 0, None)
        # for startpage
        self.owner_button = tkm.Button(self.start_frame, text="Access to Owner Panel",
                                       command=lambda: self.show_owner(True),
                                       bg=bg_button_passive,
                                       fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                       overbackground=bg_button_hover)
        self.owner_back_button = tkm.Button(self.start_frame, text="Back",
                                            command=lambda: self.show_owner(False),
                                            bg=bg_button_passive,
                                            fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                            overbackground=bg_button_hover)
        self.hidden = False
        # todo: if you're are owner/admin you can see all users + balance etc and can delete them or change rank
        #  maybe with several buttons, and if you press one, u can see all information for this user

        # for profile
        self.change_name_button = tkm.Button(self.profile_frame, text="Change Name",
                                             command=lambda: [self.username_entry.config(state="normal"),
                                                              self.button_frame.grid(row=2, column=3, sticky="s"),
                                                              self.change_name_button.grid_remove()],
                                             bg=bg_button_passive,
                                             fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                             overbackground=bg_button_hover, font=self.copperplate)
        self.change_name_submit_button = tkm.Button(self.button_frame, text="Submit",
                                                    command=lambda: self.change_username(self.username_entry.get()),
                                                    bg=bg_button_passive,
                                                    fg=fg_button_passive, activebackground=bg_button_active,
                                                    borderless=True,
                                                    overbackground=bg_button_hover, font=self.copperplate)
        self.reset_username_button = tkm.Button(self.button_frame, text="Reset Username",
                                                command=lambda: self.reset_entry_username(self.username_entry),
                                                bg=bg_button_passive,
                                                fg=fg_button_passive, activebackground=bg_button_active,
                                                borderless=True,
                                                overbackground=bg_button_hover, font=self.copperplate)
        self.rank_buy_button = tkm.Button(self.profile_frame, text="Buy Rank",
                                          command=lambda: self.buy_rank(self.rank_variable.get()),
                                          bg=bg_button_passive, fg=fg_button_passive,
                                          activebackground=bg_button_active, borderless=True,
                                          overbackground=bg_button_hover, font=self.copperplate)
        self.rank_buy_button_submit = tkm.Button(self.buy_frame, text="Buy Rank",
                                                 bg=bg_color,
                                                 fg=fg_button_passive, activebackground=bg_button_active,
                                                 borderless=True,
                                                 overbackground=bg_button_hover)
        self.rank_buy_back_button = tkm.Button(self.buy_frame, text="Back",
                                               bg=bg_color,
                                               fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                               overbackground=bg_button_hover)
        self.restore_rank = tkm.Button(self.profile_frame, text="Restore Rank",
                                       bg=bg_color,
                                       fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                       overbackground=bg_button_hover)
        self.delete_account_button = tkm.Button(self.profile_frame, text="Delete Account",
                                                command=lambda: [
                                                    self.delete_frame.grid(row=3, column=4, columnspan=4, rowspan=4,
                                                                           sticky="s"),
                                                    self.delete_account_button.grid_remove()],
                                                bg=bg_color,
                                                fg=fg_button_passive, activebackground=bg_button_active,
                                                borderless=True,
                                                overbackground=bg_button_hover, font=self.copperplate)
        self.delete_account_submit_button = tkm.Button(self.delete_frame, text="Delete",
                                                       command=lambda: self.delete_account(current_user),
                                                       bg=bg_color,
                                                       fg=fg_button_passive, activebackground=bg_button_active,
                                                       borderless=True,
                                                       overbackground=bg_button_hover, font=self.copperplate)
        self.delete_account_cancel_button = tkm.Button(self.delete_frame, text="Cancel",
                                                       command=lambda: [self.delete_frame.grid_remove(),
                                                                        self.delete_account_button.grid(row=5,
                                                                                                        column=6,
                                                                                                        sticky="s")],
                                                       bg=bg_color,
                                                       fg=fg_button_passive, activebackground=bg_button_active,
                                                       borderless=True,
                                                       overbackground=bg_button_hover, font=self.copperplate)
        self.change_email_button = tkm.Button(self.profile_frame, text="Change E-Mail",
                                              command=lambda: [self.email_entry.config(state="normal"),
                                                               self.email_frame.grid(row=2, column=6, sticky="s"),
                                                               self.change_email_button.grid_remove()],
                                              bg=bg_button_passive,
                                              fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
                                              overbackground=bg_button_hover, font=self.copperplate)
        self.change_email_submit_button = tkm.Button(self.email_frame, text="Submit",
                                                     command=lambda: self.change_email(self.email_entry.get()),
                                                     bg=bg_button_passive,
                                                     fg=fg_button_passive, activebackground=bg_button_active,
                                                     borderless=True,
                                                     overbackground=bg_button_hover, font=self.copperplate)
        self.reset_email_button = tkm.Button(self.email_frame, text="Reset E-Mail",
                                             command=lambda: self.reset_entry_email(self.email_entry),
                                             bg=bg_button_passive,
                                             fg=fg_button_passive, activebackground=bg_button_active,
                                             borderless=True,
                                             overbackground=bg_button_hover, font=self.copperplate)

        self.change_password_button = tkm.Button(self.profile_frame, text="Check old password",
                                                 command=lambda: self.change_password(self.password_entry.get()),
                                                 bg=bg_button_passive,
                                                 fg=fg_button_passive, activebackground=bg_button_active,
                                                 borderless=True,
                                                 overbackground=bg_button_hover, font=self.copperplate)
        # for settings
        self.rank_code_submit_button = tkm.Button(self.settings_frame, text="Submit Code",
                                                  command=lambda: self.code_rank_submit(self.rank_code_entry.get()),
                                                  bg=bg_button_passive, fg=fg_button_passive,
                                                  activebackground=bg_button_active, borderless=True,
                                                  overbackground=bg_button_hover, font=self.copperplate)

        # Option Menu
        # todo: making a admin menu with a option menu --> you have a menu, where all users are in, you can choose one and you'll see all data
        # startpage

        self.all_users = []
        self.update_current_user_widgets()
        self.admin_variable = tk.StringVar(self.start_frame)
        self.admin_variable.set(self.all_users[0])
        self.admin_option_menu = tk.OptionMenu(self.start_frame, self.admin_variable, *self.all_users)
        self.admin_option_menu.config(bg=bg_color, fg=fg_color,
                                      activebackground=bg_color,
                                      activeforeground=fg_color,
                                      font=self.copperplate)

        self.admin_variable.trace("w", self.callback_admin)

        # profile
        self.rank_options = ["Choose a rank",
                             "User",
                             "Premium",
                             "VIP"]
        self.rank_variable = tk.StringVar(self.profile_frame)
        self.rank_variable.set(self.rank_options[0])
        self.rank_option_menu = tk.OptionMenu(self.profile_frame, self.rank_variable, *self.rank_options)
        self.rank_option_menu.config(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color,
                                     font=self.copperplate)

        self.rank_variable.trace("w", self.callback_gift_code)

        # SFrame

        # startpage
        self.user_sframe = tkm.SFrame(self.owner_frame, bg="gray", autohidescrollbar=True, scrollbarwidth=0)

        # Grid widgets
        brand_label.grid(row=0, column=0, columnspan=9)

        self.start_page_button.grid(row=1, column=0)
        self.profile_button.grid(row=2, column=0)
        self.settings_button.grid(row=3, column=0)
        self.log_out_button.grid(row=7, column=0)

        self.start_frame.grid(row=1, column=1, rowspan=8, columnspan=8, sticky="nswe", pady=10, padx=10)

        # startpage
        self.welcome_message.grid(row=0, column=0, columnspan=9)

        self.balance_label.grid(row=0, column=9)

        # profile
        self.rank_message.grid(row=0, column=0)
        self.rank_label.grid(row=1, column=0)

        self.username_label.grid(row=0, column=3)
        self.username_entry.grid(row=1, column=3)
        self.change_name_button.grid(row=2, column=3)
        self.change_name_submit_button.grid(row=0, column=1, sticky="w", )
        self.reset_username_button.grid(row=0, column=0, sticky="e")

        self.change_password_label.grid(row=3, column=3)
        self.password_entry.grid(row=4, column=3)
        self.change_password_button.grid(row=5, column=3, sticky="s")

        self.buy_rank_label.grid(row=3, column=0)
        self.rank_option_menu.grid(row=4, column=0)
        self.rank_buy_button.grid(row=5, column=0, sticky="s")

        self.rank_buy_label_price.grid(row=0, column=0, columnspan=2)
        self.rank_buy_money.grid(row=0, column=0, columnspan=2, sticky="s")
        self.rank_buy_back_button.grid(row=1, column=0)
        self.rank_buy_button_submit.grid(row=1, column=1)

        self.delete_account_button.grid(row=5, column=6, sticky="s")
        self.delete_account_label.grid(row=0, column=0, columnspan=2)
        self.delete_account_cancel_button.grid(row=5, column=0)
        self.delete_account_submit_button.grid(row=5, column=1)

        self.email_label.grid(row=0, column=6)
        self.email_entry.grid(row=1, column=6)
        self.change_email_button.grid(row=2, column=6)
        self.change_email_submit_button.grid(row=0, column=1, sticky="w")
        self.reset_email_button.grid(row=0, column=0, sticky="e")

        # settings
        self.rank_code_label.grid(row=1, column=0)
        self.rank_code_entry.grid(row=2, column=0)
        self.rank_code_submit_button.grid(row=3, column=0, sticky="s")

    def show_owner(self, show: bool):
        if show:

            self.admin_option_menu.grid(row=3, column=0, sticky="n")
            self.owner_button.grid_remove()
            self.owner_back_button.grid(row=3, column=0, sticky="s")
            self.callback_rank_option_menu.grid_remove()
            self.hidden = True
        else:
            self.admin_option_menu.grid_remove()
            self.owner_frame.grid_remove()
            self.owner_back_button.grid_remove()
            self.owner_button.grid(row=2, column=0)
            self.hidden = False

    def log_out(self):
        global current_user

        self.username_entry.delete(0, "end")
        self.master.select(0)
        self.selected_button(self.start_page_button)
        self.switching_frame(self.start_frame)
        self.owner_frame.grid_remove()
        self.callback_rank_option_menu.grid_remove()
        self.admin_variable.set(self.all_users[0])
        current_user = None

    def selected_button(self, button):
        button.config(bg=bg_button_selected)
        if button != self.start_page_button:
            self.start_page_button.config(bg=bg_color)
        if button != self.profile_button:
            self.profile_button.config(bg=bg_color)
        if button != self.settings_button:
            self.settings_button.config(bg=bg_color)

    def switching_frame(self, frame):
        for _ in (self.start_frame, self.profile_frame, self.settings_frame):
            if _ == frame:
                frame.grid(row=1, column=1, rowspan=8, columnspan=8, sticky="nswe", pady=10, padx=10)

            elif _ != frame:
                _.grid_remove()

    def update_current_user_widgets(self, color: bool = True):
        self.rank_label.config(text=users[current_user][2], fg=ranks[users[current_user][2]] if color else fg_color)

        self.username_entry.config(state="normal")
        self.username_entry.delete(0, "end")
        self.username_entry.insert(0, current_user)
        self.username_entry.config(disabledforeground=ranks[users[current_user][2]], disabledbackground=bg_color,
                                   state="disabled", fg=ranks[users[current_user][2]])

        self.balance_label.config(text=f"Your balance:\n{users[current_user][3]}$")

        self.email_entry.config(state="normal")
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, users[current_user][0])
        self.email_entry.config(disabledforeground=fg_color, disabledbackground=bg_color,
                                state="disabled", fg=fg_color)
        self.welcome_message.config(text=f"Welcome {current_user}")

        self.welcome_message.config(text=f"Welcome {current_user}!")

        self.deactivate_pass_entry(None)

        self.owner_button.grid_remove()
        if list(ranks).index(users[current_user][2]) >= list(ranks).index("Moderator") and not self.hidden:
            self.owner_button.grid(row=2, column=0)

        elif not self.hidden or list(ranks).index(users[current_user][2]) < list(ranks).index("Moderator"):
            self.owner_frame.grid_remove()
            self.owner_back_button.grid_remove()
            try:
                self.admin_option_menu.grid_remove()
            except AttributeError:
                pass

        for i in list(users):
            self.all_users.append(i)

    def change_username(self, username):
        global users, current_user

        def hide_error_message(label):
            label.grid_remove()

        def grid_error_message(label, row: int = 2, column: int = 3, sticky="n"):
            label.grid(row=row, column=column, sticky=sticky)

        if username == "":
            self.username_error.config(text="No username")
            grid_error_message(self.username_error)
            self.after(2000, lambda: hide_error_message(self.username_error))
            self.username_entry.delete(0, "end")
        elif " " in username:
            self.username_error.config(text="You aren't allowed to use spaces")
            grid_error_message(self.username_error)
            self.after(2000, lambda: hide_error_message(self.username_error))
            self.username_entry.delete(0, "end")
        elif username == current_user:
            self.username_error.config(text="You're already using this name")
            grid_error_message(self.username_error)
            self.after(2000, lambda: hide_error_message(self.username_error))
        elif username in users:
            self.username_error.config(text="This name is already taken")
            grid_error_message(self.username_error)
            self.after(2000, lambda: hide_error_message(self.username_error))
            self.username_entry.delete(0, "end")
        else:
            new_name_label = tk.Label(self.profile_frame, text="New name set", bg=bg_color, fg=fg_color,
                                      font=self.copperplate)
            grid_error_message(new_name_label)
            self.after(2000,
                       lambda: [hide_error_message(new_name_label), hide_error_message(self.button_frame)])
            users = rename_dic(users, current_user, username)
            current_user = username
            print(f"New name: {current_user}")
            self.username_entry.config(state="disabled")
            self.after(2000, lambda: grid_error_message(self.change_name_button, 2, 3))

    def change_email(self, email):
        global users

        current_email = users[current_user][0]
        counter = 0

        def hide_error_message(label):
            label.grid_remove()

        def grid_error_message(label, row: int = 2, column: int = 6, sticky="n"):
            label.grid(row=row, column=column, sticky=sticky)

        if email == "":
            self.email_error.config(text="No E-Mail")
            grid_error_message(self.email_error)
            self.after(2000, lambda: hide_error_message(self.email_error))
            self.username_entry.delete(0, "end")
            counter += 1
        elif " " in email:
            self.email_error.config(text="You aren't allowed to use spaces")
            grid_error_message(self.email_error)
            self.after(2000, lambda: hide_error_message(self.email_error))
            self.username_entry.delete(0, "end")
            counter += 1
        elif email == current_email:
            self.email_error.config(text="You're already using this E-Mail")
            grid_error_message(self.email_error)
            self.after(2000, lambda: hide_error_message(self.email_error))
            counter += 1
        for _ in users:
            if email == users[_][0] and email != current_email:
                self.email_error.config(text="This E-Mail is already taken")
                grid_error_message(self.email_error)
                self.after(2000, lambda: hide_error_message(self.email_error))
                self.email_entry.delete(0, "end")
                counter += 1
        if counter == 0:
            new_name_label = tk.Label(self.profile_frame, text="New E-Mail set", bg=bg_color, fg=fg_color,
                                      font=self.copperplate)
            grid_error_message(new_name_label)
            self.after(2000,
                       lambda: [hide_error_message(new_name_label), hide_error_message(self.email_frame)])
            users[current_user][0] = email
            users = rename_dic(users, users[current_user][0], email)

            print(f"New E-Mail: {users[current_user][0]}")
            self.email_entry.config(state="disabled")
            self.after(2000, lambda: grid_error_message(self.change_email_button, 2, 6))

    def change_password(self, password, checked: bool = False):
        global users
        old_password = users[current_user][1]

        def hide_error_message(label):
            label.grid_remove()

        def grid_error_message(label, row: int = 5, column: int = 3, sticky="n"):
            label.grid(row=row, column=column, sticky=sticky)

        current_password = users[current_user][1]
        if not self.active:
            pass
        elif checked:
            if password == "":
                self.password_error_message.config(text="No Password")
                grid_error_message(self.password_error_message)
                self.after(2000, lambda: hide_error_message(self.password_error_message))
            elif " " in password:
                self.password_error_message.config(text="You aren't allowed to use spaces")
                grid_error_message(self.password_error_message)
                self.after(2000, lambda: hide_error_message(self.password_error_message))
            elif password == current_password:
                self.password_error_message.config(text="You already using this password")
                grid_error_message(self.password_error_message)
                self.after(2000, lambda: hide_error_message(self.password_error_message))
            else:
                users[current_user][1] = password
                new_label = tk.Label(self.profile_frame, text="New password set", bg=bg_color, fg=fg_color,
                                     font=self.copperplate)
                grid_error_message(new_label)
                self.after(2000,
                           lambda: [hide_error_message(new_label), hide_error_message(self.password_error_message)])
                self.password_entry.delete(0, "end")
                self.password_entry.insert(0, "Enter old password")
                self.password_entry.config(state="disabled")
                self.change_password_button.config(text="Check old password",
                                                   command=lambda: self.change_password(self.password_entry.get()))
                self.active = False
        elif not checked:
            if password == old_password:
                label = tk.Label(self.profile_frame, text="Correct!", fg=fg_color, bg=bg_color,
                                 font=("Copperplate Gothic Bold", "12"))
                grid_error_message(label)
                self.after(2000, lambda: [hide_error_message(label),
                                          self.password_entry.delete(0, "end"),
                                          self.change_password_button.config(text="Change Password",
                                                                             command=lambda: self.change_password(
                                                                                 self.password_entry.get(), True))])
            else:
                self.password_error_message.config(text="Incorrect!")
                grid_error_message(self.password_error_message)
                self.after(2000, lambda: hide_error_message(self.password_error_message))
                self.password_entry.delete(0, "end")

    def activate_pass_entry(self, event):
        self.active = True
        self.password_entry.config(state="normal")
        self.password_entry.delete(0, "end")

    def deactivate_pass_entry(self, event):
        self.active = False
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, "Enter old password")
        self.password_entry.config(state="disabled")
        self.change_password_button.config(text="Check old password",
                                           command=lambda: self.change_password(self.password_entry.get()))

        self.password_entry.delete(0, "end")

    def reset_entry_username(self, entry):
        entry.delete(0, "end")
        entry.insert(0, current_user)
        self.after(500, lambda: [self.change_name_button.grid(row=2, column=3), self.button_frame.grid_remove(),
                                 self.username_entry.config(state="disabled")])

    def reset_entry_email(self, entry):
        entry.delete(0, "end")
        entry.insert(0, users[current_user][0])
        self.after(500, lambda: [self.change_email_button.grid(row=2, column=6), self.email_frame.grid_remove(),
                                 self.email_entry.config(state="disabled")])

    def check_entry_text(self, text, old_text):
        if text == "":
            return False
        elif " " in text:
            return False
        elif text == old_text:
            return False
        else:
            return True

    def callback_admin(self, *args):

        def activate_entry(entry):
            nonlocal own_rank_index
            if self.admin_variable.get() != "Username" and list(ranks)[(own_rank_index)] == "Owner" or list(
                    ranks).index(users[current_user][2]) > list(
                ranks).index(
                users[self.admin_variable.get()][2]):
                entry.config(state="normal")
                if entry == self.callback_password_entry:
                    entry.config(show="")

        def deactivate_entry(entry):
            if entry == self.callback_password_entry:
                entry.config(show="*")
            entry.config(state="disabled")

        def callback(*args):
            pass

        def create_buttons(grid: list, textes=None):
            if textes is None:
                textes = ["Reset", 'Submit']

            reset_button = tkm.Button(self.owner_frame, text=textes[0],
                                      bg=bg_button_passive,
                                      fg=fg_button_passive, activebackground=bg_button_active,
                                      borderless=True,
                                      overbackground=bg_button_hover, font=self.copperplate)
            submit_button = tkm.Button(self.owner_frame, text=textes[1],
                                       bg=bg_button_passive,
                                       fg=fg_button_passive, activebackground=bg_button_active,
                                       borderless=True,
                                       overbackground=bg_button_hover, font=self.copperplate)

            reset_button.grid(row=grid[0], column=grid[1])
            submit_button.grid(row=grid[0], column=grid[1] + 1)

            return reset_button, submit_button

        def change_parameter(widget, user, grid: list, indices, menu: bool = False, options: tk.StringVar = None):
            nonlocal chosen_user, own_rank_index
            global users

            def create_message(text, grid: list, error: bool = True):
                if error:
                    error_message = ttk.Label(self.owner_frame, text=f"{text} can not be set",
                                              style="Error.Message.TLabel")
                    error_message.grid(row=grid[0], column=grid[1])
                    self.after(2000, lambda: error_message.grid_remove())
                else:
                    message = ttk.Label(self.owner_frame, text=f"{text} successfully set",
                                        style="Success.Message.TLabel")
                    message.grid(row=grid[0], column=grid[1])
                    self.after(2000, lambda: message.grid_remove())

            if user != "Username" and list(ranks)[(own_rank_index)] == "Owner" or own_rank_index >= list(ranks).index(
                    users[user][2]):
                if not menu:

                    new_parameter = widget.get()
                    try:
                        if self.check_entry_text(new_parameter, users[user][indices]):
                            users[user][indices] = new_parameter
                            print(f"{user}'s New {users['Username'][indices]}: {new_parameter}")
                            create_message(users["Username"][indices], grid, False)
                            widget.config(state="disabled")
                        else:
                            create_message(users["Username"][indices], grid)
                            reset_parameter(widget, user, indices)

                    except TypeError:
                        print("Username can not be edited so far ")  # Username can not be edited so far
                        reset_parameter(widget, user, None)  # todo: Username edit
                        """if new_parameter != list(users)[list(users).index(user)]: 
                            users = rename_dic(users, user, new_parameter)
                            print(f"{user}'s New Username: {new_parameter}")
                            self.admin_variable.set(self.all_users[list(users).index(new_parameter)])
                            chosen_user = self.admin_variable.get()"""

                else:
                    selection = options.get()

                    selection_index = list(ranks).index(selection)
                    if own_rank_index > selection_index and own_rank_index >= list(ranks).index(
                            "Moderator") and selection != users[user][2]:
                        create_message("Rank", grid, False)
                        users[user][2] = selection
                        print(f"{user}'s new rank: {users[user][2]}")
                    else:
                        create_message("Rank", grid)
                        self.callback_rank_variable.set(users[chosen_user][2])

        def reset_parameter(widget, user, indices, menu: bool = False):
            try:
                if not menu:
                    widget.config(state="normal")
                    widget.delete(0, "end")
                    if indices is None:
                        widget.insert(0, list(users)[list(users).index(user)])
                    else:
                        widget.insert(0, users[user][indices])
                    widget.config(state="disabled")
                else:
                    self.callback_rank_variable.set(users[user][indices])
            except AttributeError:
                print("Error")
                pass

        chosen_user = self.admin_variable.get()
        own_rank_index = list(ranks).index(users[current_user][2])

        username_label = ttk.Label(self.owner_frame, text="Username: ", style="Message.TLabel")
        email_label = ttk.Label(self.owner_frame, text="E-Mail: ", style="Message.TLabel")
        password_label = ttk.Label(self.owner_frame, text="Password: ", style="Message.TLabel")
        rank_label = ttk.Label(self.owner_frame, text="Rank: ", style="Message.TLabel")
        balance_label = ttk.Label(self.owner_frame, text="Balance: ", style="Message.TLabel")

        # I don't really know why, but somehow I can't pass the command through the method, so I have to config it manually
        username_reset_button, username_submit_button = create_buttons([0, 2])
        username_reset_button.config(command=lambda: reset_parameter(self.callback_username_entry, chosen_user, None))
        username_submit_button.config(
            command=lambda: change_parameter(self.callback_username_entry, chosen_user, [0, 4], None))

        email_reset_button, email_submit_button = create_buttons([1, 2])
        email_reset_button.config(command=lambda: reset_parameter(self.callback_email_entry, chosen_user, 0))
        email_submit_button.config(command=lambda: change_parameter(self.callback_email_entry, chosen_user, [1, 4], 0))

        password_reset_button, passsword_submit_button = create_buttons([2, 2])
        password_reset_button.config(command=lambda: reset_parameter(self.callback_password_entry, chosen_user, 1))
        passsword_submit_button.config(
            command=lambda: change_parameter(self.callback_password_entry, chosen_user, [2, 4], 1))

        rank_reset_button, rank_submit_button = create_buttons([3, 2])
        rank_reset_button.config(command=lambda: reset_parameter(self.callback_rank_option_menu, chosen_user, 2, True))
        rank_submit_button.config(
            command=lambda: change_parameter(self.callback_rank_option_menu, chosen_user, [3, 4], 2, True,
                                             self.callback_rank_variable))

        balance_reset_button, balance_submit_button = create_buttons([4, 2])
        balance_reset_button.config(command=lambda: reset_parameter(self.callback_balance_entry, chosen_user, 3))
        balance_submit_button.config(
            command=lambda: change_parameter(self.callback_balance_entry, chosen_user, [4, 4], 3))

        if not self.owner_frame.winfo_ismapped():
            self.callback_username_entry = tk.Entry(self.owner_frame, background=bg_color_entry, foreground=fg_color,
                                                    borderwidth=0,
                                                    highlightthickness=0, justify="center", font=("Courier", "18"),
                                                    disabledforeground=fg_color, disabledbackground=bg_color)
            self.callback_email_entry = tk.Entry(self.owner_frame, background=bg_color_entry, foreground=fg_color,
                                                 borderwidth=0,
                                                 highlightthickness=0, justify="center", font=("Courier", "18"),
                                                 disabledforeground=fg_color, disabledbackground=bg_color)
            self.callback_password_entry = tk.Entry(self.owner_frame, background=bg_color_entry, foreground=fg_color,
                                                    borderwidth=0,
                                                    highlightthickness=0, justify="center", font=("Courier", "18"),
                                                    disabledforeground=fg_color, disabledbackground=bg_color)
            self.callback_balance_entry = tk.Entry(self.owner_frame, background=bg_color_entry, foreground=fg_color,
                                                   borderwidth=0,
                                                   highlightthickness=0, justify="center", font=("Courier", "18"),
                                                   disabledforeground=fg_color, disabledbackground=bg_color)

            self.callback_rank_options = list(ranks)
            self.callback_rank_variable = tk.StringVar(self.owner_frame)
            self.callback_rank_option_menu = tk.OptionMenu(self.owner_frame, self.callback_rank_variable,
                                                           *self.callback_rank_options)

        # that's not the cleanest solution, but I don't really know how I could do it better
        self.callback_rank_option_menu.config(bg=bg_color, fg=fg_color, activebackground=bg_color,
                                              activeforeground=fg_color,
                                              font=self.copperplate)
        self.callback_rank_variable.set(users[chosen_user][2])

        self.callback_rank_variable.trace("w", callback)

        self.callback_username_entry.config(state="normal")
        self.callback_username_entry.delete(0, "end")
        self.callback_username_entry.insert(0, chosen_user)
        self.callback_username_entry.config(state="disabled")

        self.callback_email_entry.config(state="normal")
        self.callback_email_entry.delete(0, "end")
        self.callback_email_entry.insert(0, users[chosen_user][0])
        self.callback_email_entry.config(state="disabled")

        self.callback_password_entry.config(state="normal", show="*")
        self.callback_password_entry.delete(0, "end")
        self.callback_password_entry.insert(0, users[chosen_user][1])
        self.callback_password_entry.config(state="disabled")

        self.callback_balance_entry.config(state="normal")
        self.callback_balance_entry.delete(0, "end")
        self.callback_balance_entry.insert(0, users[chosen_user][3])
        self.callback_balance_entry.config(state="disabled")

        self.callback_username_entry.bind("<1>", lambda event: activate_entry(self.callback_username_entry))
        self.callback_username_entry.bind("<Double-Button-1>",
                                          lambda event: deactivate_entry(self.callback_username_entry))
        self.callback_username_entry.bind("<Return>",
                                          lambda event: change_parameter(self.callback_username_entry, chosen_user,
                                                                         [0, 4], None))

        self.callback_email_entry.bind("<1>", lambda event: activate_entry(self.callback_email_entry))
        self.callback_email_entry.bind("<Double-Button-1>", lambda event: deactivate_entry(self.callback_email_entry))
        self.callback_email_entry.bind("<Return>",
                                       lambda event: change_parameter(self.callback_email_entry, chosen_user, [1, 4],
                                                                      0))

        self.callback_password_entry.bind("<1>", lambda event: activate_entry(self.callback_password_entry))
        self.callback_password_entry.bind("<Double-Button-1>",
                                          lambda event: deactivate_entry(self.callback_password_entry))
        self.callback_password_entry.bind("<Return>",
                                          lambda event: change_parameter(self.callback_password_entry, chosen_user,
                                                                         [2, 4], 1))

        self.callback_balance_entry.bind("<1>", lambda event: activate_entry(self.callback_balance_entry))
        self.callback_balance_entry.bind("<Double-Button-1>",
                                         lambda event: deactivate_entry(self.callback_balance_entry))
        self.callback_balance_entry.bind("<Return>",
                                         lambda event: change_parameter(self.callback_balance_entry, chosen_user,
                                                                        [4, 4], 3))

        self.owner_frame.grid(row=3, column=4)

        if not self.owner_frame.winfo_ismapped():
            username_label.grid(row=0)
            email_label.grid(row=1)
            password_label.grid(row=2)
            rank_label.grid(row=3)
            balance_label.grid(row=4)

            self.callback_username_entry.grid(row=0, column=1)
            self.callback_email_entry.grid(row=1, column=1)
            self.callback_password_entry.grid(row=2, column=1)
            self.callback_balance_entry.grid(row=4, column=1)

            self.callback_rank_option_menu.grid(row=3, column=1)

    def callback_gift_code(self, *args):
        rank_color = self.rank_variable.get()
        if rank_color in ranks:
            self.rank_option_menu.config(fg=ranks[rank_color])
            self.rank_selected = rank_color
        else:
            self.rank_option_menu.config(fg=fg_color)

    def buy_rank(self, rank):
        def hide_error_message(label):
            label.grid_remove()

        def grid_error_message(label, row: int = 5, column: int = 0, columnspan: int = 1, rowspan: int = 1, sticky="n"):
            label.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky=sticky)

        def hide_for_buy_frame():
            self.buy_rank_label.grid_remove()
            self.rank_option_menu.grid_remove()
            self.rank_buy_button.grid_remove()

        def grid_for_buy_frame():
            self.buy_rank_label.grid(row=3, column=0)
            self.rank_option_menu.grid(row=4, column=0)
            self.rank_buy_button.grid(row=5, column=0, sticky="s")

        def check_buyable(money):
            if money > price:
                users[current_user][3] -= price
                users[current_user][2] = rank
                self.update_current_user_widgets()

        price = 0

        if rank in self.buyable_ranks:
            for n in range(list(ranks).index(rank)):
                price += 10
            if list(ranks).index(users[current_user][2]) < list(ranks).index(rank):
                grid_error_message(self.buy_frame, 3, 0, 2, 3, "nswe")
                hide_for_buy_frame()

                self.rank_buy_money.config(text=f"Your Balance: {users[current_user][3]}$")
                self.rank_buy_label_price.config(text=f"Buy {rank} for {price}$?")
                self.rank_buy_back_button.config(
                    command=lambda: [hide_error_message(self.buy_frame), grid_for_buy_frame()])
                self.rank_buy_button_submit.config(command=lambda: [check_buyable(users[current_user][3]),
                                                                    hide_error_message(self.buy_frame),
                                                                    grid_for_buy_frame()])

            else:
                self.rank_buy_error_label.config(text="Sorry, your rank is higher or the same",
                                                 font=("Copperplate Gothic Bold", 12))
                grid_error_message(self.rank_buy_error_label)
                self.after(2000, lambda: hide_error_message(self.rank_buy_error_label))
        else:
            self.rank_buy_error_label.config(text="Sorry, this isn't an option", font=self.copperplate)
            grid_error_message(self.rank_buy_error_label)
            self.after(2000, lambda: hide_error_message(self.rank_buy_error_label))

    def code_rank_submit(self, code):
        global users

        def hide_error_message(label):
            label.grid_remove()

        def grid_error_message(label, row: int = 3, column: int = 0, sticky="n"):
            label.grid(row=row, column=column, sticky=sticky)

        if code in list(code_ranks):
            if list(ranks).index(code_ranks[code]) > list(ranks).index(users[current_user][2]):
                self.rank_code_error_label.config(text="Congratulations, you found a correct code!", fg=fg_color,
                                                  font=("Copperplate Gothic Bold", 12))
                users[current_user][2] = code_ranks[code]
                print(f"New rank: {code_ranks[code]}")
                grid_error_message(self.rank_code_error_label)
                self.after(2000, lambda: hide_error_message(self.rank_code_error_label))
                self.rank_code_entry.delete(0, "end")
                self.update_current_user_widgets()

            else:
                self.rank_code_error_label.config(text="Sorry, your rank is higher", fg="red", font=self.copperplate)
                grid_error_message(self.rank_code_error_label)
                self.after(2000, lambda: hide_error_message(self.rank_code_error_label))
                self.rank_code_entry.delete(0, "end")

        else:
            self.rank_code_error_label.config(text="Sorry, this code is does not exist", fg="red",
                                              font=self.copperplate)
            grid_error_message(self.rank_code_error_label)
            self.after(2000, lambda: hide_error_message(self.rank_code_error_label))
            self.rank_code_entry.delete(0, "end")

    def restore_rank(self):  # todo: first only the current rank price, later maybe for all purchases too
        pass

    def delete_account(self, account):
        global current_user

        def hide():
            self.delete_frame.grid_remove()
            self.delete_account_button.grid(row=5, column=6, sticky="s")
            self.master.select(0)
            users.pop(account)
            print(f"Deleted Account: {account}")

        self.delete_message_label.grid(row=4, column=0, columnspan=2, sticky="n")
        self.after(2000, lambda: hide())
        current_user = "Username"

    def sframe_startpage(self, account, rank):

        self.user_sframe.grid(ipadx=50)
        button_list = []
        if rank in ["Owner", "Admin"]:
            self.owner_frame.grid(row=2, column=0, columnspan=3, rowspan=3)

        if rank and list(ranks).index(rank) >= list(ranks).index("Moderator"):
            for n in users:
                if n != "Username" and list(ranks).index(rank) > list(ranks).index(users[n][2]):
                    tk.Label(self.user_sframe, text=n, bg=bg_color, fg=fg_color, font=self.copperplate).grid(
                        row=list(users).index(n))
                    tk.Label(self.user_sframe, text="     ", bg=bg_color, fg=fg_color, font=self.copperplate)
                    button_list.append(tkm.Button(self.user_sframe, text="Inspect User",
                                                  command=lambda: self.open_user_information(n),
                                                  bg=bg_button_passive,
                                                  fg=fg_button_passive, activebackground=bg_button_active,
                                                  borderless=True,
                                                  overbackground=bg_button_hover, font=self.copperplate))
                    # todo: remake (buttons only shows the last person)

    def open_user_information(self, account):
        self.user_sframe.grid_remove()
        tk.Label(self.owner_frame, text=account, bg=bg_color, fg=fg_color, font=self.copperplate).grid()
        tk.Label(self.owner_frame, text="Password").grid()

        tk.Label(self.owner_frame, text="E-Mail").grid()

        tk.Label(self.owner_frame, text="Permission").grid()

        tk.Label(self.owner_frame, text="Balance").grid()


# ---------
# FUNCTIONS
# ---------
def make_grid(master, row_number: int = 9, column_number: int = 9, show_grid=False):
    for r in range(row_number):
        master.rowconfigure(r, weight=1, minsize=10)
        for c in range(column_number):
            master.columnconfigure(c, weight=1, minsize=10)
    if show_grid:
        for r in range(row_number):
            for c in range(column_number):
                tk.Button(master, text="").grid(row=r, column=c, sticky="nswe")


def exit_button(root, text="Exit", row=8, column=8, sticky="nw", font=None, bg=bg_button_passive, fg=fg_button_passive,
                activebg=bg_button_active, overbg=bg_button_hover):
    tkm.Button(root, text=text, command=lambda: [root.quit(), save_data("users", users)], font=font, bg=bg,
               fg=fg, activebackground=activebg, borderless=True,
               overbackground=overbg).grid(row=row, column=column, sticky=sticky)


def back_button(self, root, text="Back to menu", row=8, column=0):
    tkm.Button(self, text=text, command=lambda: root.show_title(), bg=bg_button_passive,
               fg=fg_button_passive, activebackground=bg_button_active, borderless=True,
               overbackground=bg_button_hover).grid(row=row, column=column, padx=25, sticky="n")


# using images is working, but these aren't so clean, so I am using text instead
def create_imgs():
    show_pass_img = tk.PhotoImage(file=r"img_show2.png")
    hide_pass_img = tk.PhotoImage(file=r"img_hide2.png")
    show_pass_img = show_pass_img.subsample(35, 35)
    hide_pass_img = hide_pass_img.subsample(35, 35)
    return show_pass_img, hide_pass_img


def show_img(root, grid: list, path):
    img = ImageTk.PhotoImage(Image.open(path))
    row, column, sticky = grid
    panel = tk.Label(root, image=img)
    panel.grid(row=row, column=column, sticky=sticky)


def save_data(file, dic):
    with open(file, "w") as f:
        for n in dic:
            indicator = random.randint(1, len(available_symbols))
            word = de.encoding(str(n), indicator, available_symbols) if n != "Username" else n
            f.write(word)
            for i in dic[n]:
                word = de.encoding(str(i), indicator, available_symbols) if n != "Username" else i
                f.write(f" {word}")
            f.write(f" {str(indicator)}")
            f.write("\n")


def load_data(file):
    global users, current_user
    with open(file, "r") as f:
        if file == "users":
            f.readline()
            for line in f:
                key, email, password, user_type, currency, indicator = line.split()  # splits one line (separated with spaces) in separate elements

                key = de.decoding(key, int(indicator), available_symbols)
                email = de.decoding(email, int(indicator), available_symbols)
                password = de.decoding(password, int(indicator), available_symbols)
                user_type = de.decoding(user_type, int(indicator), available_symbols)
                currency = de.decoding(currency, int(indicator), available_symbols)

                users[key] = [email, password, user_type, int(currency)]
        elif file == "codes":
            f.readline()
            for line in f:
                (code, activated_rank) = line.split()
                code_ranks[code] = activated_rank

    if file == "users":
        current_user = list(users)[2]


def rename_dic(old_dict, old_name, new_name):
    new_dict = {}
    for key, value in zip(old_dict.keys(), old_dict.values()):
        new_key = key if key != old_name else new_name
        new_dict[new_key] = old_dict[key]
    return new_dict


if __name__ == "__main__":
    load_data("users")
    print(users)
    load_data("codes")

    App = MainSystem()

    App.mainloop()

    save_data("users", users)
