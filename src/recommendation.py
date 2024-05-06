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
                "MOVIE": "Do you want it to have any film age restrictions?",
                "SHOW": "Do you want it to have any TV age restrictions?"
            },
            "Do you want it to have any TV age restrictions?":"What genre do you like?",
            "Do you want it to have any film age restrictions?":"What genre do you like?",
            "What genre do you like?": "Do you prefer it to last a maximum of 2 hours?",
            "Do you prefer it to last a maximum of 2 hours?": "What streaming platform do you want it to be on?",
            "What streaming platform do you want it to be on?": "What country do you want it to be from?",
            "What country do you want it to be from?": "What decade do you want it to be?",
            "What decade do you want it to be?": "Who do you want to star in it? (Actor or Director)",
            "Who do you want to star in it? (Actor or Director)": "¡Te recomendaría ver una película!"
        }

        self.answer_options = {
            "What do you prefer movies or series?": ["MOVIE", "SHOW"],
            "Do you want it to have any TV age restrictions?": ["TV-Y", "TV-Y7", "TV-G", "TV-PG",
                                                                "TV-14", "TV-MA", "undefined"],
            "Do you want it to have any film age restrictions?": ["G", "PG", "PG-13", "R", "NC-17", "undefined"],
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

        if self.current_question == "Who do you want to star in it? (Actor or Director)":
            input_frame = tk.Frame(self.master, bg="#333")
            input_frame.pack(pady=10)
            input_label = tk.Label(input_frame, text="Who do you want to star in it? (Actor or Director):", fg="white", bg="#333")
            input_label.pack()
            input_var = tk.StringVar()
            input_entry = tk.Entry(input_frame, textvariable=input_var, bg="#666", fg="white")
            input_entry.pack()
            input_button = tk.Button(input_frame, text="Next", command=lambda: self.handle_user_input(input_var), bg="#666", fg="white")
            input_button.pack()
            self.question_label.pack_forget()
            self.answer_menu.pack_forget()
            self.button.pack_forget()     
        else:
            self.answer_var.set(self.answer_options[self.current_question][0])
            self.answer_menu['menu'].delete(0, 'end')
            for option in self.answer_options[self.current_question]:
                self.answer_menu['menu'].add_command(label=option, command=tk._setit(self.answer_var, option))
        
        self.question_label.config(text=self.current_question)

        if self.current_question == "¡Te recomendaría ver una película!":
            user_responses = [answer for _, answer in self.user_answers.items()]
            print("Respuestas del usuario:", user_responses)
            recommendations = self.get_recommendation(user_responses)
            self.show_recommendations(recommendations)

    def get_recommendation(self, user_responses):
        cursor = connection.connection.cursor()
        if user_responses[3] == "Yes":
            user_responses[3] = 120
        else:
            user_responses[3] = 600
        if user_responses[1] == "undefined":
            user_responses[1] = ["G", "PG", "PG-13", "R", "NC-17"]
        recommendation = querys.recommendation(user_responses[0], user_responses[1], user_responses[2], user_responses[3], user_responses[4], user_responses[5], user_responses[6])
        cursor.execute(recommendation, (user_responses[0], user_responses[1], user_responses[2], user_responses[3], user_responses[4], user_responses[5], user_responses[6], int(user_responses[6]) + 10))
        resultados = cursor.fetchall()
        cursor.close()
        recommendations = []
        for resultado in resultados:
            title = resultado[0]
            recommendations.append(title)
        if not recommendations:
            messagebox.showwarning("Warning", "No recommendations were found in the database.")
            return "No recommendations were found in the database."
        return recommendations

    def handle_user_input(self, input_var):
        input_value = input_var.get()
        if input_value.strip():
            updated_answers = self.user_answers.copy()
            updated_answers["Who do you want to star in it? (Actor or Director)"] = input_value.strip()
            self.user_answers = updated_answers
            self.next_question()
        else:
            messagebox.showwarning("Warning", "Please enter a valid name.")

    def show_recommendations(self, recommendations):
        self.recommendations_window = tk.Toplevel(self.master)
        self.recommendations_window.title("Movie Recommendations")
        self.recommendations_window.geometry("800x500")
        self.recommendations_window.configure(bg="#333")

        recommendation_label = tk.Label(self.recommendations_window, text="Recommended Titles:", fg="white", bg="#333")
        recommendation_label.pack()

        recommendations_text = "\n".join(recommendations)
        recommendations_display = tk.Text(self.recommendations_window, bg="#666", fg="white")
        recommendations_display.insert(tk.END, recommendations_text)
        recommendations_display.pack()

        agree_button = tk.Button(self.recommendations_window, text="I agree", command=self.agree_recommendations, bg="#666", fg="white")
        agree_button.pack(side=tk.LEFT, padx=10, pady=10)

        disagree_button = tk.Button(self.recommendations_window, text="I disagree", command=self.disagree_recommendations, bg="#666", fg="white")
        disagree_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def agree_recommendations(self):
        messagebox.showinfo("Feedback", "Thank you for your feedback! We're glad you found the recommendations helpful.")
        self.recommendations_window.destroy()

    def disagree_recommendations(self):
        cursor = connection.connection.cursor()
        recommendation = querys.recommendationDefault()
        cursor.execute(recommendation)
        resultados = cursor.fetchall()
        cursor.close()
        recommendations = []
        for resultado in resultados:
            title = resultado[0]
            recommendations.append(title)

        self.recommendations_window = tk.Toplevel(self.master)
        self.recommendations_window.title("Movie Recommendations")
        self.recommendations_window.geometry("800x500")
        self.recommendations_window.configure(bg="#333")

        recommendation_label = tk.Label(self.recommendations_window, text="Recommended Titles:", fg="white", bg="#333")
        recommendation_label.pack()

        recommendations_text = "\n".join(recommendations)
        recommendations_display = tk.Text(self.recommendations_window, bg="#666", fg="white")
        recommendations_display.insert(tk.END, recommendations_text)
        recommendations_display.pack()

def main():
    root = tk.Tk()
    app = MovieRecommendationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
