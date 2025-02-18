mathOperations = {
    "subtraction-var": {
        "Equation": "3x + 13 = 2x + 6",
        "Operation": "Subtract 2x from both sides.",
        "Result": "3x - 2x + 13 = 2x - 2x + 6",
    },
    "subtraction-const": {
        "Equation": "3x + 13 = 2x + 6",
        "Operation": "Subtract 6 from both sides.",
        "Result": "3x + 13 - 6 = 2x + 6 - 6",
    },
    "division-simple": {
        "Equation": "4x = 20",
        "Operation": "Divide both sides by 4.",
        "Result": "4x/4 = 20/4",
    },
    "division-complex": {
        "Equation": "2(x + 3) = 16",
        "Operation": "Divide both sides by 2.",
        "Result": "(2(x + 3))/2 = 16/2; x + 3 = 8",
    },
    "distribute-multiplication": {
        "Equation": "2(x + 4) = 10",
        "Operation": "Distribute the multiplication, multiply both sides by 2.",
        "Result": "2*x + 2*4 = 10",
    },
    "divide": {
        "Equation": "4x/4 = 20/4",
        "Operation": "Simplify the division, divide both sides by 4.",
        "Result": "x = 5",
    },
    "combine-like-var": {
        "Equation": "4x - 2x + 1 = 15",
        "Operation": "Combine like variable terms, simplify 4x - 2x.",
        "Result": "2x + 1 = 15",
    },
    "combine-like-const": {
        "Equation": "3x - 1 + 1 = -10 + 1",
        "Operation": "Combine like constant terms, add 1 to both sides to simplify.",
        "Result": "3x = -9",
    },
    "cancel-var": {
        "Equation": "10x + 8 = 14x + 4",
        "Operation": "Cancel the variable term (10x) from both sides.",
        "Result": "8 = 4x + 4",
    },
    "cancel-const": {
        "Equation": "2x + 5 = 15",
        "Operation": "Cancel the constant term (5) from both sides.",
        "Result": "2x = 10",
    },
}

KNOWLEDGE_COMPONENTS = dict()
for kc in mathOperations:
    equation = mathOperations[kc]["Equation"]
    operation = mathOperations[kc]["Operation"]
    result = mathOperations[kc]["Result"]
    KNOWLEDGE_COMPONENTS[kc] = f"For example, we have the following equation: {equation}. And we conduct the following operation: {operation} And get the result {result}."

