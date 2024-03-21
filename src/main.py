import connection
import querys
import matplotlib.pyplot as plt

cursor = connection.connection.cursor()

streamingAction = querys.streamingAction()
streamingType = querys.streamingType()
topActors = querys.topActors()

cursor.execute(streamingAction)
results = cursor.fetchall()

for row in results:
    x = [row[0] for row in results]
    y = [row[1] for row in results]

#Grafica de barras
plt.title('Content Count by Streaming Platform for Action Genre')
plt.xlabel('Streaming Platform')
plt.ylabel('Content Count')
plt.bar(x, y)
#plt.show()

cursor.execute(streamingType)
results = cursor.fetchall()

for row in results:
    x = [row[0] for row in results]
    y = [row[1] for row in results]
    z = [row[2] for row in results]

# Create a bar plot with custom width for each bar
bar_width = 0.35  # Adjust width as needed
index = range(len(x))  # Define x-axis positions

# Create bars for series and movies with different positions
plt.bar(index, y, bar_width, label='Shows')
plt.bar([p + bar_width for p in index], z, bar_width, label='Movies')

# Set labels and title
plt.xlabel('Streaming Platform')
plt.ylabel('Content Count')
plt.title('Distribution of Shows and Movies on Streaming Platforms')

# Add labels and legend
plt.xticks([i + bar_width / 2 for i in index], x, rotation=45)  # Rotate x-axis labels for readability
plt.legend()

# Show the graph
plt.tight_layout()
#plt.show()

cursor.execute(topActors)
results = cursor.fetchall()

for row in results:
    print(row)
    #x = [row[0] for row in results]
    #y = [row[1] for row in results]