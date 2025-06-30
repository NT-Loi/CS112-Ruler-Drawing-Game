# Ruler Drawing Game - A "Divide and Conquer" Visualization

## Introduction
**Ruler Drawing Game** is an interactive Python application built with **Pygame** that visually demonstrates the **"Divide and Conquer"** algorithm through the classic *ruler marking problem*. 

Users can choose from multiple ruler types, customize visual styles and parameters, and watch as the program recursively draws tick marks step-by-step.

> 🏫 This project is the bonus assignment for the _"Design and Analysis of Algorithms"_ course (CS112.P22), carried out under the supervision of **PhD. Huynh Thi Thanh Thuong**.

### Member
|#|Full Name|Student ID|
|:-:|:-:|:-:|
|1|[Nguyễn Thắng Lợi](https://github.com/NT-Loi)|23520872|
---

## 🧠 Key Features

- 🎮 **Interactive GUI**: Clean and user-friendly interface using Pygame.
- 📐 **Multiple Ruler Types**: Straight Ruler, Triangle Square, and Protractor.
- 🎨 **Customizable Colors**: Choose your own color and see a live preview on the icons.
- 🔢 **Configurable Parameters**: Adjust ruler length and recursion depth (h).
- ✏️ **Animated Drawing**: Watch the recursive "Divide and Conquer" algorithm in real-time.
- 👁 **Visual Icons**: Custom-drawn intuitive icons for each ruler type.
- 🧑‍🏫 **Educational Value**: Ideal for teaching recursive thinking and algorithm visualization.

---

## 📸 Screenshots

<table>
<tr>
<td align="center"><b>Selection Screen</b></td>
<td align="center"><b>Input Screen</b></td>
<td align="center"><b>Drawing Result</b></td>
</tr>
<tr>
<td><img src="assets\selection_screen.png" alt="Selection Screen" width="400"></td>
<td><img src="assets\input_screen.png" alt="Input Screen" width="400"></td>
<td><img src="assets\drawing_result.png" alt="Drawing Result" width="400"></td>
</tr>
</table>

---

## ⚙️ Requirements

- Python 3.10+

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```sh
git clone https://github.com/NT-Loi/CS112-Ruler-Drawing-Game.git
cd CS112-Ruler-Drawing-Game
```

### 2. Intall Dependencies

```sh
pip install -r requirements.txt
```


### 3. Run the Application
```sh
python ruler_drawing.py
```

---

## 🕹️ How to Use

1. Start the program to view the selection screen.

2. Select a **Ruler Type**: Click on the icon of your choice.

3. Choose a **Color**: Click on a color swatch to preview it on the icons.

4. Click **Continue**.

5. Set **Parameters**: Enter the ruler length and number of recursion levels.

6. Click **Draw** to start the animated ruler drawing.

7. Click **Draw Again** to try different settings.

---

## 🔍 Algorithm Overview: Divide and Conquer

This project applies the classic **"Divide and Conquer"** method to draw ruler tick marks:

- **Divide:** Split the current segment by finding its midpoint.

- **Conquer:** Draw a tick mark at the midpoint. The height is based on the current recursion level.

- **Combine:** Recursively apply the same logic to the left and right halves, reducing the level by 1 each time.

- **Base Case:** The recursion ends when the level reaches 0.

This elegant method ensures a perfectly marked ruler using a simple, recursive structure.

---

## 📄 License
This project is for academic purposes only. Contact the authors for reuse permissions.

---

## 🤝 Contributions
Feel free to fork the project and open a pull request if you'd like to contribute new features or improvements!

---