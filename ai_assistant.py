"""
AI Assistant - Natural Language Processing for Calculator
"""
import re
import math
import random
from typing import Dict, List, Any, Tuple

class AICalculatorAssistant:
    """AI-powered assistant for the calculator"""
    
    def __init__(self):
        self.conversation_history = []
        
        # Mathematical patterns for natural language
        self.patterns = {
            'percentage': r'(\d+)\s*percent\s*of\s*(\d+)',
            'square_root': r'square root of\s*(\d+)',
            'power': r'(\d+)\s*to the power of\s*(\d+)',
            'factorial': r'factorial of\s*(\d+)',
            'sine': r'sine of\s*(\d+)',
            'cosine': r'cosine of\s*(\d+)',
            'tangent': r'tangent of\s*(\d+)',
            'logarithm': r'log(?:arithm)?\s*(?:of\s*)?(\d+)',
            'average': r'average of\s*([\d\s,]+)',
        }
    
    def parse_natural_language(self, text: str) -> Dict[str, Any]:
        """Parse natural language into mathematical operations"""
        text = text.lower().strip()
        
        # Check for greetings
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        if any(word in text for word in greetings):
            return {'type': 'greeting', 'response': self._get_greeting()}
        
        # Check for help
        if any(word in text for word in ['help', 'what can you do', 'features']):
            return {'type': 'help', 'response': self._get_help()}
        
        # Check for calculation patterns
        for pattern_name, pattern in self.patterns.items():
            match = re.search(pattern, text)
            if match:
                return self._handle_pattern(pattern_name, match.groups())
        
        # Check for basic arithmetic in natural language
        if 'plus' in text or 'add' in text:
            return self._handle_basic_operation(text, 'add')
        if 'minus' in text or 'subtract' in text:
            return self._handle_basic_operation(text, 'subtract')
        if 'times' in text or 'multiply' in text:
            return self._handle_basic_operation(text, 'multiply')
        if 'divided by' in text or 'divide by' in text:
            return self._handle_basic_operation(text, 'divide')
        
        # Try to extract numbers and infer operation
        numbers = re.findall(r'\d+\.?\d*', text)
        if numbers and len(numbers) >= 2:
            return self._infer_operation(text, numbers)
        
        return {'type': 'unknown', 'response': "I'm not sure how to help. Try saying 'help' for features."}
    
    def _handle_pattern(self, pattern_name: str, groups: Tuple) -> Dict:
        """Handle specific mathematical patterns"""
        try:
            if pattern_name == 'percentage':
                percent, number = map(float, groups)
                result = (percent * number) / 100
                return {
                    'type': 'calculation',
                    'expression': f"{percent}% of {number}",
                    'result': f"{result:.2f}",
                    'value': result
                }
            
            elif pattern_name == 'square_root':
                n = float(groups[0])
                result = math.sqrt(n)
                return {
                    'type': 'calculation',
                    'expression': f"√{n}",
                    'result': f"{result:.4f}",
                    'value': result
                }
            
            elif pattern_name == 'power':
                base, exp = map(float, groups)
                result = base ** exp
                return {
                    'type': 'calculation',
                    'expression': f"{base}^{exp}",
                    'result': f"{result:.4f}",
                    'value': result
                }
            
            elif pattern_name == 'factorial':
                n = int(float(groups[0]))
                result = math.factorial(n)
                return {
                    'type': 'calculation',
                    'expression': f"{n}!",
                    'result': f"{result:,}",
                    'value': result
                }
            
            elif pattern_name in ['sine', 'cosine', 'tangent']:
                angle = float(groups[0])
                radians = math.radians(angle)
                func = {'sine': math.sin, 'cosine': math.cos, 'tangent': math.tan}[pattern_name]
                result = func(radians)
                return {
                    'type': 'calculation',
                    'expression': f"{pattern_name}({angle}°)",
                    'result': f"{result:.4f}",
                    'value': result
                }
            
            elif pattern_name == 'logarithm':
                n = float(groups[0])
                if n <= 0:
                    return {'type': 'error', 'response': "Cannot take logarithm of non-positive number"}
                result = math.log10(n)
                return {
                    'type': 'calculation',
                    'expression': f"log({n})",
                    'result': f"{result:.4f}",
                    'value': result
                }
            
            elif pattern_name == 'average':
                numbers = [float(x) for x in re.findall(r'\d+\.?\d*', groups[0])]
                if numbers:
                    result = sum(numbers) / len(numbers)
                    return {
                        'type': 'calculation',
                        'expression': f"Average of {numbers}",
                        'result': f"{result:.2f}",
                        'value': result
                    }
        
        except Exception as e:
            return {'type': 'error', 'response': f"Error: {str(e)}"}
        
        return {'type': 'unknown', 'response': "Couldn't compute that."}
    
    def _handle_basic_operation(self, text: str, operation: str) -> Dict:
        """Handle basic operations from natural language"""
        numbers = re.findall(r'\d+\.?\d*', text)
        if numbers:
            nums = [float(n) for n in numbers]
            
            if operation == 'add':
                result = sum(nums)
                return {
                    'type': 'calculation',
                    'expression': ' + '.join(map(str, nums)),
                    'result': str(result),
                    'value': result
                }
            elif operation == 'subtract':
                result = nums[0] - sum(nums[1:]) if len(nums) > 1 else nums[0]
                return {
                    'type': 'calculation',
                    'expression': f"{nums[0]} - {' - '.join(map(str, nums[1:])) if len(nums)>1 else '0'}",
                    'result': str(result),
                    'value': result
                }
            elif operation == 'multiply':
                result = 1
                for n in nums:
                    result *= n
                return {
                    'type': 'calculation',
                    'expression': ' × '.join(map(str, nums)),
                    'result': str(result),
                    'value': result
                }
            elif operation == 'divide':
                if 0 in nums[1:]:
                    return {'type': 'error', 'response': "Cannot divide by zero!"}
                result = nums[0]
                for n in nums[1:]:
                    result /= n
                return {
                    'type': 'calculation',
                    'expression': ' ÷ '.join(map(str, nums)),
                    'result': str(result),
                    'value': result
                }
        
        return {'type': 'unknown', 'response': "Couldn't find numbers to operate on."}
    
    def _infer_operation(self, text: str, numbers: List[str]) -> Dict:
        """Infer operation from context"""
        nums = [float(n) for n in numbers]
        
        # Check for sum operation
        result = sum(nums)
        return {
            'type': 'calculation',
            'expression': f"Sum of {nums}",
            'result': str(result),
            'value': result
        }
    
    def _get_greeting(self) -> str:
        """Generate greeting response"""
        greetings = [
            "Hello! 👋 I'm your AI math assistant. How can I help?",
            "Hi there! 🧮 Ready to do some calculations?",
            "Greetings! 🌟 I can help with math problems and more!",
            "Hey! 🚀 What would you like to calculate today?"
        ]
        return random.choice(greetings)
    
    def _get_help(self) -> str:
        """Get help message"""
        return """
        🤖 I can help you with:
        
        📊 Basic Operations:
        • Addition, Subtraction, Multiplication, Division
        
        🔢 Advanced Math:
        • Square root, Power, Factorial
        • Logarithms (log, ln)
        
        📐 Trigonometry:
        • Sine, Cosine, Tangent (in degrees)
        
        📈 Statistics:
        • Average, Mean, Median
        
        💬 Examples:
        • "What's 20% of 50?"
        • "Square root of 144"
        • "Factorial of 5"
        • "Sine of 30"
        • "Average of 5, 8, 12, 15"
        """
    
    def smart_suggest(self, input_text: str, history: List) -> List[str]:
        """Provide intelligent suggestions based on input and history"""
        suggestions = []
        
        # Context-based suggestions
        if 'sqrt' in input_text or '√' in input_text:
            suggestions.append("Try: square root of 144")
        if 'percent' in input_text or '%' in input_text:
            suggestions.append("Try: 15% of 200")
        if 'factorial' in input_text or '!' in input_text:
            suggestions.append("Try: factorial of 5")
        if 'sin' in input_text:
            suggestions.append("Try: sine of 30")
        if 'log' in input_text:
            suggestions.append("Try: log of 100")
        
        # Suggest based on history
        if history and len(history) > 0:
            last_entry = history[-1]
            if last_entry.get('expression'):
                suggestions.append(f"Repeat: {last_entry['expression']}")
        
        # Default suggestions
        if not suggestions:
            suggestions = [
                "Try: 2 + 2 = 4",
                "Try: square root of 144",
                "Try: 15% of 200",
                "Try: sine of 45",
                "Try: factorial of 5"
            ]
        
        return suggestions[:5]
    
    def correct_expression(self, expression: str) -> str:
        """Smart error correction for mathematical expressions"""
        # Fix common mistakes
        corrections = {
            '²': '**2',
            '³': '**3',
            '×': '*',
            '÷': '/',
            ' ': '',
            '--': '+',
            '++': '+',
            '**': '^',
            'x': '*',
            'X': '*'
        }
        
        corrected = expression
        for wrong, correct in corrections.items():
            corrected = corrected.replace(wrong, correct)
        
        # Fix unbalanced parentheses
        open_parens = corrected.count('(')
        close_parens = corrected.count(')')
        if open_parens > close_parens:
            corrected += ')' * (open_parens - close_parens)
        
        return corrected
    
    def get_insights(self, history: List[Dict]) -> str:
        """Generate insights from calculation history"""
        if not history:
            return "📊 No calculations yet. Start calculating to get insights!"
        
        # Analyze history
        total = len(history)
        operations = {}
        error_count = 0
        
        for entry in history:
            op = entry.get('operation', 'unknown')
            operations[op] = operations.get(op, 0) + 1
            result = entry.get('result', '')
            if isinstance(result, str) and 'error' in result.lower():
                error_count += 1
        
        most_common = max(operations.items(), key=lambda x: x[1]) if operations else ('none', 0)
        
        insights = f"""
        📊 Calculation Insights:
        • Total calculations: {total}
        • Most common operation: {most_common[0]} ({most_common[1]} times)
        • Error rate: {(error_count/total)*100:.1f}%
        """
        
        # Add personalized suggestions
        if most_common[0] in ['add', 'subtract']:
            insights += "\n💡 Try: Advanced functions like sin, cos, or log"
        elif most_common[0] in ['sin', 'cos', 'tan']:
            insights += "\n💡 Try: Statistical functions like mean, median"
        elif most_common[0] in ['sqrt', 'power']:
            insights += "\n💡 Try: Solving equations or calculating logarithms"
        elif most_common[0] == 'percentage':
            insights += "\n💡 Try: Compound interest or growth calculations"
        
        return insights
