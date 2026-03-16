# We can do better - Rayon!

Rayon is a pretty handy Rust library. It spins up a thread pool (one thread per core),
each with work-stealing and a task pool. It's not async, but for CPU-bound tasks - it's
pretty great. It also has some really nice helpers to make iterator magic run in
parallel.

So we'll start by adding Rayon as a dependency:

```bash
cargo add rayon
```

Now let's add a Rayon version to `src/lib.rs`:

```rust
    #[pyfunction]
    fn par_fibo(max: u64) -> PyResult<Vec<u64>> {
        use rayon::prelude::*;
        let result = (1..max)
            .into_par_iter()
            .map(|n| fibo(n))
            .collect::<Vec<u64>>();
        Ok(result)
    }
```

And make `fibo_rayon.py`:

```python3
#/usr/bin/python3
import time
from scratchpad import par_fibo

print("Multi thread")
results = []
t0 = time.time()
results = par_fibo(40)
t1 = time.time()
print(results)
print("Time: ", t1-t0)
```

The results are quite nice:

```
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$ python3 fib_rayon.py 
Multi thread
[1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155]
Time:  0.3917417526245117
```
