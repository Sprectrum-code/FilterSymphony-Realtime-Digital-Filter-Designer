from classes.pole import Pole
from classes.zero import Zero
from classes.filterCodeGenerator import FilterCodeGenerator

# Create test poles and zeros
pole1 = Pole([0.5, 0.4])
pole1_conj = Pole([0.5, -0.4])
pole1.conjugate = pole1_conj
pole1_conj.conjugate = pole1

zero1 = Zero([-1.0, 0])
zero1_conj = Zero([-1.0, 0])
zero1.conjugate = zero1_conj
zero1_conj.conjugate = zero1

# Create the lists with conjugate pairs
poles_list = [(pole1, pole1_conj)]
zeros_list = [(zero1, zero1_conj)]

# Generate the code
generator = FilterCodeGenerator()
generator.save_to_file(poles_list, zeros_list, "myCcode")