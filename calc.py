import tkinter as tk;
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"



# Calculator class with dimension, title
class Calculator:
    def __init__(self):
        self.window = tk.Tk();
        self.window.geometry("400x667");
        self.window.resizable(0,0);
        self.window.title("Calculator");
        self.display_frame = self.create_display_frame();
        self.total_expression = "";
        self.current_expression = "";
        self.total_label, self.label = self.create_display_labels();
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"};
        self.buttons_frame = self.create_buttons_frame();
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.bind_keys();
        self.create_digit_buttons();
        self.create_operator_buttons();
        self.create_special_buttons();
    
    def run(self):
            self.window.mainloop();
    

# create special button
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()


# display label
    def create_display_labels(self):
        total_label=tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, font=SMALL_FONT_STYLE);
        total_label.pack(expand=True, fill="both")
        label=tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, font=LARGE_FONT_STYLE);
        label.pack(expand=True, fill="both")
        return total_label,label;


# create button based on digits
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), font=DIGITS_FONT_STYLE, borderwidth=0, bg=WHITE, fg=LABEL_COLOR, command=lambda x=digit: self.add_to_expression(x));
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW);
           

# create button based on operator
    def create_operator_buttons(self):
        i=0
        for operators, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=str(symbol), font=DEFAULT_FONT_STYLE, borderwidth=0, bg=OFF_WHITE, fg=LABEL_COLOR,command=lambda x=operators: self.append_operator(x));
            button.grid(row=i, column=4, sticky=tk.NSEW);
            i+=1


# display frame
    def create_display_frame(self):
        frame = tk.Frame(self.window,bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame;


# display button frame
    def create_buttons_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame;


# create clear button
    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0,command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)


# create square button
    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)


#sqrt a number
    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"));
        self.update_current_label();
        
    
    
#square a number
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"));
        self.update_current_label();


# create sqrt button
    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)



# create equal button
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)



#update total label
    def update_total_label(self):
        expressions=self.total_expression;
        for operators, symbols in self.operations.items():
            expressions = expressions.replace(operators, f' {symbols}');
        self.total_label.config(text=expressions);



#update total label
    def update_current_label(self):
        self.label.config(text=self.current_expression[:10]);


#add to expression
    def add_to_expression(self,value):
        self.current_expression += str(value);
        self.update_current_label();


#update operators
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()


#evaluate functionality
    def evaluate(self):
        self.total_expression+=self.current_expression;
        self.update_total_label();
        try:
            self.current_expression=str(eval(self.total_expression))
            self.total_expression=""
        except Exception as e:
            self.current_expression="Error"
            self.total_expression=""
        finally:
            self.update_current_label();



# Bind keyboard Keys with calculator keys
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<KP_Enter>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event,digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event,operator=key: self.append_operator(operator))
            


#clear functionality
    def clear(self):
        self.current_expression = "";
        self.total_expression = "";
        self.update_current_label();
        self.update_total_label();


# To render calc window on running
if __name__ == "__main__":
    calc = Calculator();
    calc.run();