from flask import Flask, render_template, request
import compress_pickle
import numpy as np



app = Flask(__name__)

# Load the model
popular_df = compress_pickle.load('model.pkl.gz')
similarity_scores = compress_pickle.load('similarity.pkl.gz')
pt = compress_pickle.load('pt.pkl.gz')
books = compress_pickle.load('books.pkl.gz')



@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author =  list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_rating'].values),
                        )





@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html', book_titles=list(pt.index))


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    distances = similarity_scores[index]
    similar_items = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    
    return render_template('recommend.html', data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)