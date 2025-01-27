import numpy as np

class allPassFiltersLibrary:
    def __init__(self):
        self.filter_library = {}
        for i, pole_real in enumerate(np.linspace(0.1, 0.9, 10)):
            pole = (pole_real, 0.0)  
            zero = (1/pole_real, 0.0) 
            self.filter_library[f'ap{i+1}'] = (pole, zero)
        self.custom_filter_library = {}
    
    def get_filter(self, filter_name):
        if filter_name in self.filter_library:
            return self.filter_library[filter_name]
        raise ValueError(f"Filter {filter_name} not found")
    
    def make_custom_all_pass(self,coefficient):
        if coefficient  == 0:
            return
        pole = (coefficient, 0.0)
        zero = (1/coefficient, 0.0)
        self.custom_filter_library[f'custom filter a={coefficient}'] = (pole, zero)
        return (pole, zero)
    