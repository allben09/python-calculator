"""
AI Professional Calculator - Main Entry Point
Upgraded from simple console calculator to AI-powered GUI
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.calculator_controller import CalculatorController
from views.calculator_view import CalculatorView

def main():
    """Main entry point - Replaces your console menu with GUI"""
    print("🤖 AI Professional Calculator")
    print("=" * 40)
    print("💡 Features:")
    print("  • Natural language processing (Ask AI)")
    print("  • Advanced math functions")
    print("  • History tracking")
    print("  • Memory operations (MC, MR, MS, M+)")
    print("  • Keyboard shortcuts")
    print("  • Professional GUI")
    print("=" * 40)
    print("🚀 Starting GUI...")
    
    try:
        controller = CalculatorController()
        view = CalculatorView(controller)
        view.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
