import random
import customtkinter as ctk


class BikeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1200x800")
        self.font = ("Roboto",30)
        self.bike_path = "bikes.csv"
        self.create_form()

    def create_form(self):
        self.brand_label = ctk.CTkLabel(self, pady = 10, text="Brand Name", width=200, font=self.font)
        self.brand_label.pack(ipady = 10)
        self.brand_input = ctk.CTkEntry(self, placeholder_text="Brand Name", width=200, font=self.font)
        self.brand_input.pack(ipady = 10)
        self.model_label = ctk.CTkLabel(self, text="Model Name", font=self.font, pady = 10)
        self.model_label.pack(ipady = 10)
        self.model_input = ctk.CTkEntry(self, placeholder_text="Model Name", width=200, font=self.font)
        self.model_input.pack(ipady = 10)
        self.size_label = ctk.CTkLabel(self, text="Brand Name", font=self.font, pady = 10)
        self.size_label.pack(ipady = 10)
        self.size_input = ctk.CTkOptionMenu(self, values=SIZE, font=self.font, dropdown_font=self.font)
        self.size_input.pack()
        self.add_button = ctk.CTkButton(self, text="Add Bike", font=self.font, command=self.add_bike)
        self.add_button.pack(ipady = 15, pady = 20)


    def add_bike(self):
        brand = self.brand_input.get()
        model = self.model_input.get()
        size = self.size_input.get()
        if brand and model and size:
            with open(self.bike_path, "a+") as file:
                bike = Bike(brand, model, size)
                line = bike.to_csv() + "\n"
                file.write(line)
            self.brand_input.delete(0, ctk.END)
            self.model_input.delete(0, ctk.END)
            self.size_input.set("S")
        else:
            print("Fill all the inputs")

class Bike:
    id = 0

    def __init__(self, brand, model, size):
        Bike.id += 1
        self.brand = brand
        self.model = model
        self.size = size
        self.id = Bike.id
    
    def new():
        brand = random.choice(list(BRAND_MODEL.keys()))
        model = random.choice(BRAND_MODEL[brand])
        size = random.choice(SIZE)
        return Bike(brand, model, size)
    
    def __str__(self):
        return f"{self.id} {self.brand} {self.model} {self.size}"
    
    def __repr__(self):
        return str(self)
    
    def to_csv(self):
        return f"{self.id}, {self.brand}, {self.model}, {self.size},"

SIZE = ["S", "M", "L", "XL"]
BRAND_MODEL = {"Bianchi" : ["Stadale", "Piastri"], "Giant" : ["Trance", "Omnium"], "Autor" : ["Karel", "Pepa"]}


if __name__ == "__main__":
    # bikes = [Bike.new() for i in range(10)]
    # print(bikes)
    # with open("bikes.csv", "a+") as file:
    #     for bike in bikes:
    #         bike_str = bike.to_csv() + "\n"
    #         file.write(bike_str)
    app = BikeApp()
    app.mainloop()