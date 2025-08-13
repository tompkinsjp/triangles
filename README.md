# Tompkins Triangle Generator

This Python script generates and visualizes Tompkins Triangles for a given polygonal order `k` and maximum number of rows `n`.

## Features
- **Custom Polygonal Order (`k`)**: Specify the polygonal order for the triangle.
- **Custom Number of Rows (`n`)**: Choose how many rows of the triangle to display.
- **Highlighting**: Optionally highlight a specific value in the triangle.
- **Adjustable Padding**: Optimized figure layout for readability in PNG output.

## Requirements
- Python 3.7+
- matplotlib
- numpy

Install the dependencies using:
```bash
pip install matplotlib numpy
```

## Usage
Run the script from the command line:
```bash
python tompkins_triangle.py --k 4 --n 8
```

### Options
- `--k` (int): Polygonal order (e.g., 4 for squares, 3 for triangles).
- `--n` (int): Number of rows to generate.
- `--highlight` (int, optional): Value to highlight in the triangle.

Example with highlighting:
```bash
python tompkins_triangle.py --k 4 --n 8 --highlight 25
```

## Output
The script saves the generated triangle as a PNG file:
```
tompkins_triangle_k{k}_n{n}.png
```

## License
This project is released under the MIT License.
