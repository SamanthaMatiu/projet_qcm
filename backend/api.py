from app import app
from app import db, models
from flask_cors import CORS

CORS(app)

if __name__ == "__main__":
    db.create_all() 
    app.run(debug=True)
