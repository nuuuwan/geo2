def rangef(start, end, step):
    n_steps = (int)(round(1.0 * (end - start) / step))
    for i in range(n_steps):
        yield start + i * step
