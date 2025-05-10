import re
import sympy

def calculator_tool(query):
    """
    A calculator tool that can perform basic arithmetic operations.
    """
    try:
        # Check for specific patterns like "X employees on Y plan"
        employee_cost_match = re.search(r'(\d+)\s+employees.*?(\$\d+|\d+\s+dollars|\d+)', query.lower())
        if employee_cost_match:
            num_employees = int(employee_cost_match.group(1))
            cost_str = employee_cost_match.group(2).replace('$', '').replace('dollars', '').strip()
            cost = int(float(cost_str))
            total = num_employees * cost
            return f"For {num_employees} employees at ${cost} per employee, the total monthly cost would be ${total}."
        
        # Extract mathematical expression
        expression = re.search(r'\d+\s*[\+\-\*/]\s*\d+', query)
        if expression:
            # Extract the expression and evaluate it
            expr = expression.group(0).replace(' ', '')
            result = sympy.sympify(expr)
            return f"The result of {expr} is {result}."
        
        # If no expression is found, try to extract numbers and operation keywords
        numbers = re.findall(r'\d+', query)
        if len(numbers) >= 2:
            if "add" in query.lower() or "plus" in query.lower() or "sum" in query.lower():
                result = sum(int(num) for num in numbers)
                return f"The sum of {', '.join(numbers)} is {result}."
            elif "subtract" in query.lower() or "minus" in query.lower() or "difference" in query.lower():
                result = int(numbers[0]) - int(numbers[1])
                return f"The difference between {numbers[0]} and {numbers[1]} is {result}."
            elif "multiply" in query.lower() or "product" in query.lower():
                result = 1
                for num in numbers:
                    result *= int(num)
                return f"The product of {', '.join(numbers)} is {result}."
            elif "divide" in query.lower():
                result = int(numbers[0]) / int(numbers[1])
                return f"The result of dividing {numbers[0]} by {numbers[1]} is {result}."
        
        return "I couldn't calculate that. Please provide a valid mathematical expression."
    except Exception as e:
        return f"I couldn't calculate that. Please provide a valid mathematical expression. Error: {str(e)}"