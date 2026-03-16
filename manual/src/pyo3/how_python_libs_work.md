# How Python Libraries Work

When you type `import mymodule` in Python, Python searches your `sys.path` for a module of that
name. Either a Python module, or a `mymodule.so` file (`.dll` on Windows). It uses `dlopen()`
(or whatever the Win64 equivalent is) and looks for the symbol `PyInit_mymodule`. The symbol
name must match the module name.

The module itself must export `PyMODINIT_FUNC PyInit_mymodule(void)` - which returns a pointer to
a `PyObject`. So a relatively small C program is enough to make a Python module:

```c
#include <Python.h>

static PyObject* hello_func(PyObject* self, PyObject* args) {
    printf("Hello from C!\n");
    Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
    {"hello", hello_func, METH_NOARGS, "Say hello"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "mymodule",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_mymodule(void) {
    return PyModule_Create(&module);
}
```

Honestly, not too bad - as long as you like jumping from Python to C.

C++ actually makes it a bit easier - once you figure out how to install Boost:

```cpp
#include <boost/python.hpp>

int add(int a, int b) {
    return a + b;
}

BOOST_PYTHON_MODULE(mymodule)
{
    using namespace boost::python;
    def("add", add);
}
```

We've ignored the plumbing that typically goes with C and C++ (Makefiles, CMake, dependency
management and so on). But it's a testament to Python's design that you can make modules for
it so easily - and it was one of the original design objectives. Python is a glue language.
