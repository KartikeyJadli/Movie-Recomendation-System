import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Funcyion to return index by taking movie names
def get_title_from_index(index):
    try: 
        return (df[df.index == index]["title"].values[0])
    except Exception as e:
        print("This movie name is not in our data set and check your spelling.\n ")
        exit(0)
# Function to return movies name by taking index
def get_index_from_title(title):
    try:
        return df[df.title == title]["index"].values[0]
    except Exception as e:
        print("This movie name is not in our data set and check your spelling.\n ")
        exit(0)
# Read CSV File
df = pd.read_csv("https://raw.githubusercontent.com/Diya-1/movie_recomendation/main/movie_dataset.csv")
#print df.columns

# Select Features by which we want to recommend mpovies 

features = ['keywords','cast','genres','director']


# Function to fill the missing values in our dataset
for feature in features:
	df[feature] = df[feature].fillna('')

# Create a column in DF which combines all selected features
def combine_features(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print ("Error:", row)	
df["combined_features"] = df.apply(combine_features,axis=1)

# To check the combine function 
#print("Combined Features:", df["combined_features"].head())

# Creating count matrix from this new combined column
cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])

# Compute the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix) 

# Taking the inputs from the user
movie_user_likes = input("Enter the name ofg movie by which you want to recommendation:")
movie_user_likes=movie_user_likes.title()
no_movies_recommend=int(input("Enter the number of movies you want to recommend: "))

# Get index of this movie from its title
movie_index = get_index_from_title(movie_user_likes)

# Creating the list of similar movies
similar_movies =  list(enumerate(cosine_sim[movie_index]))

# Get a list of similar movies in descending order of similarity score
sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

# Print titles of  movies
i=0
try:
    for element in sorted_similar_movies:
        print(get_title_from_index(element[0]))
        i=i+1
        if (i==no_movies_recommend):
            break
except Exception as e:
    print("We can recommend only these movies.\n")
print("\n\t\tTHANK YOU.")