from flask import Flask, render_template,g,request,redirect
import searcher
app = Flask(__name__)

@app.route('/',methods = ['GET'])
def show_search_results():
    if(request.args.get('search')):
        results = searcher.search(request.args.get('search'))
        return render_template('index.html',results = results,searchTerm = request.args.get('search'))
    else:
        return render_template('index.html')

@app.route('/article',methods = ['GET'])
def show_article():
    if(request.args.get('path')):
        with open(request.args.get('path') , 'r') as file:
            title = request.args.get('path').split("\\")[-1].replace('.txt', '')
            content = file.readlines()
            return render_template("article.html",article=content, title=title)
    else:
        return redirect(url_for("/"))


if __name__ == "__main__":
    app.run(debug=True)