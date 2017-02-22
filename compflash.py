"""

Yadu sharon
Fablab Trivandrum
Feb 2017

"""




import os
import sys
import subprocess
from subprocess import call

from threading import Thread
from Queue import Queue, Empty

from Tkinter import *
from Tkinter import Tk
import ttk
from tkFileDialog import askopenfilename
from tkFileDialog import *
root = Tk()


filetypes_allowed = [("C files","*.c"),('Hex files','*.hex')]
file_name = ""
filepath = ""
hex_file = ""
#fuse = StringVar()
fuse = False




def openfile():
    global filepath
    global file_name
    global file_extention
    global hex_file
    filepath = askopenfilename(filetypes=filetypes_allowed)
    file_path_entry.delete(0,END)
    file_path_entry.insert(0,filepath)

    file_name,file_extention=os.path.splitext(filepath)
    #print file_name
    if file_extention== ".hex" :
        hex_file = filepath
        button_compile.config(state=DISABLED)
    else:
        button_compile.config(state=NORMAL)

def Compile():
    cwd = os.getcwd()
    global hex_file
    file_bare = file_name

    fda = file_name.split('/')
    n = len(fda)
    file_name_only = fda[n-1]

    object_file = cwd+"/"+file_name_only+ ".o"
    elf_file = cwd+"/"+file_name_only+ '.elf'
    hex_file = file_bare+ '.hex'



    device_name = Chip_combobox.get()
    frequency = frequency_entry.get()
    device=device_name.lower()





    #make_object = "avr-gcc -g -Os -mmcu=" + device + " -c "+filepath
    make_object= "avr-gcc -g -Os -mmcu="+device+" -D_FCPU="+str(frequency)+" -c "+filepath
    make_link = "avr-gcc -g -mmcu="+device+" -o "+elf_file+" "+object_file
    make_hex = "avr-objcopy -j .text -j .data -O ihex "+elf_file+ " "+ hex_file

    out_error=""

    Terminal_window.config(state=NORMAL)

    process = subprocess.Popen(make_object, shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    #out = process.stdout.readline()
    #error = process.stderr.readline()
    out, error = process.communicate()
    #errors="".join(er)
    Terminal_window.insert(END,out)
    Terminal_window.insert(END,error)
    Terminal_window.see("end")
    out_error=out_error+out+error
    #process.wait()


    if out_error =="" :
        process = subprocess.Popen(make_link, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        out1, error1 = process.communicate()
        #errors="".join(er)
        Terminal_window.insert(END,out1)
        Terminal_window.insert(END,error1)
        Terminal_window.see("end")
        out_error=out_error+out1+error1
        #process.wait()

        if out_error== "":
            process = subprocess.Popen(make_hex, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

            out2, error2 = process.communicate()
            #errors="".join(er)
            Terminal_window.insert(END,out2)
            Terminal_window.insert(END,error2)
            Terminal_window.see("end")
            out_error=out_error+out2+error2
            process.wait()

            if out_error== "":
                Terminal_window.insert(END,"Compiled\n")
                dlt_obj = "rm -f "+object_file
                dlt_elf = "rm -f "+elf_file
                subprocess.Popen(dlt_obj, shell=True)
                subprocess.Popen(dlt_elf, shell=True)





    Terminal_window.config(state=DISABLED)


def program():
    part =""
    prgrmr= ""

    device_name = Chip_combobox.get()
    for i in range(0,len(chip_list)):
        if chip_list[i][0]== device_name:
            part=chip_list[i][1]

    prgrmr_name = programmer_combobox.get()
    for i in range(0,len(programmer_list)):
        if programmer_list[i][0]== prgrmr_name:
            prgrmr=programmer_list[i][1]

    Terminal_window.config(state=NORMAL)

    Terminal_window.insert(END,"Let's wait for few seconds!\n")
    Terminal_window.see("end")

    flash_chip = "avrdude -c "+prgrmr+" -p "+part+" -U flash:w:"+hex_file

    process = subprocess.Popen(flash_chip, shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    #process.wait()
    out, er = process.communicate()
    #er = process.stderr.readlines()
    #print er
    errors="".join(er)
    Terminal_window.insert(END,errors)
    Terminal_window.insert(END,out)
    Terminal_window.see("end")
    Terminal_window.config(state=DISABLED)



def fuse_deact():
    global default_color
    button_fuse.config(relief = RAISED,bg=default_color,activebackgroun=default_color)
    entry_lfuse.config(state=DISABLED)
    entry_hfuse.config(state=DISABLED)
    button_read_fuse.config(state=DISABLED)
    button_write_fuse.config(state=DISABLED)

def fuse_act():

    button_fuse.config(relief = SUNKEN,bg='#B6EBCE',activebackgroun='#B6EBCE')
    entry_lfuse.config(state=NORMAL)
    entry_hfuse.config(state=NORMAL)
    button_read_fuse.config(state=NORMAL)
    button_write_fuse.config(state=NORMAL)


def fuse_on_off():
    global fuse
    if fuse:
        fuse_deact()
    else:
        fuse_act()
    fuse = not fuse





def read_fuse():

    part =""
    prgrmr= ""

    device_name = Chip_combobox.get()
    for i in range(0,len(chip_list)):
        if chip_list[i][0]== device_name:
            part=chip_list[i][1]

    prgrmr_name = programmer_combobox.get()
    for i in range(0,len(programmer_list)):
        if programmer_list[i][0]== prgrmr_name:
            prgrmr=programmer_list[i][1]

    Terminal_window.config(state=NORMAL)
    Terminal_window.insert(END,"Let's wait for few seconds!\n")
    Terminal_window.see("end")


    fuse_chip = "avrdude -c "+prgrmr+" -p "+part+" -U hfuse:r:-:h -U lfuse:r:-:h"

    process = subprocess.Popen(fuse_chip, shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    #process.wait()
    stdout, er = process.communicate()
    errors="".join(er)
    Terminal_window.insert(END,errors)
    Terminal_window.see("end")
    Terminal_window.config(state=DISABLED)
    lh = stdout.split()
    lf=lh[1].split('x',2)
    hf=lh[0].split('x',2)
    low_fuse=lf[1]
    high_fuse=hf[1]
    entry_lfuse.delete(0,'end')
    entry_hfuse.delete(0,'end')
    entry_lfuse.insert(0,low_fuse)
    entry_hfuse.insert(0,high_fuse)

    Terminal_window.see("end")
    Terminal_window.config(state=DISABLED)


def write_fuse():

    part =""
    prgrmr= ""

    device_name = Chip_combobox.get()
    for i in range(0,len(chip_list)):
        if chip_list[i][0]== device_name:
            part=chip_list[i][1]

    prgrmr_name = programmer_combobox.get()
    for i in range(0,len(programmer_list)):
        if programmer_list[i][0]== prgrmr_name:
            prgrmr=programmer_list[i][1]

    low_value=entry_lfuse.get()
    high_value = entry_hfuse.get()
    lf_string=""
    hf_string=""
    if low_value != "":
        low_fuse= "0x"+low_value
        lf_string= " -U lfuse:w:"+low_fuse+":m"
    if high_value != "":
        high_fuse = "0x"+high_value
        hf_string = " -U hfuse:w:"+high_fuse+":m"

    Terminal_window.config(state=NORMAL)
    Terminal_window.insert(END,"Let's wait for few seconds!\n")
    Terminal_window.see("end")

    fuse_string = "avrdude -c "+prgrmr+" -p "+part+lf_string+hf_string
    process = subprocess.Popen(fuse_chip, shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    #process.wait()
    stdout, er = process.communicate()
    errors="".join(er)
    Terminal_window.insert(END,errors)
    Terminal_window.see("end")
    Terminal_window.config(state=DISABLED)

def key_comp():
    if button_compile['state']== NORMAL :
        Compile()

def key_flash():
    if button_flash['state'] == NORMAL :
        program()



chip_list= [
["ATtiny44","t44"],
["ATtiny45","t45"],
["ATmega8","m8"],
["ATmega16","m16"],
["ATmega168","m168"],
["ATmega168p","m168p"],
["ATmega32","m32"],
["ATmega328","m328"],
["ATmega328P","m328p"]]

programmer_list= [
["USB Tiny","usbtiny"],
["USBasp", "usbasp-clone"]
]

chips=[]
for i in range(0,len(chip_list)):
    chips.append(chip_list[i][0])
programmers=[]
for i in range(0,len(programmer_list)):
    programmers.append(programmer_list[i][0])













#root.geometry('700x500+400+250')
root.title('Compflash')




#open_image_full=PhotoImage(file="open.png")
#open_image= open_image_full.subsample(8,8)
button_open= Button(root, text= "Open",command=openfile)

button_compile= Button(root, text= "Compile",borderwidth=2,fg="white",bg="green",relief="solid",width=6, command=Compile)
button_flash= Button(root, text= "Flash",borderwidth=2,fg="white",bg="red",relief="solid",width=6, command=program)


#fuse_check_button = Checkbutton(root, text="Fuse", variable = fuse, onvalue="yes", offvalue="no")
#fuse= "no"
button_fuse=Button(root,text= "Fuse", relief = RAISED,command=fuse_on_off)
default_color= root.cget('bg')
button_fuse.config(activebackgroun=default_color)

entry_lfuse = Entry(root, width=4)
entry_hfuse = Entry(root,width=4)
button_read_fuse = Button(root, text = "Read", command=read_fuse)
button_write_fuse = Button(root, text = "Write", command=write_fuse)


file_path_entry = Entry(root,width=40)
file_path_entry.insert(0, 'File path')

chip = StringVar()
Chip_combobox = ttk.Combobox(root, textvariable=chip, values=chips, width=12)

programmer= StringVar()
programmer_combobox = ttk.Combobox(root, textvariable=programmer, values=programmers, width=12)

frequency_entry = Entry(root, width=10)

#terminal_scroll = Scrollbar(root, orient = VERTICAL)
Terminal_window=Text(root,state=NORMAL, width=70,height=15, wrap="word")
#terminal_scroll.config(command=Terminal_window.yview)
#Terminal_window.config(yscrollcommand=terminal_scroll.set)



label_filename= Label(root,text="File path")
label_chip= Label(root,text="Chip")
label_frequency= Label(root,text="Frequency")
label_programmer= Label(root,text="Programmer")
label_lfuse= Label(root,text="Low fuse")
label_hfuse= Label(root,text="High fuse")
label_key_comp= Label(root, text= "Compile : Ctrl+R")
label_key_flash= Label(root, text= "Flash : Ctrl+F")



fuse_deact()

###----------Keys press-----------###

root.bind('<Control-r>', lambda e: key_comp())

root.bind('<Control-f>', lambda e: key_flash())


#####-------------- grid------------

label_filename.grid(row=0,column=0,padx=5,pady=5,sticky=E)
file_path_entry.grid(row=0,column=1, columnspan=3,padx=5,pady=5,sticky=W)
button_open.grid(row=0,column=5,padx=5,pady=5)

label_chip.grid(row=1,column=0,pady=5,sticky=E)
Chip_combobox.grid(row=1,column=1, pady=5,padx=5, sticky=W)

label_frequency.grid(row=1,column=2,pady=5, sticky=E)
frequency_entry.grid(row=1,column=3,sticky=W)
button_compile.grid(row=1,column=5,padx=5,pady=5)

label_programmer.grid(row=2, column=0,sticky=E,padx=5,pady=5)
programmer_combobox.grid(row=2, column=1,padx=5,pady=5, sticky=W)

button_flash.grid(row=2, column=5, padx=5,pady=5,sticky=E)

#fuse_check_button.grid(row=3,column = 0,padx=5,pady=5)
button_fuse.grid(row=3, column=0, pady=5,)
label_lfuse.grid(row=3, column=1,pady=5, padx=10, sticky=W)
entry_lfuse.grid(row=3, column=1,pady=5, padx=25, sticky=E)
label_hfuse.grid(row=3, column=2,pady=5, padx=5, sticky=W)
entry_hfuse.grid(row=3, column=2,pady=5, padx=0, columnspan=2)
button_read_fuse.grid(row = 3, column=3, pady = 5,padx=2, sticky=E)
button_write_fuse.grid(row = 3, column=5, pady = 5,padx=2, sticky=W)

Terminal_window.grid(row=4, column=0, columnspan=6, padx=5,pady=5)
Terminal_window.update_idletasks()
Terminal_window.config(state=DISABLED)

label_key_comp.grid(row=5, column = 0, padx=7, columnspan=2, sticky = W)
label_key_flash.grid(row=5, column = 1, padx=7, columnspan=2)




root.mainloop()
