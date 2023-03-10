"""

Title: 1st GUI 
Author: Parsh Gandhi AP CSP 219, Python Simplified(youtube)
Date: 1/25/23
Description: Makes a GUI to read and extract data from a user inputted pdf using python. 
Does this by using the tkinter module to make a window in which the app contents are
placed. The window has the logo of thee website and underneath it instructions on what 
to do. The user clicks on the button to browse their files and choose a pdf to read. It 
will then extract the contents of that pdf whether they be text or images using the pillow 
and PyPDF2 modules. Using tkinter the app displays the extracted contents onto the users
screen(in the tkinter window). Using buttons created the user can copy the current image, save
the image, save all the images, or scroll through the images. Finally theree is an exit button
at the top of the window to exit out of the app when done

"""

from tkinter import *
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from functions import display_logo, display_textbox, display_icon, display_images, extract_images, resize_image, copy_text, save_all, save_image

#global parameters, updating dynamically
all_content = []
all_images = []
img_idx = [0]
displayed_img = []

#initiallize a Tkinter root object
root = Tk()
root.title('Parsh Gandhi AP CSP 219 GUI')
root.geometry('+%d+%d'%(350,10)) #place GUI at x=350, y=10

#ARROW BUTTONS FUNCTIONALITY
#right arrow
def right_arrow(all_images, selected_img, what_text):
    #restrict button actions to the number of avialable images
    if img_idx[-1] < len(all_images) -1:
        #change to the following index
        new_idx = img_idx[-1] + 1
        img_idx.pop()
        img_idx.append(new_idx)
        #remove displayed image if exists
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        #create a new image in the new index & display it
        new_img = all_images[img_idx[-1]]
        selected_img = display_images(new_img)
        displayed_img.append(selected_img)
        #update the new index on the interface
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

#left arrow
def left_arrow(all_images, selected_img, what_text):
    #restrict button actions to indices greater than 1
    if img_idx[-1] >= 1:
        #change to the previous index
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)
        #remove displayed image if exists
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        #create a new image in the new index & display it
        new_img = all_images[img_idx[-1]]
        selected_img = display_images(new_img)
        displayed_img.append(selected_img)
        #update the new index on the interface
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

#header area - logo & browse button
header = Frame(root, width=800, height=175, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

#main content area - text and image extraction
main_content = Frame(root, width=800, height=250, bg="#20bebe")
main_content.grid(columnspan=3, rowspan=2, row=4)

def open_file():

    #clear global list of indices
    for i in img_idx:
        img_idx.pop()
    img_idx.append(0) #set global index to 0

    browse_text.set("loading...")

    #load a PDF file
    file = askopenfile(parent=root, mode='rb', filetypes=[("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfReader(file)
        #select a page
        page = read_pdf.pages[0]
        #extract text content from page
        page_content = page.extract_text()

        #SET A SPECIAL ENCODING OR REPLACE CHARACTERS
        #page_content = page_content.encode('cp1252')
        page_content = page_content.replace('\u2122', "'")

        #CLEARING GLOBAL VARIABLES ONCE A NEW PDF FILE IS SELECTED
        #clear the content of the previous PDF file
        if all_content:
            for i in all_content:
                all_content.pop()

        #clear the image list from the previous PDF file
        for i in range(0, len(all_images)):
            all_images.pop()

        #hide the displayed image from the previous PDF file and remove it
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()

        #BEGIN EXTRACTING
        #extract text
        all_content.append(page_content)
        #extract images
        images = extract_images(page)
        for img in images:
            all_images.append(img)

        #BEGIN DISPLAYING
        #display the first image that was detected
        selected_image = display_images(images[img_idx[-1]])
        displayed_img.append(selected_image)

        #display the text found on the page
        display_textbox(all_content, 4, 0, root)

        #reset the button text back to Browse
        browse_text.set("Browse")

        #BEGIN MENUES AND MENU WIDGETS
        #1.image menu on row 2
        img_menu = Frame(root, width=800, height=60)
        img_menu.grid(columnspan=3, rowspan=1, row=2)

        what_text = StringVar()
        what_img = Label(root, textvariable=what_text, font=("shanti", 10))
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))
        what_img.grid(row=2, column=1)

        #arrow buttons
        display_icon('arrow_l.png', 2, 0, E, lambda:left_arrow(all_images, selected_image, what_text))
        display_icon('arrow_r.png', 2, 2, W, lambda:right_arrow(all_images, selected_image, what_text))

        #2.save image menu on row 3
        save_img_menu = Frame(root, width=800, height=60, bg="#c8c8c8")
        save_img_menu.grid(columnspan=3, rowspan=1, row=3)

        #create action buttons
        copyText_btn = Button(root, text="copy text",command=lambda:copy_text(all_content, root), font=("shanti", 10), height=1, width=15)
        saveAll_btn = Button(root, text="save all images", command=lambda:save_all(all_images), font=("shanti", 10), height=1, width=15)
        save_btn = Button(root, text="save image", command=lambda:save_image(all_images[img_idx[-1]]), font=("shanti", 10), height=1, width=15)

        #place buttons on grid
        copyText_btn.grid(row=3,column=0)
        saveAll_btn.grid(row=3,column=1)
        save_btn.grid(row=3,column=2)

#BEGIN INITIAL APP COMPONENTS
display_logo('logo.png', 0, 0)

#instructions
instructions = Label(root, text="Select a PDF file", font=("Raleway", 10), bg="white")
instructions.grid(column=2, row=0, sticky=SE, padx=75, pady=5)

#browse button
browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway",12), bg="#20bebe", fg="white", height=1, width=15)
browse_text.set("Browse")
browse_btn.grid(column=2, row=1, sticky=NE, padx=50)

#exit button
exit_text = StringVar()
exit_btn = Button(root, textvariable=exit_text, command=root.destroy, font=("shanti", 10), height=1, width=15)
exit_text.set("Click to exit")
exit_btn.grid(column=2, row=0, sticky=NE, padx=50)

root.mainloop()
