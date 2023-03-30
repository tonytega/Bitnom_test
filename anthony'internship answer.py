from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from collections import Counter

# Load the HTML table containing the colors of dresses worn by Bincom staffs
with open("C:\\Users\\DELL\\Desktop\\python_class_question.html.html") as f:
    html = f.read()

# Parse the HTML table using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
table = soup.find("table")

# Extract the data from the table and store it in a pandas dataframe
data = []
for row in table.find_all("tr")[1:]:
    day, colors = [cell.get_text(strip=True) for cell in row.find_all("td")]
    colors = colors.split(", ")
    data.append((day, colors))
df = pd.DataFrame(data, columns=["Day", "Colors"])

# 1. Which color of shirt is the mean color?
all_colors = [color for colors in df["Colors"] for color in colors]
mean_color = Counter(all_colors).most_common(1)[0][0]
print("The mean color is:", mean_color)

# 2. Which color is mostly worn throughout the week?
most_common_color = Counter(all_colors).most_common(1)[0][0]
print("The color that was mostly worn throughout the week is:", most_common_color)

# 3. Which color is the median?
all_colors.sort()
n = len(all_colors)
if n % 2 == 0:
    median_color = all_colors[n//2 - 1]
else:
    median_color = all_colors[n//2]
print("The median color is:", median_color)

# 4. BONUS: Get the variance of the colors
colors_counts = Counter(all_colors)
variance = sum([(count - len(all_colors)/len(colors_counts))**2 for count in colors_counts.values()]) / len(colors_counts)
print("The variance of the colors is:", variance)

# 5. BONUS: If a color is chosen at random, what is the probability that the color is red?
total_colors = sum(colors_counts.values())
red_count = colors_counts.get("RED", 0)
red_probability = red_count / total_colors
print("The probability that the color is red is:", red_probability)

# 6. Save the colours and their frequencies in postgresql database
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_user",
    password="your_password"
)
cursor = conn.cursor()
for color, count in colors_counts.items():
    cursor.execute("INSERT INTO colors (color, count) VALUES (%s, %s)", (color, count))
conn.commit()
cursor.close()
conn.close()

# 7. BONUS: Write a recursive searching algorithm to search for a number entered by user in a list of numbers.
def recursive_search(numbers, target):
    if not numbers:
        return False
    elif numbers[0] == target:
        return True
    else:
        return recursive_search(numbers[1:], target)

# 8. Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.
import random
binary_digits = [str(random.randint(0, 1)) for _ in range(4)]
binary_string = "".join(binary_digits)
decimal_number = int(binary_string, 2)
print("The randomly generated binary number is:", binary_string)
print("Its decimal equivalent is:", decimal_number)

# 9. Write a program to sum the first 50 fibonacci sequence
def fibonacci(n):
    if n == 0:
        return 0