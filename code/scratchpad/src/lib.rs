use pyo3::prelude::*;

#[pyclass]
struct Counter {
    #[pyo3(get)]
    count: usize,
}

#[pymethods]
impl Counter {
    #[new]
    fn new(count: usize) -> Self {
        Self { count }
    }

    fn increment(&mut self) {
        self.count += 1;
    }

    fn add(&mut self, amount: usize) {
        self.count += amount;
    }

    fn __repr__(&self) -> String {
        format!("Counter(count={})", self.count)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
mod scratchpad {
    #[pymodule_export]
    use super::Counter;

    use pyo3::exceptions::PyArithmeticError;
    use pyo3::prelude::*;

    /// Formats the sum of two numbers as string.
    #[pyfunction]
    fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
        Ok((a + b).to_string())
    }

    #[pyfunction]
    fn hello_rust() -> PyResult<()> {
        println!("Hello World from Rust");
        Ok(())
    }

    #[pyfunction]
    fn divide(a: i32, b: i32) -> PyResult<i32> {
        if b == 0 {
            Err(PyArithmeticError::new_err(
                "Dividing by zero will ruin your day",
            ))
        } else {
            Ok(a / b)
        }
    }

    #[pyfunction]
    fn vectors(v: Vec<i32>) -> PyResult<Vec<i32>> {
        Ok(v.into_iter().map(|n| n * 2).collect())
    }

    use std::collections::HashMap;
    #[pyfunction]
    fn mappy(m: HashMap<String, String>) {
        println!("{m:?}");
    }

    fn fibo(n: u64) -> u64 {
        match n {
            0 => 1,
            1 => 1,
            _ => fibo(n - 1) + fibo(n - 2),
        }
    }

    #[pyfunction]
    fn recur_fibo(n: u64) -> PyResult<u64> {
        Ok(fibo(n))
    }

    #[pyfunction]
    fn par_fibo(max: u64) -> PyResult<Vec<u64>> {
        use rayon::prelude::*;
        let result = (1..max)
            .into_par_iter()
            .map(|n| fibo(n))
            .collect::<Vec<u64>>();
        Ok(result)
    }
}
