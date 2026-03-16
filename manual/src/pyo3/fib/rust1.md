# Let's Port that to Rust

So the Rust version is pretty similar:

```rust
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
```

I've actually spread it out a little, so we have a callable API and an internal function.

So we'll build that with `maturin develop`, and look at `fib_rs.py`:

```python3
#/usr/bin/python3
import time
from scratchpad import recur_fibo

print("Single thread")
results = []
t0 = time.time()
for i in range(40):
    results.append(recur_fibo(i))
t1 = time.time()
print(results)
print("Time: ", t1-t0)
```

And let's give it a run:

```
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$ python3 ./fib_rs.py 
Single thread
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155]
Time:  0.9770832061767578
```

So that's an improvement from about 11.5 seconds to about 0.9 seconds. Not bad!
