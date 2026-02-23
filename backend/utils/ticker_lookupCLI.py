import pandas as pd
from difflib import get_close_matches

#creating class to save reads and improve speed
class TickerLookup:
    #constructor
    def __init__(self, csv_path="../data/tickers.csv"):
        
        self.df = pd.read_csv(csv_path)

        self.company_names=self.df["Name"].tolist()
        self.symbols=self.df["Symbol"].tolist()

        self.company_names_lowercased=[name.lower() for name in self.company_names] #i am a list comprehension GAWD
        
    def match_name_to_ticker(self, input_company_name: str):

        cleaned_input_string=input_company_name.strip()
        
        if cleaned_input_string.upper() in self.symbols:
            return cleaned_input_string.upper()
        
        potential_matches=get_close_matches(cleaned_input_string, self.company_names, n=3, cutoff=.8)
        if not potential_matches:
            print("no matches for: ",cleaned_input_string )
            return None
        
        if len(potential_matches)==1:
            match=self.df["Name"]==company_name
            matching_row=self.df[match]
            first_row = matching_row.iloc[0]
            return first_row["Symbol"]
        
        print(f"Multiple potential companies matched {cleaned_input_string} ")
        count=1
        for name in potential_matches:
            print(str(count) + ":" + name)
            count+=1
        
        user_choice=input("please select the correct number one or 0 if none")

        try:
            user_choice=int(user_choice)
            if user_choice==0:
                return None
            selected_name=potential_matches[user_choice-1]
            match=self.df["Name"]==selected_name
            matching_row=self.df[match]
            first_row = matching_row.iloc[0]
            return first_row["Symbol"]
        except(ValueError,IndexError):
            print("invalid choice, please try again")
            return None
            

        
if __name__ == "__main__":
    lookup_list=TickerLookup("../data/tickers.csv")
    test_cases = [
    ("Adamas Trust Inc.", "ADAM"),       
    ("Adamas", "ADAM"),                   
    ("AGNC Investment Corp.", "AGNC"),    
    ("AGNC", "AGNC"),
    ("NVIDIA Corp", "NVDA"),
    ("Apple Inc.", "AAPL")                     
    ]

    for company_name, expected in test_cases:
        result=lookup_list.match_name_to_ticker(company_name)
        print(f"Input: {company_name} -> Lookup: {result} | Expected: {expected} | {'PASS' if result == expected else 'FAIL'}")