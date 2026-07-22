"""
Calculator Controller - Mediates between Model and View with AI
"""
from typing import Optional, Dict, Any, List
from models.calculator_model import CalculatorModel
from utils.history_manager import HistoryManager
from utils.ai_assistant import AICalculatorAssistant
import math

class CalculatorController:
    """Controller with AI features"""
    
    def __init__(self):
        self.model = CalculatorModel()
        self.history = HistoryManager()
        self.ai_assistant = AICalculatorAssistant()
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input with AI assistance"""
        # Check if it's natural language
        if self._is_natural_language(user_input):
            return self.ai_assistant.parse_natural_language(user_input)
        
        # Try to evaluate as mathematical expression
        try:
            result = self.evaluate_expression(user_input)
            return {
                'type': 'calculation',
                'expression': user_input,
                'result': result,
                'value': float(result) if self._is_number(result) else None
            }
        except:
            # Get AI suggestions
            suggestions = self.ai_assistant.smart_suggest(
                user_input, 
                self.history.get_history()
            )
            return {
                'type': 'suggestion',
                'message': "💡 I can help with these calculations:",
                'suggestions': suggestions
            }
    
    def _is_natural_language(self, text: str) -> bool:
        """Check if input is natural language"""
        # Check for common natural language patterns
        language_patterns = [
            'what is', 'calculate', 'solve', 'find', 'how much',
            'plus', 'minus', 'times', 'divided by', 'percent of',
            'square root', 'power of', 'factorial', 'logarithm',
            'sine', 'cosine', 'tangent', 'average', 'mean',
            'hello', 'hi', 'help', 'what can you do', 'features'
        ]
        
        text_lower = text.lower()
        for pattern in language_patterns:
            if pattern in text_lower:
                return True
        
        # If it contains letters but not mathematical operators
        if any(c.isalpha() for c in text) and not any(c in '+-*/^√' for c in text):
            return True
        
        return False
    
    def _is_number(self, value: str) -> bool:
        """Check if string can be converted to number"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def evaluate_expression(self, expression: str) -> str:
        """Evaluate a mathematical expression with AI enhancement"""
        try:
            # Let AI correct the expression
            corrected = self.ai_assistant.correct_expression(expression)
            corrected = corrected.replace('×', '*').replace('÷', '/')
            
            # Safety evaluation with allowed functions
            safe_dict = {
                'sin': lambda x: self.model.sine(x, True),
                'cos': lambda x: self.model.cosine(x, True),
                'tan': lambda x: self.model.tangent(x, True),
                'sqrt': self.model.square_root,
                'log': self.model.logarithm,
                'ln': self.model.natural_log,
                'factorial': self.model.factorial,
                'pi': math.pi,
                'e': math.e,
                'abs': abs,
                'round': round,
                'max': max,
                'min': min
            }
            
            # Evaluate expression
            result = eval(corrected, {"__builtins__": {}}, safe_dict)
            
            # Add to history
            self.history.add_entry('eval', expression, str(result), 'standard')
            return str(result)
            
        except ZeroDivisionError:
            return "❌ Error: Division by zero"
        except SyntaxError:
            return "❌ Error: Check your syntax"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def perform_basic_operation(self, a: float, b: float, operator: str) -> str:
        """Perform basic arithmetic operations"""
        operation_map = {
            '+': self.model.add,
            '-': self.model.subtract,
            '×': self.model.multiply,
            '÷': self.model.divide,
            '^': self.model.power,
            '%': self.model.percentage
        }
        
        try:
            if operator in operation_map:
                result = operation_map[operator](a, b)
                if isinstance(result, str) and result.startswith("Error"):
                    return result
                
                expr = f"{a} {operator} {b}"
                self.history.add_entry(operator, expr, str(result), 'basic')
                return str(result)
            else:
                return "❌ Error: Invalid operation"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def perform_unary_operation(self, value: float, operation: str) -> str:
        """Perform unary operations (one operand)"""
        operation_map = {
            'sqrt': self.model.square_root,
            'sin': lambda x: self.model.sine(x, True),
            'cos': lambda x: self.model.cosine(x, True),
            'tan': lambda x: self.model.tangent(x, True),
            'ln': self.model.natural_log,
            'log10': lambda x: self.model.logarithm(x, 10),
            'factorial': self.model.factorial,
            '1/x': lambda x: 1/x if x != 0 else "Error: Division by zero"
        }
        
        try:
            if operation in operation_map:
                result = operation_map[operation](value)
                if isinstance(result, str) and result.startswith("Error"):
                    return result
                self.history.add_entry(operation, f"{operation}({value})", str(result), 'unary')
                return str(result)
            else:
                return "❌ Error: Unknown operation"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def get_history(self, limit: Optional[int] = None) -> list:
        """Get calculation history"""
        return self.history.get_history(limit)
    
    def clear_history(self) -> None:
        """Clear history"""
        self.history.clear_history()
    
    def search_history(self, query: str) -> list:
        """Search history"""
        return self.history.search_history(query)
    
    def get_ai_insights(self) -> str:
        """Get AI insights from calculation history"""
        return self.ai_assistant.get_insights(self.history.get_history())
    
    def get_ai_suggestions(self, current_input: str) -> List[str]:
        """Get AI suggestions for current input"""
        return self.ai_assistant.smart_suggest(
            current_input, 
            self.history.get_history()
        )
    
    def memory_store(self, value: float) -> None:
        """Store value in memory"""
        self.model.memory_store(value)
    
    def memory_recall(self) -> float:
        """Recall value from memory"""
        return self.model.memory_recall()
    
    def memory_clear(self) -> None:
        """Clear memory"""
        self.model.memory_clear()
    
    def memory_add(self, value: float) -> None:
        """Add to memory"""
        current_memory = self.model.memory_recall()
        self.model.memory_store(current_memory + value)
