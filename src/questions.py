import tkinter as tk
from tkinter import messagebox
import connection
import querys

class MovieRecommendationApp:
    def __init__(self, master):
        self.master = master
        master.title("Movie Recommendation App")
        master.geometry("400x200")
        master.configure(bg="#333")

        self.question_map = {
            "What do you prefer movies or series?": {
                "MOVIE": "Do you want it to have any age restrictions or not",
                "SHOW": "Do you want it to have any age restrictions or not",
                "undefined": "Do you want it to have any age restrictions or not"
            },
            "Do you want it to have any age restrictions or not": {
                "Yes": "Which one?",
                "No": "¡Te recomendaría ver una película!"
            },
            "Which one?": "¡Te recomendaría ver una película!"
        }

        self.answer_options = {
            "What do you prefer movies or series?": ["MOVIE", "SHOW", "undefined"],
            "Do you want it to have any age restrictions or not": ["Yes", "No"],
            "Which one?": ["G", "PG", "PG-13", "R", "NC-17","TV-Y", "TV-Y7", "TV-G", "TV-PG", "TV-14", "TV-MA", "undefined"],
            "What genre do you like?": ["comedy", "family", "animation", "action",
                                        "fantasy", "horror", "drama", "war", "western",
                                        "european", "romance", "thriller", "crime", "history", 
                                        "sport", "scifi", "documentation", "music", "reality", "undefined"],
            "Do you prefer it to last a maximum of 2 hours?": ["Yes", "No"],
            "What streaming platform do you want it to be on?": ["Amazon_Prime", "Disney_Plus", "HBOMax", 
                                                                 "Hulu", "Netflix", "ParamountTV",
                                                                "Rakuten_Viki", "undefined"],
            "What country do you want it to be from?": ["US", "GB", "MX", "CA", "DE", "SU", "IN", "XX", "IT", "JP", "FR", "HK", "ES",
                                                        "IL", "AU", "CH", "IE", "GR", "CN", "PH", "NL", "YU", "CI", "PR", "LI", "KR", 
                                                        "XC", "HU", "TW", "AN", "MC", "CO", "RO", "EG", "TR", "BE", "ZA", "PT", "CL", 
                                                        "SE", "BR", "DK", "NZ", "RU", "LU", "CZ", "FI", "AT", "SK", "AR", "VE", "TH", 
                                                        "PL", "AE", "SI", "BA", "ID", "NO", "AF", "IR", "IS", "BG", "JM", "RS", "SZ", 
                                                        "LT", "TC", "SG", "UY", "BO", "UA", "MY", "TN", "QA", "NG", "KZ", "GQ", "MT", 
                                                        "SO", "KE", "UnitedStatesofAmerica", "MA", "VN", "BD", "FJ", "MN", "UG", "TT", 
                                                        "PK", "XK", "PE", "DO", "SV", "GE", "PS", "HR", "LV", "AQ", "LB", "KH", "CR", 
                                                        "BM", "JO", "PA", "AL", "CY", "CU", "PY", "EE", "ET", "PF", "EC", "IO", "AM", 
                                                        "SY", "CM", "LY", "SUHH", "KI", "BW", "XG", "DZ", "SN", "AO", "RW", "GT", "ZW", 
                                                        "KW", "CS", "MK", "BY", "GH", "BF", "BS", "Lebanon", "SA", "CD", "GL", "IQ", 
                                                        "VA", "TZ", "NP", "KG", "BT", "MW", "LK", "MU", "NA", "KN", "FO", "HN", "SB", 
                                                        "ZM", "NC", "MO", "undefined"],
            "What decade do you want it to be?": ["1900","1910","1920","1930", "1940", "1950", "1960", 
                                                  "1970", "1980","1990","2000","2010", "2020", "undefined"],
            "¡Te recomendaría ver una película!": ["Yes", "No"]
        }

        self.current_question = "What do you prefer movies or series?"
        self.user_answers = {}  # Diccionario para almacenar las respuestas del usuario

        self.question_label = tk.Label(master, text=self.current_question, fg="white", bg="#333")
        self.question_label.pack()

        self.answer_var = tk.StringVar(master)
        self.answer_var.set(self.answer_options[self.current_question][0])
        self.answer_menu = tk.OptionMenu(master, self.answer_var, *self.answer_options[self.current_question])
        self.answer_menu.config(bg="#666", fg="white")
        self.answer_menu.pack()

        self.button = tk.Button(master, text="Next", command=self.next_question, bg="#666", fg="white")
        self.button.pack()

    def next_question(self):
        answer = self.answer_var.get()
        self.user_answers[self.current_question] = answer  # Almacenar la respuesta del usuario
        
        if self.current_question == "What do you prefer movies or series?":
            next_question_text = self.question_map[self.current_question][answer]
            self.current_question = next_question_text
        else:
            next_question_text = self.question_map[self.current_question]
            self.current_question = next_question_text

        self.answer_var.set(self.answer_options[self.current_question][0])
        self.answer_menu['menu'].delete(0, 'end')
        for option in self.answer_options[self.current_question]:
            self.answer_menu['menu'].add_command(label=option, command=tk._setit(self.answer_var, option))
        
        self.question_label.config(text=self.current_question)
        
def main():
    root = tk.Tk()
    app = MovieRecommendationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
