from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io

root = Tk()
root.geometry("600x700")
root.title("PokéxFinder")
root['bg'] = "#b7c9e2"
root.resizable(0, 0)

# button hover effects
def on_hover(event):
    event.widget.configure(bg="#d3d3d3")
    
def on_default(event):
    event.widget.configure(bg="#fff")
 
def get_pokemon(id_or_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{id_or_name}/' # url for api using id to iterate
    response = requests.get(url)

    if response.status_code == 200: # if status code is 200 then the request was successful
        pokemon_data = response.json()
            
        return pokemon_data

def get_pokemon_image(id):
    pokemon_data_id = get_pokemon(id) # calls get_pokemon to get pokemon data
    
    sprite_url = pokemon_data_id['sprites']['front_default'] # url for sprite
    sprite_response = requests.get(sprite_url)

    if sprite_response.status_code == 200: # if status code is 200 then the request was successful
        sprite_data = sprite_response.content
        image = Image.open(io.BytesIO(sprite_data))
        return image

def get_type_info(type_name):
    url = f'https://pokeapi.co/api/v2/type/{type_name}/' # url for api using id to iterate
    response = requests.get(url)

    if response.status_code == 200:
        type_info = response.json()
        return type_info

def get_damage_relations(type_info):
    # stores the type's weakness and resistances
    weakness = [x['name'] for x in type_info['damage_relations']['double_damage_from']] 
    resistantances = [x['name'] for x in type_info['damage_relations']['half_damage_from'] + type_info['damage_relations']['no_damage_from']]
    
    return weakness, resistantances # returns two lists

def filter_pokemon(error_label_id=None, error_label_name=None):
    search_text = search_bar.get().lower()
    
    # clear error labels
    error_label_id.place_forget()
    error_label_name.place_forget()
    
    if search_text.isnumeric(): # if the input is a number
        pokemon_id = int(search_text)

        try:
            pokemon_details(pokemon_id)
        except:
            error_label_id.place(x=280, y=35)     

    else:
        try: # if entry matches a pokemon
            pokemon = get_pokemon(search_text)
            pokemon_details(pokemon['id'])
        except:
            error_label_name.place(x=280, y=35)

def create_temp_frame(): # creates a temporary frame to use 
    temp_frame = Frame(root, bg="#314663")
    temp_frame.place(x=0, y=0, width=600, height=700)
    return temp_frame

def next_frame():
    global current_frame

    current_frame_index = main_frame_list.index(current_frame)
    if current_frame_index < len(main_frame_list) - 1: # if not the last frame
        page_number.config(text=f"{current_frame_index + 2}/{len(main_frame_list)}")
        current_frame.place_forget()
        current_frame = main_frame_list[current_frame_index + 1] # get the next frame
        current_frame.place(x=22, y=100) # place the new frame

def previous_frame():
    global current_frame

    current_frame_index = main_frame_list.index(current_frame)
    if current_frame_index > 0: # if not the first frame
        page_number.config(text=f"{current_frame_index}/{len(main_frame_list)}")
        current_frame.place_forget()
        current_frame = main_frame_list[current_frame_index - 1] # get the previous frame
        current_frame.place(x=22, y=100)

def update_main_frames(frames, rows, columns):
    global main_frame_list
    
    for i in range(frames): # how many frames
        main_frame = Frame(root, background="#b7c9e2") 
        main_frame_list.append(main_frame) # appends all the frames to switch between
        
        for r in range(rows): # how many rows in the grid
            for c in range(columns): # how many columns in the grid
                pokemon_id = 1 + c + r * 3 + i * 9 # starts the loop at 1 and ends at 152

                if pokemon_id < 152:
                    pokemon = get_pokemon(pokemon_id) # gets the pokemon from the the current pokemon_id number
                    pokemon_image = get_pokemon_image(pokemon_id) # gets the pokemon image from the current pokemon_id number
                    pokemon_image = ImageTk.PhotoImage(pokemon_image) # converts the image to a photo
                    
                    pokemon_frame = Frame(main_frame, width=165, height=170) # creates a frame showcasing each pokemon
                    pokemon_frame.grid(row=r, column=c, padx=10, pady=10, sticky=N)

                    image_label = Button(pokemon_frame, image=pokemon_image, width=165, # showcases the image in a button
                                        height=90, bd=0, background="#fff",
                                        command=lambda id=pokemon['id']:pokemon_details(id)) # using the id of the pokemon
                    
                    image_label.bind('<Enter>', on_hover)
                    image_label.bind('<Leave>', on_default)
                    
                    image_label.image = pokemon_image
                    image_label.place(x=0, y=0)

                    # shows the pokemon id and name and keeping the id have 3 digits
                    if pokemon_id < 10: 
                        Label(pokemon_frame, text=f"#000{pokemon['id']}",
                              font=("Lexend 8"), fg="#bfbfbf").place(x=13, y=92)
                    else:
                        if pokemon_id < 100:
                            if pokemon_id < 1000:
                                Label(pokemon_frame, text=f"#00{pokemon['id']}",
                                    font=("Lexend 8"), fg="#bfbfbf").place(x=13, y=92)
                            else:
                                Label(pokemon_frame, text=f"#0{pokemon['id']}",
                                    font=("Lexend 8"), fg="#bfbfbf").place(x=13, y=92)
                        else:
                            Label(pokemon_frame, text=f"#{pokemon['id']}",
                                  font=("Lexend 8"), fg="#bfbfbf").place(x=13, y=92)

                    Label(pokemon_frame, text=f"{pokemon['name'].title()}",
                          font=("Lexend 12")).place(x=13, y=112)
                    
                    # shows the pokemon types and saves it in a list to frame them
                    type_images = []
                    for t in pokemon['types']:
                        img_path = f"pokemon types/{t['type']['name']}.png" # gets the path of the image by name
                        img = Image.open(img_path)
                        img = img.resize((62, 15))
                        img = ImageTk.PhotoImage(img)
                        type_images.append(img)
                        
                    for index, img in enumerate(type_images): # places the images in the frame 
                        Label(pokemon_frame, image=img).place(x=13 + index * 70, y=141)

                    pokemon_frame.type_images = type_images

def pokemon_details(pokemon_id):
    # getting pokemon data and creating a frame
    pokemon = get_pokemon(pokemon_id)
    pokemon_image = get_pokemon_image(pokemon_id)
    temp_frame = create_temp_frame()
    
    title = Label(temp_frame, text=f"{pokemon['name'].title()}",
                  font=("Lexend 22 bold"), fg="#fff", bg="#314663")
    
    # using the id of the pokemon and configuring the title
    if pokemon_id < 10:
        title.config(text = f"{pokemon['name'].title()} #000{pokemon['id']}")
    else:
        if pokemon_id < 100:
            if pokemon_id < 1000:
                title.config(text = f"{pokemon['name'].title()} #00{pokemon['id']}")
            else:
                title.config(text = f"{pokemon['name'].title()} #0{pokemon['id']}")
        else:
            title.config(text = f"{pokemon['name'].title()} #{pokemon['id']}")
    
    title.pack(pady=5)
    
    # adding the image to the frame
    pokemon_image = pokemon_image.resize((300, 300))
    photo_image = ImageTk.PhotoImage(pokemon_image)
    image_label = Label(temp_frame, image=photo_image, bg="#fff", width=600, height=300)
    image_label.photo = photo_image
    image_label.place(x=0, y=50)
    
    size_frame = Frame(temp_frame, bg="#f0f0f0")
    size_frame.place(x=10, y=370, width=300, height=310)
    
    # showing the pokemon height, weight and abilities
    Label(size_frame, text="Height", font=("Lexend 12 bold"), bg="#f0f0f0").place(x=18, y=10)
    Label(size_frame, text=f"{pokemon['height'] * 10}cm", font=("Lexend 12"), bg="#f0f0f0").place(x=18, y=40)
    
    Label(size_frame, text="Weight", font=("Lexend 12 bold"), bg="#f0f0f0").place(x=18, y=80)
    Label(size_frame, text=f"{pokemon['weight'] / 10}kg", font=("Lexend 12"), bg="#f0f0f0").place(x=18, y=110)
    
    abilities_list = pokemon.get('abilities', []) # getting the abilities of the pokemon and saves it in a list
    
    Label(size_frame, text="Ability", font=("Lexend 12 bold"), bg="#f0f0f0").place(x=150, y=10)

    ability = abilities_list[0].get('ability', {}).get('name') # getting the name of the first ability
    Label(size_frame, text=f"{ability.title()}", font=("Lexend 12"), bg="#f0f0f0").place(x=150, y=40)
    
    Label(size_frame, text="Hidden Ability", font=("Lexend 12 bold"), bg="#f0f0f0").place(x=150, y=80)
    
    # shows the name of the hidden ability and if there is none it shows none
    hidden_ability = abilities_list[1].get('ability', {}).get('name') if len(abilities_list) > 1 else None 

    if hidden_ability:
        Label(size_frame, text=f"{hidden_ability.title()}", font=("Lexend 12"), bg="#f0f0f0").place(x=150, y=110)
    else:
        Label(size_frame, text="None", font=("Lexend 12"), bg="#f0f0f0").place(x=150, y=110)
    
    stats_frame = Frame(temp_frame, bg="#f0f0f0")
    stats_frame.place(x=20, y=530, width=270, height=132)

    # saves the stats of the pokemon
    all_stats = ["Hp", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]
    
    stats = pokemon.get('stats', []) # gets the stats of the pokemon
    base_stats = [stat['base_stat'] for stat in stats] # saves the base stats in a list
    for index, label in enumerate(all_stats): # creates a label for each stat
        Label(stats_frame, text=label, font=("Lexend 10"), bg="#f0f0f0").grid(row=index, column=0, sticky=W, padx=7)
        Label(stats_frame, text=base_stats[index], font=("Lexend 10"), bg="#f0f0f0").grid(row=index, column=1, sticky=E, padx=3)

        # creates a progress bar for each stat and changes the value depending on the base stat with a max of 255
        bar = ttk.Progressbar(stats_frame, length=135, orient=HORIZONTAL, value=base_stats[index] / 2.55) 
        bar.grid(row=index, column=2, sticky=W)
    
    type_frame = Frame(temp_frame, bg="#f0f0f0")
    type_frame.place(x=300, y=370, width=290, height=310)
    
    # shows the pokemon types
    Label(temp_frame, text="Types", font=("Lexend 16"), bg="#f0f0f0").place(x=300, y=380)
    
    type_images = [] # saves the images of the pokemon types
    for t in pokemon['types']: # gets the images of the pokemon types
        img_path = f"pokemon types/{t['type']['name']}.png"
        img = Image.open(img_path)
        img = ImageTk.PhotoImage(img)
        type_images.append(img)
        
    for index, img in enumerate(type_images): # shows the images of the pokemon types
        Label(temp_frame, image=img, bg="#f0f0f0").place(x=300 + index * 140, y=415)

    temp_frame.type_images = type_images
    
    type_list = [] # saves the info of the pokemon types
    for t in pokemon['types']:
        all_types = t['type']['name']
        type_info = get_type_info(all_types) # gets the info of the pokemon types
        type_list.append(type_info) # saves the info of the pokemon types

    all_weaknesses = set()
    all_resistances = set()

    Label(temp_frame, text="Weaknesses", font=("Lexend 16"), bg="#f0f0f0").place(x=300, y=470)
    
    for type_info in type_list:
        type_weaknesses, type_resistances = get_damage_relations(type_info) # gets the weaknesses and resistances of the pokemon types
        all_weaknesses.update(type_weaknesses) # adds the weaknesses and resistances of the pokemon types
        all_resistances.update(type_resistances) # adds the weaknesses and resistances of the pokemon types

    remaining_weaknesses = all_weaknesses - all_resistances # gets the remaining weaknesses by deleting the resistances

    weakness_frame = Frame(temp_frame, bg="#f0f0f0")
    weakness_frame.place(x=293, y=505)

    weakness_images = [] # saves the images of the remaining weaknesses
    for index, type_name in enumerate(remaining_weaknesses):
        img_path2 = f"pokemon types/{type_name}.png"
        img2 = Image.open(img_path2)
        img2 = ImageTk.PhotoImage(img2)
        
        # creates a row and column for the images to be displayed
        row = index // 2
        column = index % 2 
        
        Label(weakness_frame, image=img2, bg="#f0f0f0").grid(row=row, column=column, sticky=W, padx=6, pady=3)
        weakness_images.append(img2)
        
    weakness_frame.weakness_images = weakness_images
    
    # creates a close button to close the frame
    close_button = Button(temp_frame, text="X", width=10, bg="#fff", command=temp_frame.destroy)
    
    close_button.bind('<Enter>', on_hover)
    close_button.bind('<Leave>', on_default)
    
    close_button.place(x=10, y=12)

def title_screen():
    temp_frame = create_temp_frame()
    
    title_frame_center = Frame(root, bg="#314663")
    title_frame_center.place(x=0, y=210, width=600, height=300)
    
    Label(title_frame_center, text="Welcome to\nPokéFinder!", font=("Lexend 22 bold"), bg="#314663", fg="#fff").pack(pady=10)
    
    Label(title_frame_center,
          text="Click on any Pokémon icon or search by ID or name\nto access its details. Only the first 151 Pokémon\nare displayed. Use the search function to find\nPokémon in any generation.", 
          font=("Lexend 15"), bg="#314663", fg="#fff").pack(pady=10)

    Button(title_frame_center, text="Start", width=15, font=("Lexend 12"), bg="#fff",
           command=lambda:[temp_frame.destroy(), title_frame_center.destroy()]).pack(pady=10)
        
nav_frame = Frame(root, bg="#314663")
nav_frame.place(x=0, y=0, width=600, height=50)

Label(root, text="PokéFinder", font=("Lexend 22 bold"), bg="#314663", fg="#fff").place(x=20, y=6)

search_bar = Entry(root, width=30)
search_bar.place(x=280, y=16)

# error labels
error_label_id = Label(root, text="Error: Invalid Pokemon ID.", font=("Lexend 9"), bg="#e13f38", fg="#fff")
error_label_name = Label(root, text="Error: Invalid Pokemon name.", font=("Lexend 9"), bg="#e13f38", fg="#fff")

# search button
search_button = Button(root, text="Search", width=10, font=("Lexend 7"), 
                       command=lambda:filter_pokemon(error_label_id, error_label_name))
search_button.place(x=470, y=15)

# previous and next buttons to switch between frames
previous_button = Button(root, text="Previous", width=10, command=previous_frame)

previous_button.bind('<Enter>', on_hover)
previous_button.bind('<Leave>', on_default)

previous_button.place(x=30, y=70)

next_button = Button(root, text="Next", width=10, command=next_frame)

next_button.bind('<Enter>', on_hover)
next_button.bind('<Leave>', on_default)

next_button.place(x=490, y=70)

# main frame list to iterate through
main_frame_list = []

# the number of frames and rows and columns
frames = 1
rows = 1
columns = 1

update_main_frames(frames, rows, columns)

main_frame_list[0].place(x=22, y=100)
current_frame = main_frame_list[0]

page_number = Label(root, text=f"1/{len(main_frame_list)}", font=("Lexend 10"), bg="#b7c9e2")
page_number.place(x=30, y=670)

title_screen()

root.mainloop()