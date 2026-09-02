# Activation Functions

### Activation function reference <!-- tag:ml, relu, sigmoid, tanh, gelu, activation, nonlinearity, dead neurons, saturation, swish -->

| Function | Formula | Range | Notes |
|----------|---------|-------|-------|
| ReLU | `max(0, x)` | [0, ∞) | default for CNNs/MLPs; cheap, but units can die when stuck at x<0 |
| Leaky ReLU | `max(αx, x)`, α≈0.01 | (−∞, ∞) | fixes dying ReLU, keeps a small negative slope |
| PReLU | `max(αx, x)`, α learned | (−∞, ∞) | Leaky ReLU with α as a parameter |
| ELU | `x` if x>0 else `α(eˣ−1)` | (−α, ∞) | smooth at 0, pushes mean activation toward zero |
| GELU | `x·Φ(x)` | (−0.17, ∞) | standard in transformers (BERT, GPT) |
| SiLU / Swish | `x·σ(x)` | (−0.28, ∞) | smooth, often edges out ReLU on deeper nets |
| Sigmoid | `1/(1+e⁻ˣ)` | (0, 1) | saturates both ends; output layer for binary only |
| Tanh | `tanh(x)` | (−1, 1) | zero-centered sigmoid; still saturates |
| Softmax | `eˣⁱ/Σeˣʲ` | (0, 1), sums to 1 | multiclass output layer, not a hidden activation |

### Derivatives (what backprop actually uses) <!-- tag:ml, derivative, gradient, backprop, vanishing gradient -->

| Function | Derivative | Vanishing gradient risk |
|----------|------------|-------------------------|
| ReLU | `1` if x>0 else `0` | none for x>0; zero gradient below |
| Leaky ReLU | `1` if x>0 else `α` | none |
| Sigmoid | `σ(x)(1−σ(x))`, max 0.25 | high — gradient ≤ 0.25 everywhere |
| Tanh | `1 − tanh²(x)`, max 1.0 | moderate — better than sigmoid |
| GELU | smooth, no closed form used in practice | low |

### plot activation functions <!-- tag:matplotlib, tag:ml,image:activations.svg, activation, relu, sigmoid, compare -->
```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, 500)
acts = {
    "ReLU": np.maximum(0, x),
    "Leaky ReLU": np.where(x > 0, x, 0.1 * x),
    "Sigmoid": 1 / (1 + np.exp(-x)),
    "Tanh": np.tanh(x),
    "GELU": 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3))),
    "SiLU": x / (1 + np.exp(-x)),
}

fig, ax = plt.subplots(figsize=(7, 5))
for name, y in acts.items():
    ax.plot(x, y, label=name)
ax.axhline(0, color="black", lw=0.5)
ax.axvline(0, color="black", lw=0.5)
ax.set_ylim(-1.5, 3)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title("Activation functions")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

### activations in PyTorch <!-- tag:pytorch, relu, gelu, layer, module -->
```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),           # nn.LeakyReLU(0.01), nn.GELU(), nn.SiLU(), nn.Tanh()
    nn.Linear(256, 10),
)

# functional form, no module needed
import torch.nn.functional as F
h = F.relu(x)
```
