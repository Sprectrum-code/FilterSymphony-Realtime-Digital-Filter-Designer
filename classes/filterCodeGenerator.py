class FilterCodeGenerator:
    def __init__(self, filter_name="filter1"):
        self.filter_name = filter_name
        
    def generate_code(self, poles_list, zeros_list):

        # Calculate coefficients for each stage
        coefficients = self._calculate_coefficients(poles_list, zeros_list)
        
        # Generate the complete C code
        c_code = self._generate_complete_c_code(coefficients, len(poles_list))
        
        return c_code
    
    def _calculate_coefficients(self, poles_list, zeros_list):

        # biquad coefficients
        coefficients = []
        
        for i in range(len(poles_list)):
            # Handle zeros for this section
            if i < len(zeros_list):
                zero, _ = zeros_list[i]
                z_real = zero.real
                z_imag = zero.imaginary
                
                # Calculate b coefficients
                b0 = 1.0
                b1 = -2 * z_real
                b2 = z_real * z_real + z_imag * z_imag
            else:
                b0, b1, b2 = 1.0, 0.0, 0.0
            
            # Handle poles for this section
            pole, _ = poles_list[i]
            p_real = pole.real
            p_imag = pole.imaginary
            
            # Calculate a coefficients
            a1 = -2 * p_real
            a2 = p_real * p_real + p_imag * p_imag
            
            # Normalize coefficients
            scale = 1.0 / max(abs(b0), abs(b1), abs(b2), abs(a1), abs(a2))
            coefficients.extend([b0 * scale, b1 * scale, b2 * scale, a1, a2])
            
        return coefficients
    
    def _generate_complete_c_code(self, coefficients, num_stages):
        # input --> coefficients of the biquad Filter
        # input --> num_stages where stage refers to a biquad filter section. 
        # Each stage is a 2nd-order filter, which means it processes a signal 
        # using two poles and two zeros.

        # Format coefficients for C array
        coeffs_str = ",\n    ".join([f"{c:.6f}f" for c in coefficients])
        
        return f"""/* 
 * Credits to Team 6 SBME 26
 * Automatically generated biquad filter implementation
 * Number of stages: {num_stages}
 */

#include <string.h>  // for memset

/* Filter Configuration */
#define NUM_STAGES {num_stages}
#define STATE_SIZE (NUM_STAGES * 4)
#define COEFF_LENGTH (NUM_STAGES * 5)

/* Filter State Structure */
typedef struct {{
    float state[STATE_SIZE];
    float output;
}} FilterState;

/* Filter Coefficients */
static const float filter_coefficients[COEFF_LENGTH] = {{
    {coeffs_str}
}};

/* Initialize filter state */
void filter_init(FilterState *pState) {{
    memset(pState->state, 0, sizeof(float) * STATE_SIZE);
    pState->output = 0.0f;
}}

/* Process a single sample through the filter */
float filter_process(FilterState *pState, float input) {{
    const float *pCoeff = filter_coefficients;
    float output = input;
    
    /* Process through all biquad stages */
    for (int stage = 0; stage < NUM_STAGES; stage++) {{
        float *statePtr = &pState->state[stage * 4];
        
        /* Get state variables */
        float x0 = output;
        float x1 = statePtr[0];
        float x2 = statePtr[1];
        float y1 = statePtr[2];
        float y2 = statePtr[3];
        
        /* Get coefficients */
        float b0 = pCoeff[stage * 5 + 0];
        float b1 = pCoeff[stage * 5 + 1];
        float b2 = pCoeff[stage * 5 + 2];
        float a1 = pCoeff[stage * 5 + 3];
        float a2 = pCoeff[stage * 5 + 4];
        
        /* Compute output */
        output = b0 * x0 + b1 * x1 + b2 * x2 + a1 * y1 + a2 * y2;
        
        /* Update state */
        statePtr[1] = x1;
        statePtr[0] = x0;
        statePtr[3] = y1;
        statePtr[2] = output;
    }}
    
    pState->output = output;
    return output;
}}

/* Example usage */
int main() {{
    FilterState state;
    float input = 1.0f;
    float output;
    
    /* Initialize filter */
    filter_init(&state);
    
    /* Process some samples */
    for(int i = 0; i < 10; i++) {{
        output = filter_process(&state, input);
        printf("Input: %f, Output: %f\\n", input, output);
    }}
    
    return 0;
}}"""
    
    def ensure_c_file(self, file_name):
        if file_name.endswith(".c"):
            return file_name
        else:
            return file_name + ".c"

    def save_to_file(self, poles_list, zeros_list, file_name="Filter.c"):

        corrected_file_name = self.ensure_c_file(file_name)
        c_code = self.generate_code(poles_list, zeros_list)
        with open(corrected_file_name, "w") as file:
            file.write(c_code)
        print(f"C code saved to {corrected_file_name}")

