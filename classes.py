# # Function to register child classes
# def register_child(cls):
#     # Check if the class has 'class_id' and register it
#     if hasattr(cls, 'class_id'):
#         Parent.child_classes[cls.class_id] = cls
#     return cls  # Return the class object

# # Parent class with dictionary to store child class references
# class Parent:
#     child_classes = {}

#     @classmethod
#     def create_instance(cls, class_id, *args, **kwargs):
#         # Create instance of the child class based on the class_id
#         if class_id in cls.child_classes:
#             return cls.child_classes[class_id](*args, **kwargs)
#         else:
#             raise ValueError(f"No child class registered with ID '{class_id}'")

# # Child classes with unique class_ids, automatically registered using the decorator
# @register_child
# class Child1(Parent):
#     class_id = 'child1'
    
#     def __init__(self, *args, **kwargs):
#         print("Child1 instance created with args:", args, "and kwargs:", kwargs)

# @register_child
# class Child2(Parent):
#     class_id = 'child2'
    
#     def __init__(self, *args, **kwargs):
#         print("Child2 instance created with args:", args, "and kwargs:", kwargs)

# # Automatically registered
# print("Registered child classes:", Parent.child_classes)

# # Creating instances using class IDs
# instance1 = Parent.create_instance('child1', 1, 2, 3, key="value")
# instance2 = Parent.create_instance('child2', "hello", world=True)

class Parent():
    def __init__(self, alias, *args, **kwargs):
        print(self.__class__.child_static, alias)
        print("Parent instance created with args:", args, "and kwargs:", kwargs)

class Child(Parent):
    child_static = "sdfsdfsdfsdfsdfsdfsdfsdf"
    def __init__(self, alias, *args, **kwargs):
        super().__init__(alias, *args, **kwargs)
        print("Child instance created with alias:", alias)

child = Child("My Child")
print("--------------------------------")

def function(a, b, **kwargs):
    print(a, b)

mydict = {'a': 100, 'b': 200, 'h': 300}

mydict2 = {'a': 150, 'b': 250, 'h': 350}

function(**(mydict | mydict2))
#function(**mydict)