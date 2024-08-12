from flask_app import create_app


application = create_app()

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080, debug=True)


#references -> https://www.youtube.com/watch?v=7LNl2JlZKHA
#access key update
