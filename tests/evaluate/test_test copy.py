```python
import os
import importlib.util
import pytest

# Dynamically load the module from the file "evaluate/test copy.py"
module_path = os.path.join("evaluate", "test copy.py")
spec = importlib.util.spec_from_file_location("test_copy_module", module_path)
test_copy_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_copy_module)

# Import functions from the dynamically loaded module
add_numbers = test_copy_module.add_numbers
subtract_numbers = test_copy_module.subtract_numbers
multiply_numbers = test_copy_module.multiply_numbers
divide_numbers = test_copy_module