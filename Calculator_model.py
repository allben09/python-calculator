"""
Calculator Model - Core Business Logic
Enhanced with advanced mathematical functions
"""
import math
import statistics
from typing import Union, List, Optional

class CalculatorModel:
    """Advanced calculator with mathematical operations"""
    
    def __init__(self):
        self.memory = 0.0
        self.last_result = 0.0
        
    # Basic operations (from your original code)
    def add(self, a: float, b: float) -> float:
        """Addition"""
        self.last_result = a + b
        return self.last_result
    
    def subtract(self, a: float, b: float) -> float:
        """Subtraction"""
        self.last_result = a - b
        return self.last_result
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplication"""
        self.last_result = a * b
        return self.last_result
    
    def divide(self, a: float, b: float) -> Union[float, str]:
        """Division with zero check"""
        if b == 0:
            return "Error: Division by zero"
        self.last_result = a / b
        return self.last_result
    
    # Advanced operations (NEW)
    def power(self, base: float, exponent: float) -> float:
        """Power operation"""
        self.last_result = base ** exponent
        return self.last_result
    
    def square_root(self, a: float) -> Union[float, str]:
        """Square root with negative check"""
        if a < 0:
            return "Error: Negative square root"
        self.last_result = math.sqrt(a)
        return self.last_result
    
    def percentage(self, value: float, percent: float) -> float:
        """Percentage calculation"""
        self.last_result = (value * percent) / 100
        return self.last_result
    
    def logarithm(self, a: float, base: float = 10) -> Union[float, str]:
        """Logarithm calculation"""
        if a <= 0:
            return "Error: Logarithm of non-positive number"
        if base <= 0 or base == 1:
            return "Error: Invalid logarithm base"
        self.last_result = math.log(a, base)
        return self.last_result
    
    def natural_log(self, a: float) -> Union[float, str]:
        """Natural logarithm"""
        if a <= 0:
            return "Error: Natural log of non-positive number"
        self.last_result = math.log(a)
        return self.last_result
    
    def factorial(self, n: int) -> Union[int, str]:
        """Factorial calculation"""
        if n < 0 or n > 170:
            return "Error: Invalid factorial input"
        self.last_result = math.factorial(n)
        return self.last_result
    
    def sine(self, a: float, degrees: bool = False) -> float:
        """Sine function"""
        if degrees:
            a = math.radians(a)
        self.last_result = math.sin(a)
        return self.last_result
    
    def cosine(self, a: float, degrees: bool = False) -> float:
        """Cosine function"""
        if degrees:
            a = math.radians(a)
        self.last_result = math.cos(a)
        return self.last_result
    
    def tangent(self, a: float, degrees: bool = False) -> Union[float, str]:
        """Tangent function"""
        if degrees:
            a = math.radians(a)
        if math.cos(a) == 0:
            return "Error: Tangent undefined"
        self.last_result = math.tan(a)
        return self.last_result
    
    def mean(self, numbers: List[float]) -> float:
        """Mean (average) of numbers"""
        self.last_result = statistics.mean(numbers)
        return self.last_result
    
    def median(self, numbers: List[float]) -> float:
        """Median of numbers"""
        self.last_result = statistics.median(numbers)
        return self.last_result
    
    def standard_deviation(self, numbers: List[float]) -> float:
        """Standard deviation"""
        self.last_result = statistics.stdev(numbers) if len(numbers) > 1 else 0
        return self.last_result
    
    # Memory operations
    def memory_store(self, value: float):
        """Store value in memory"""
        self.memory = value
    
    def memory_recall(self) -> float:
        """Recall value from memory"""
        return self.memory
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0.0
    
    def memory_add(self, value: float):
        """Add to memory"""
        self.memory += value
    
    def get_last_result(self) -> float:
        """Get last calculated result"""
        return self.last_result
