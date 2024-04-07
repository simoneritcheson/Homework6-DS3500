import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("preprocessed_data.csv")

## Define sentiment words

# Love
love_words = ["love", "joy", "enchanting", "captivating", "beautiful", "romance", "happiness", "healing", "connection",
              "adventure", "shiny", "sweet", "nice", "light", "blue", "lightblue", "yellow", "pink", "gold", "green",
              "purple", "courage", "faith", "passion", "amazing", "new", "wonderful"]

# Heartbreak
heartbreak_words = ["upset", "wait", "hate", "dislike", "scared", "angry", "confused", "stupid", "fear", "sadness",
                    "doubts", "doubt", "hurt", "pain", "heartbreak", "dark", "tragic", "lonely", "loneliness",
                    "loathing", "devastating", "devastated", "solitary", "cry", "cold", "tears", "teardrops",
                    "turmoil", "demons", "terror", "terrors", "black", "reputation", "brown", "darkgreen", "grey",
                    "loss", "bye"]

# Optimism
optimism_words = ["finally", "relief", "hope", "dreams", "wonderment", "wonder", "wonderful", "smile", "intrigue",
                  "happy", "sunshine", "bright", "uplifting", "positive", "cheerful", "optimistic", "inspiration",
                  "excitement", "vibrant"]

# Anger
anger_words = ["angry", "hate", "mad", "outraged", "resentment", "fury", "dislike", "bad", "unsafe", "gross",
               "loathing", "loathe", "goodbye", "liar", "lies", "lie", "rage", "bitter", "hostile", "vindictive",
               "outrageous", "provoked", "enraged", "irritated", "furious", "infuriated"]

# Reflection
reflection_words = ["loss", "bye", "enchanting", "demons", "terror", "terrors", "black", "reputation", "brown",
                    "darkgreen", "grey", "memories", "nostalgia", "contemplate", "introspection", "ponder",
                    "reminisce", "meditate", "introspective", "thoughtful", "reflective"]


## Define sentiment analysis function to calculate percentages

def calculate_sentiment_percentages(text):
    words = text.lower().split()
    total_count = len(words)

    love_count = sum(word in love_words for word in words)
    heartbreak_count = sum(word in heartbreak_words for word in words)
    optimism_count = sum(word in optimism_words for word in words)
    anger_count = sum(word in anger_words for word in words)
    reflection_count = sum(word in reflection_words for word in words)

    love_percentage = love_count / total_count * 100
    heartbreak_percentage = heartbreak_count / total_count * 100
    optimism_percentage = optimism_count / total_count * 100
    anger_percentage = anger_count / total_count * 100
    reflection_percentage = reflection_count / total_count * 100

    return love_percentage, heartbreak_percentage, optimism_percentage, anger_percentage, reflection_percentage


# Apply sentiment analysis to the prologue text
df['Love'], df['Heartbreak'], df['Optimism'], df['Anger'], df['Reflection'] = zip(
    *df['Prologue Text'].apply(calculate_sentiment_percentages))

# Normalize percentages so each sentiment category's bar extends to the same height (representing 100%)
df['Total'] = df['Love'] + df['Heartbreak'] + df['Optimism'] + df['Anger'] + df['Reflection']
df['Love'] /= df['Total'] / 100
df['Heartbreak'] /= df['Total'] / 100
df['Optimism'] /= df['Total'] / 100
df['Anger'] /= df['Total'] / 100
df['Reflection'] /= df['Total'] / 100

# Create a stacked bar plot
barWidth = 0.85
plt.figure(figsize=(10, 6))

# Set position of bar on Y axis
r = range(len(df))

# Make the plot
plt.barh(r, df['Love'], color='pink', edgecolor='white', height=barWidth, label='Love')
plt.barh(r, df['Heartbreak'], left=df['Love'], color='blue', edgecolor='white', height=barWidth, label='Heartbreak')
plt.barh(r, df['Optimism'], left=[i + j for i, j in zip(df['Love'], df['Heartbreak'])], color='lightblue',
        edgecolor='white', height=barWidth, label='Optimism')
plt.barh(r, df['Anger'], left=[i + j + k for i, j, k in zip(df['Love'], df['Heartbreak'], df['Optimism'])],
        color='red', edgecolor='white', height=barWidth, label='Anger')
plt.barh(r, df['Reflection'],
        left=[i + j + k + l for i, j, k, l in zip(df['Love'], df['Heartbreak'], df['Optimism'], df['Anger'])],
        color='limegreen', edgecolor='white', height=barWidth, label='Reflection')

# Add yticks on the middle of the group bars
plt.ylabel('Albums', fontweight='bold')
plt.xlabel('Sentiment Percentage', fontweight='bold')
plt.yticks([r for r in range(len(df))], df['Album Name'])
plt.title('Sentiment Percentage Distribution by Album')
plt.legend()

# Hide the percentages on the plot
plt.gca().axes.xaxis.set_visible(False)

# Show plot
plt.show()
