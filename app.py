from flask import Flask, jsonify, request, Response, json
from response_handler import response_handler, error_response_handler
from logger import *
from tokenHandler import tokenGenerator

app = Flask(__name__)

books = [
  {
    'id': 1,
    'name': 'opponet',
    'price': '$40',
    'range': 100
  },
  {
    'id': 2,
    'name': 'next ville',
    'price': '$200',
    'range': 10
  }
]

def find_book_by_id(id):
  return [book for book in books if book['id'] == id]

@app.route('/books')
def getBooks():
  if not bool(books):
    return error_response_handler('No books found', 404)
  return response_handler(books, 200, 'Book retrieved successfully')

@app.route('/books/<int:id>')
def getBookById(id):
  book = find_book_by_id(id)

  if not bool(book):
    return error_response_handler('Book not found', 404)
  response = response_handler(book[0], 200, 'Book retrieved successfully')
  response.headers['Location'] = '/books/' + str(id)
  return response


def validateBookObject(bookObject):
  errorObject = {}
  if ('name' not in bookObject):
    errorObject["name"] = 'Name is required'
  if ('range' not in bookObject):
    errorObject["Range"] = 'Range is required'
  if ('price' not in bookObject):
    errorObject["Price"] = 'Price is required'
  return errorObject

@app.route('/books', methods=['POST'])
def add_book():
  book_Object = request.get_json()
  validator = validateBookObject(book_Object)
  if not bool(validator):
    response = error_response_handler(validator, 400)
    return response
  else:
    new_book = {
      'id': books[-1]['id'] + 1,
      'name': book_Object['name'],
      'range': book_Object['range'],
      'price': book_Object['price']
    }
    books.append(new_book)
    response = response_handler(new_book, 201, 'Book added successfully')
    response.headers['Location'] = '/books/' + str(new_book['id'])
    return response

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
  book_object = request.get_json()
  retrieved_book = find_book_by_id(id)

  if (bool(retrieved_book) == False):
    return error_response_handler('Book not found', 404)

  book = retrieved_book[0]
  book['name'] = book_object['name'] or book['name']
  book['range'] = book_object['range'] or book['range']
  book['price'] = book_object['price'] or book['price']
  response = response_handler(book, 200, 'Book updated successfully')
  return response

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book_by_id(id):
  try:
    retrieved_book = find_book_by_id(id)

    if not bool(retrieved_book):
      return error_response_handler('Book not found', 404)

    book = retrieved_book[0]
    del books[books.index(book)]
    response = response_handler([], 200, 'Book deleted successfully')
    return response
  except:
    logging.exception('Error')
    return error_response_handler('An error occurred, unable to delete book', 500)

if __name__ == "__main__":
  app.run(port=4000, debug=True)