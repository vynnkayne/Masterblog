from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load blog posts from the JSON file
def load_blog_posts():
    with open('blog_posts.json') as json_file:
        return json.load(json_file)

# Save blog posts to the JSON file
def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as json_file:
        json.dump(posts, json_file)

# Fetch a blog post by ID
def fetch_post_by_id(post_id):
    posts = load_blog_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

# Home page - Display all blog posts
@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

# Add a new blog post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        posts = load_blog_posts()
        post_id = len(posts) + 1

        new_post = {'id': post_id, 'author': author, 'title': title, 'content': content}
        posts.append(new_post)

        save_blog_posts(posts)

        return redirect(url_for('index'))

    return render_template('add.html')

# Delete a blog post
@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_blog_posts()
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            save_blog_posts(posts)
            break

    return redirect(url_for('index'))

# Update a blog post
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        save_blog_posts(load_blog_posts())

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)





