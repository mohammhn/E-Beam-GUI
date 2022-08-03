# Python program to create a simple GUI
# calculator using Tkinter
 
# import everything from tkinter module
from tkinter import *
from tkinter import ttk

import serial

 
# globally declare the expression variable
expression = ""
 
 
# Function to update expression
# in the text entry box
def press(button, num):
    # point out the global expression variable
    global expression
 
    # concatenation of string
    expression = expression + str(num)
 
    # update the expression by using set method
    equation.set(expression)
    
    
 
 
# Function to evaluate the final expression
def equalpress():
    # Try and except statement is used
    # for handling the errors like zero
    # division error etc.
 
    # Put that code inside the try block
    # which may generate the error
    try:
 
        global expression
 
        # eval function evaluate the expression
        # and str function convert the result
        # into string
        total = str(eval(expression))
 
        equation.set(total)
 
        # initialize the expression variable
        # by empty string
        expression = ""
 
    # if error is generate then handle
    # by the except block
    except:
 
        equation.set(" error ")
        expression = ""
 
 
# Function to clear the contents
# of text entry box
def clear():
    global expression
    expression = ""
    equation.set("")


class pixel:
    # Class attribute
    # baseKey = "0"
    # def __name__(self):
    #     if not self.name:
    #         self.baseKey
    #     else:
    #         self.name

    def __init__(self, row, col, pin, row_offset=0, col_offset=0, row_stride=1, col_stride=1):
        self.row = row
        self.col = col
        self.name = str("r"+str(row)+"_c"+str(col))
        # self.button = Button(gui, text=self.name, fg='white', bg='black', activeforeground='blue', activebackground='light blue', command=lambda:self.command(), height=1, width=7, relief=FLAT)
        self.button = Button(loginFrame, fg='white', bg='black', activeforeground='blue', activebackground='light blue', command=lambda:self.command(), relief=FLAT)
        
        self.button.grid(row=self.row * row_stride + row_offset, column=self.col * col_stride + col_offset, sticky='nesw', rowspan=row_stride, columnspan=col_stride)
        # self.button.grid(row=self.row * row_stride + row_offset, column=self.col * col_stride + col_offset, sticky='nesw')
        # self.button.grid(row=self.row + row_offset, column=self.col + col_offset, rowspan=3, columnspan=3)

        
        # value in mA
        self.value = 0.0
        # value as ratio between 0 and 1
        self.value_ratio = 0.0
        
        # value of pin in board pinout, from 0 to max_val
        self.pin = pin
        
        
    
    def command(self):
        print("pressed button at row:{} col:{}".format(self.row, self.col))
        
        if self.button.cget('bg') != 'light blue':   # Check current color
            self.button.config(fg = 'blue', bg='light blue', activebackground='blue', activeforeground='light blue', )
        # if self.button.cget('bg') != 'blue':   # Check current color
            # self.button.config(fg = 'white', bg='blue', activebackground='light blue', activeforeground='black')
        
        
        
        
        # if self.button.cget('bg') == 'light grey':   # Check current color
            # self.button.config(fg = 'light grey', bg='black', activebackground='light grey', activeforeground='black')
        # elif self.button.cget('bg') == 'black':   # Check current color
        #     self.button.config(bg = 'light grey', fg='black', activeforeground='light grey', activebackground='black')
        
        button_prev = pixel_pos.cget('text')
        if button_prev in pixels and pixels[button_prev].button.cget('bg') == 'light blue':
            # pixels[button_prev].button.config(bg = 'light grey', fg='red', activeforeground='light grey', activebackground='black')
            # bg_intVal = (pixels[button_prev].value / 30.0) * 255
            
            # remove with modified digipot code
            bg_intVal = (pixels[button_prev].value / 30.0) * globals()['voltage_ratio'] * 255
            fg_intVal = 255 - bg_intVal
            bg_hexVal = hex(int(bg_intVal))
            fg_intVal = hex(int(fg_intVal))
            # print(hexVal)
            bg_color = '#' + str(bg_hexVal[2:]) + str(bg_hexVal[2:]) + str(bg_hexVal[2:])
            fg_color = '#' + str(fg_intVal[2:]) + str(fg_intVal[2:]) + str(fg_intVal[2:])
            
            
            # print(color)
            pixels[button_prev].button.config(bg = bg_color, fg=fg_color, activeforeground='blue', activebackground='light blue')
            
            
                
        pixel_pos.config(text = self.name)     
        pixel_pin.config(text = self.pin)
        pixel_cur_val.config(text = self.value)
        input_var = ""
        
    
    def read(self):
        return
    
    def write(self):
        return
    
    def reset(self):
        return
        
def createGrid():
    
    rows = row_var.get()
    cols = col_var.get()
    
    if int(rows) > 0:
        if int(rows) < max_pixels:
            rows = int(rows)
        else:
            rows = max_pixels
    else:
        return
    
    if int(cols) > 0:
        if int(cols) < max_pixels / rows:
            cols = int(cols)
        else:
            cols = max_pixels // rows
    else:
        return
            
    # rows = int(rows_input)
    # cols = int(cols_input)
    global pixels
    pixels = {}
    
    # Hashtable mapping pixel pin value to pixel key for pixel dictionary
    global pinout
    pinout = {}
    
    for i in range(rows):
        for j in range(cols):
            key = str("r"+str(i)+"_c"+str(j))
            pixels[key] = pixel(i, j, i * cols + j, row_offset=0, col_offset=3, row_stride=2, col_stride=2)
            pinout[str(i * cols + j)] = key
            
    # print(pinout)
            
    


def read_cmd():
    # send input_val to pin corresponding to current pixel
    #FIX THIS TO WORK!!!
    pin_text = pixel_pin.cget('text')
    if type(pin_text) != int:
        return
    else:
        pin = int(pin_text)
    
    # inputString = "read_mA; {pin}\n".format(pin)
    inputString = "read_mA;\n"
    ser.write(inputString.encode('utf-8'))
    
    rv = ser.readline().decode('utf-8').strip()
        
    read_dictionary = dict(subString.split(":") for subString in rv.replace('mA', '').split(","))
    print(read_dictionary)
    # print(pin)
    
    value = float(read_dictionary[str(pin)])
    # pixel_cur_val.config(text=str(value))
    
    pixel_cur_val.config(text=str(value * (1 / globals()['voltage_ratio'])))
    
    print("pin:{}, val:{}".format(pin, value))
    
    for pin_i, value_i in read_dictionary.items():
        if int(pin_i) >= len(pinout):
            break
        # print(pin_i)
        # print(value_i)
        # print(pinout[pin_i])
        # print(pixel[pinout[pin_i]])
        # pixels[pinout[pin_i]].value = value_i
        
        pixels[pinout[pin_i]].value = float(value_i) * (1 / globals()['voltage_ratio'])
        
        # pixel_cur_val.config(text=str(float(value)))
    
    # pixel_cur_val.config(text=str(float(rv)))
    
    updateGrid()
    
    return
    
def write_cmd():
    pin_text = pixel_pin.cget('text')
    if type(pin_text) != int:
        return
    else:
        pin = int(pin_text)
    # print(pin)
    # value = float(globals()['input_var'].get())
    
    # Remove for DIGIPOT update
    value = float(globals()['input_var'].get()) * globals()['voltage_ratio']
    # print(value)
    # value = float(input_var)
    value2 = value * globals()['voltage_ratio']
    inputString = "write_mA; {}:{}\n".format(pin, value2)
    
    # inputString = "write_mA; {}:{}\n".format(pin, value)
    # print(inputString)
    ser.write(inputString.encode('utf-8'))
    
    pixel_cur_val.config(text=str(value))
    # pixel_cur_val.config(text=str(value * (1 / globals()['voltage_ratio'])))
    
    pixels[pinout[str(pin)]].value = value
    
    # print("pin:{}, val:{}".format(pin, value))
    
    updateGrid()
    
    return

def reset_cmd():
    pin_text = pixel_pin.cget('text')
    if type(pin_text) != int:
        return
    else:
        pin = int(pin_text)
        
    value = 0.0
    # print(value)
    # value = float(input_var)
    # value2 = value * globals()['voltage_ratio']
    # inputString = "write_mA; {}:{}\n".format(pin, value)
    
    inputString = "write_mA; "
    for pin, key in pinout.items():
        pixels[key].value = value
        inputString += "{}:{}".format(pin, pixels[key].value)
        if int(pin) < len(pinout) - 1:
            inputString += ','
    inputString += '\n'
    # print(inputString)
    
    
    # inputString = "write_mA; {}:{}\n".format(pin, value)
    # print(inputString)
    ser.write(inputString.encode('utf-8'))
    
    pixel_cur_val.config(text=str(value))
    # pixel_cur_val.config(text=str(value * (1 / globals()['voltage_ratio'])))
    
    pixels[pinout[str(pin)]].value = value
    
    # print("pin:{}, val:{}".format(pin, value))
    
    updateGrid()
    
    return

def read_volt(): 
    voltage_local = globals()['voltage']
    volt_coarse = voltage_local // 1
    volt_fine = voltage_local % 1
    
    globals()['input_coarse'].set(str(volt_coarse))
    globals()['input_fine'].set(str(volt_fine))
    # globals()['voltage_ratio'].set()
    
    updateGrid()
    
def write_volt():
    max_volts = globals()['max_voltage']
    
    volt_coarse = int(globals()['input_coarse'].get())
    volt_fine = int(globals()['input_fine'].get())
        
    volt = float(str(int(volt_coarse)) + '.' + str(int(volt_fine)))
    
    if volt > max_volts:
        volt = max_volts
        globals()['input_coarse'].set(str(max_volts // 1))
        globals()['input_fine'].set(str(int(max_volts % 1)))
    
    print(volt)
    
    globals()['voltage'] = volt
    
    globals()['voltage_ratio'] = volt / max_volts
    
    inputString = "write_mA; "
    for pin, key in pinout.items():
        newVal = globals()['voltage_ratio'] * pixels[key].value
        inputString += "{}:{}".format(pin, newVal)
        if int(pin) < len(pinout) - 1:
            inputString += ','
    inputString += '\n'
    print(inputString)
    
    ser.write(inputString.encode('utf-8'))
    
    updateGrid()
    
        
    # write_cmd()
    
    
def reset_volt():
    max_volts = globals()['max_voltage']
    # volt = max_volts
    
    volt_coarse = globals()['max_voltage'] // 1
    globals()['input_coarse'].set(str(volt_coarse))

    volt_fine = globals()['max_voltage'] % 1
    globals()['input_fine'].set(str(volt_fine))
        
    # volt = float(str(int(volt_coarse)) + '.' + str(int(volt_fine)))
    
    globals()['voltage'] = max_volts
    globals()['voltage_ratio'] = 1.0
    
    inputString = "write_mA; "
    for pin, key in pinout.items():
        newVal = globals()['voltage_ratio'] * pixels[key].value
        inputString += "{}:{}".format(pin, newVal)
        if int(pin) < len(pinout) - 1:
            inputString += ','
    inputString += '\n'
    print(inputString)
    
    ser.write(inputString.encode('utf-8'))
    
    updateGrid()

def updateGrid():
    for pin, key in pinout.items():
        bg_intVal = (pixels[key].value / 30.0) * globals()['voltage_ratio'] * 255 
        fg_intVal = 255 - bg_intVal
        bg_hexVal = hex(int(bg_intVal))
        fg_intVal = hex(int(fg_intVal))
        # print(hexVal)
        bg_color = '#' + str(bg_hexVal[2:]) + str(bg_hexVal[2:]) + str(bg_hexVal[2:])
        fg_color = '#' + str(fg_intVal[2:]) + str(fg_intVal[2:]) + str(fg_intVal[2:])
        
        # print(color)
        pixels[key].button.config(bg = bg_color, fg=fg_color, activeforeground='blue', activebackground='light blue')
    

def writeSerial(input):
    return

def readSerial(input):
    rv = ""
    return rv


 
# Driver code
if __name__ == "__main__":
    
    ser = serial.Serial('COM4', baudrate=9600, timeout=1)
    # ser.reset_input_buffer()
    input_Ser = ""
    
    while input_Ser == "":
        input_Ser = ser.readline().decode('utf-8').strip()
    
    print(input_Ser)
    
    if input_Ser == "RESET":
        ser.write("\n".encode('utf-8'))
        print("connection successful!")
        
    # print(input)
    
    # print("testing!")
    
    max_pixels = 24
    max_voltage = 3.3
    voltage = 3.3
    voltage_ratio = voltage / max_voltage
    
    
    # create a GUI window
    gui = Tk()
 
    # set the background colour of GUI window
    gui.configure(background="light blue")
 
    # set the title of GUI window
    gui.title("Control GUI")
 
    # set the configuration of GUI window
    gui.geometry("500x500")
    
    # apply to root is essential
    gui.rowconfigure(0, weight = 1)
    gui.columnconfigure(0, weight = 1)
    
    
    loginFrame = Frame(gui, bg="light blue")
    loginFrame.grid(row=0, column=0,sticky = NSEW)
    # now apply to loginFrame
    loginFrame.rowconfigure(0, weight = 1)
    loginFrame.rowconfigure(1, weight = 1)
    loginFrame.rowconfigure(2, weight = 1)
    loginFrame.rowconfigure(3, weight = 1)
    loginFrame.rowconfigure(4, weight = 1)
    loginFrame.rowconfigure(5, weight = 1)
    loginFrame.rowconfigure(6, weight = 1)
    loginFrame.rowconfigure(7, weight = 1)
    loginFrame.rowconfigure(8, weight = 1)
    loginFrame.rowconfigure(9, weight = 1)
    loginFrame.rowconfigure(10, weight = 1)
    loginFrame.rowconfigure(11, weight = 1)
    loginFrame.rowconfigure(12, weight = 1)
    loginFrame.rowconfigure(13, weight = 1)
    loginFrame.columnconfigure(0, weight = 1)
    loginFrame.columnconfigure(1, weight = 1)
    loginFrame.columnconfigure(2, weight = 1)
    loginFrame.columnconfigure(3, weight = 1)
    loginFrame.columnconfigure(4, weight = 1)
    loginFrame.columnconfigure(5, weight = 1)
    loginFrame.columnconfigure(6, weight = 1)
    loginFrame.columnconfigure(7, weight = 1)
    loginFrame.columnconfigure(8, weight = 1)
    loginFrame.columnconfigure(9, weight = 1)
    # loginFrame.columnconfigure(10, weight = 1)
    # loginFrame.columnconfigure(11, weight = 1)
    # loginFrame.columnconfigure(12, weight = 1)
    # loginFrame.columnconfigure(13, weight = 1)
    # loginFrame.columnconfigure(14, weight = 1)
 
    # # StringVar() is the variable class
    # # we create an instance of this class
    # equation = StringVar()
    
    # declaring string variable
    # for storing name and password
    row_var=StringVar()
    col_var=StringVar()
    input_var=StringVar()
    
    input_coarse=StringVar()
    input_fine=StringVar()
    
    
    
    # # create the text entry box for
    # # showing the expression .
    # expression_field = Entry(gui, textvariable=equation)
 
    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    # expression_field.grid(columnspan=5, ipadx=10)
    # expression_field.grid(ipadx=10)
    
    
    # the label for user_name 
    rows_label = Label(loginFrame, text = "Rows", bg='light blue')
        
    # the label for user_password  
    cols_label = Label(loginFrame, text = "Columns", bg='light blue') 
    
    rows_input = Entry(loginFrame, textvariable = row_var, font=('calibre',10,'normal'), width=5)
        
    cols_input = Entry(loginFrame, textvariable = col_var, font=('calibre',10,'normal'), width=5)
        
    # submit_button = Button(gui, text = "Create").place(x = 40, y = 130)
    
    submit_button = Button(loginFrame, text="CREATE / RESET", fg='black', bg='light grey', activeforeground='light grey', activebackground='black', command=lambda:createGrid(), relief=FLAT)
    
    # Separator object
    # separator = ttk.Separator(gui, orient='horizontal')
    # separator.place(relx=0.47, rely=0, relwidth=0.2, relheight=1)
    
    

    # placing the label and entry in
    # the required position using grid
    # method
    rows_label.grid(row=0,column=0, sticky='nesw')
    rows_input.grid(row=0,column=1, sticky='nesw')
    cols_label.grid(row=1,column=0, sticky='nesw')
    cols_input.grid(row=1,column=1, sticky='nesw')
    submit_button.grid(row=2,column=1, sticky='nesw')
    
    seperator_label_0 = Label(loginFrame, text = " ", bg='light blue').grid(row=0, column=2, sticky='nesw')
    seperator_label_1 = Label(loginFrame, text = " ", bg='light blue').grid(row=1, column=2,sticky='nesw')
    seperator_label_2 = Label(loginFrame, text = " ", bg='light blue').grid(row=2, column=2, sticky='nesw')
    
    seperator_label_3 = Label(loginFrame, text = " ", bg='light blue').grid(row=3, column=0, sticky='nesw')
    seperator_label_4 = Label(loginFrame, text = " ", bg='light blue').grid(row=3, column=1, sticky='nesw')
    seperator_label_5 = Label(loginFrame, text = " ", bg='light blue').grid(row=3, column=2, sticky='nesw')
    
    
    pixel_pos_label = Label(loginFrame, text = "Pixel (Row,Col):", bg='light blue')
    pixel_pos = Label(loginFrame, text = "  ", bg='light blue')
    
    pixel_pin_label = Label(loginFrame, text = "Pin:", bg='light blue')
    pixel_pin = Label(loginFrame, text = "", bg='light blue')
    
    pixel_cur_val_label = Label(loginFrame, text = "Current Value:", bg='light blue')
    pixel_cur_val = Label(loginFrame, text = "0", bg='light blue')
    pixel_cur_val_units = Label(loginFrame, text = "mA", bg='light blue')
    
    pixel_input_label = Label(loginFrame, text = "Input:", bg='light blue')
    pixel_input = Entry(loginFrame, textvariable = input_var, font=('calibre',10,'normal'), width=5)  
    pixel_input_units = Label(loginFrame, text = "mA", bg='light blue')
    
    read_button = Button(loginFrame, text="READ", fg='black', bg='green', activeforeground='light grey', activebackground='black', command=lambda:read_cmd(), relief=FLAT)
    write_button = Button(loginFrame, text="WRITE", fg='black', bg='red', activeforeground='light grey', activebackground='black', command=lambda:write_cmd(), relief=FLAT)
    reset_button = Button(loginFrame, text="RESET", fg='black', bg='light grey', activeforeground='light grey', activebackground='black', command=lambda:reset_cmd(), relief=FLAT)
    
    
    pixel_pos_label.grid(row=4,column=0, sticky='nesw')
    pixel_pos.grid(row=4,column=1, sticky='nesw')
    pixel_pin_label.grid(row=5,column=0, sticky='nesw')
    pixel_pin.grid(row=5,column=1, sticky='nesw')
    
    pixel_cur_val_label.grid(row=6,column=0, sticky='nesw')
    pixel_cur_val.grid(row=6,column=1, sticky='nesw')
    pixel_cur_val_units.grid(row=6,column=2, sticky='nesw')
    
    pixel_input_label.grid(row=7,column=0, sticky='nesw')
    pixel_input.grid(row=7,column=1, sticky='nesw')
    pixel_input_units.grid(row=7,column=2, sticky='nesw')
    
    read_button.grid(row=8,column=0, sticky='nesw')
    write_button.grid(row=8,column=1, sticky='nesw')
    reset_button.grid(row=8,column=2, sticky='nesw')
    
    seperator_label_6 = Label(loginFrame, text = " ", bg='light blue').grid(row=9, column=0, sticky='nesw')
    seperator_label_7 = Label(loginFrame, text = " ", bg='light blue').grid(row=9, column=1, sticky='nesw')
    seperator_label_8 = Label(loginFrame, text = " ", bg='light blue').grid(row=9, column=2, sticky='nesw')
    seperator_label_9 = Label(loginFrame, text = " ", bg='light blue').grid(row=9, column=3, sticky='nesw')
    # seperator_label_10 = Label(gui, text = " ", bg='light blue').grid(row=8, column=3)
    
    digipot_title = Label(loginFrame, text = "Voltage Control", bg='light blue')
    digipot_coarse_label = Label(loginFrame, text = "coarse", bg='light blue')
    digipot_fine_label = Label(loginFrame, text = "fine", bg='light blue')
    digipot_coarse_input = Entry(loginFrame, textvariable = input_coarse, font=('calibre',10,'normal'), width=6)
    digipot_fine_input = Entry(loginFrame, textvariable = input_fine, font=('calibre',10,'normal'), width=6)
    digipot_coarse_units = Label(loginFrame, text = "V", bg='light blue')
    digipot_fine_units = Label(loginFrame, text = "mV", bg='light blue')
    
    read_button = Button(loginFrame, text="READ", fg='black', bg='green', activeforeground='light grey', activebackground='black', command=lambda:read_volt(), relief=FLAT)
    write_button = Button(loginFrame, text="WRITE", fg='black', bg='red', activeforeground='light grey', activebackground='black', command=lambda:write_volt(), relief=FLAT)
    reset_button = Button(loginFrame, text="RESET", fg='black', bg='light grey', activeforeground='light grey', activebackground='black', command=lambda:reset_volt(), relief=FLAT)
    
    digipot_title.grid(row=10,column=1, sticky='nesw')
    
    digipot_coarse_label.grid(row=11,column=0, sticky='nesw')
    digipot_coarse_input.grid(row=11,column=1, sticky='nesw')
    digipot_coarse_units.grid(row=11,column=2, sticky='nesw')
    
    digipot_fine_label.grid(row=12,column=0, sticky='nesw')
    digipot_fine_input.grid(row=12,column=1, sticky='nesw')
    digipot_fine_units.grid(row=12,column=2, sticky='nesw')
    
    read_button.grid(row=13,column=0, sticky='nesw')
    write_button.grid(row=13,column=1, sticky='nesw')
    reset_button.grid(row=13,column=2, sticky='nesw')
    
    # ttk.Separator(
    # master=gui,
    # orient=HORIZONTAL,
    # # style='blue.TSeparator',
    # class_= ttk.Separator,
    # takefocus= 1,
    # cursor='plus'    
    # ).grid(row=3, column=1)
    
    # ).grid(row=3, column=1, ipadx=200, pady=10)
    
    # Number of rows and cols for grid
    # rows = 3
    # cols = 3
    # pixels = {}
    
    # for i in range(rows):
    #     for j in range(cols):
    #         key = str("r"+str(i)+"_c"+str(j))
    #         pixels[key] = pixel(i, j)
    
    # for i in range(rows):
    #     for j in range(cols):
    #         key = str("r"+str(i)+"_c"+str(j))
    #         # pixels[key] = "Button(gui, text=key, fg='black', bg='light grey', activeforeground='light grey', activebackground='black', command=lambda: press(key, 1), height=1, width=7, relief=FLAT)"
    #         pixels[key] = Button(gui, text=key, fg='black', bg='light grey', activeforeground='light grey', activebackground='black', command=lambda: press(r, 1), height=1, width=7, relief=FLAT)
    #         # pixels[key] = Button(gui, text=key, fg='black', bg='red', command=lambda: press(i,j), height=1, width=7)
    # for key,value in pixels.items():
    #     exec(f'{key}={value}')
        
    #     gridCommand = "{}.grid(row={}, column={})".format(key, key[1], key[4])
    #     exec(gridCommand)
        
        
        
        # key.grid(row=key[1], column=key[4])
    
        
    
    
    # start the GUI
    gui.mainloop()