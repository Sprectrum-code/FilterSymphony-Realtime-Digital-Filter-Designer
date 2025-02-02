/* 
 * Credits to Team 6 SBME 26
 * Automatically generated biquad filter implementation
 * Number of stages: 8
 */

#include <string.h>  // for memset

/* Filter Configuration */
#define NUM_STAGES 8
#define STATE_SIZE (NUM_STAGES * 4)
#define COEFF_LENGTH (NUM_STAGES * 5)

/* Filter State Structure */
typedef struct {
    float state[STATE_SIZE];
    float output;
} FilterState;

/* Filter Coefficients */
static const float filter_coefficients[COEFF_LENGTH] = {
    0.569307f,
    -0.903610f,
    0.569307f,
    -1.756521f,
    0.852587f,
    0.630037f,
    -1.000000f,
    0.630037f,
    -1.403500f,
    0.544850f,
    0.630037f,
    -1.000000f,
    0.630037f,
    -1.403500f,
    0.544850f,
    0.569307f,
    -0.903610f,
    0.569307f,
    -1.756521f,
    0.852587f,
    1.000000f,
    0.000000f,
    0.000000f,
    -0.543074f,
    0.618338f,
    1.000000f,
    0.000000f,
    0.000000f,
    -0.717599f,
    0.265275f,
    1.000000f,
    0.000000f,
    0.000000f,
    -0.717599f,
    0.265275f,
    1.000000f,
    0.000000f,
    0.000000f,
    -0.543074f,
    0.618338f
};

/* Initialize filter state */
void filter_init(FilterState *pState) {
    memset(pState->state, 0, sizeof(float) * STATE_SIZE);
    pState->output = 0.0f;
}

/* Process a single sample through the filter */
float filter_process(FilterState *pState, float input) {
    const float *pCoeff = filter_coefficients;
    float output = input;
    
    /* Process through all biquad stages */
    for (int stage = 0; stage < NUM_STAGES; stage++) {
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
    }
    
    pState->output = output;
    return output;
}

/* Example usage */
int main() {
    FilterState state;
    float input = 1.0f;
    float output;
    
    /* Initialize filter */
    filter_init(&state);
    
    /* Process some samples */
    for(int i = 0; i < 10; i++) {
        output = filter_process(&state, input);
        printf("Input: %f, Output: %f\n", input, output);
    }
    
    return 0;
}