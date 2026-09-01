## Plotting

### line plot <!-- plot, chart, graph, matplotlib, visualize, visualization -->
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, label="series")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Title")
ax.legend()
plt.tight_layout()
plt.savefig("plot.png", dpi=150)
plt.show()
```

### scatter plot <!-- plot, chart, scatter, matplotlib, visualize -->
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, alpha=0.7, s=20)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Title")
plt.tight_layout()
plt.show()
```

### multiple subplots <!-- plot, chart, subplot, grid, matplotlib -->
```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, y)
axes[0, 0].set_title("Top left")
axes[0, 1].scatter(x, y)
axes[0, 1].set_title("Top right")
plt.tight_layout()
plt.show()
```
