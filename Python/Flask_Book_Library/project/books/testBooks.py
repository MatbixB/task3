import unittest
from project import db, app
from project.books.models import Book

class TestBookModel(unittest.TestCase):
	
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
		
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
		
    def test_new_book(self):
        book = Book(name="Test Book", author="Test Author", year_published=2024, book_type="Fiction")
        db.session.add(book)
        db.session.commit()
        self.assertIsNotNone(book.id)
        self.assertEqual(book.name, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year_published, 2024)
        self.assertEqual(book.book_type, "Fiction")
        self.assertEqual(book.status, "available")
		
    def test_modify(self):
        book = Book(name="Test Book", author="Test Author", year_published=2024, book_type="Fiction")
        db.session.add(book)
        db.session.commit()
        book_to_update = Book.query.get(book.id)
        book_to_update.name = 'New Title'
        db.session.commit()
        self.assertEqual(book.name, 'New Title')
		
    def test_delete(self):
        book = Book(name="Test Book", author="Test Author", year_published=2024, book_type="Fiction")
        db.session.add(book)
        db.session.commit()
        db.session.delete(book)
        db.session.commit()
        self.assertIsNone(Book.query.get(book.id))
	
    def test_invalid_title(self):
        book = Book('', 'Author', 2024, 'Fiction')
        with self.assertRaises(Exception):
            db.session.add(book)
            db.session.commit()

    def test_invalid_author(self):
        book = Book('Title', '', 2000, 'Fiction')
        db.session.add(book)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_invalid_year(self):
        book = Book('Tytul', 'Autor', 'year: 2024', 'Fiction')
        db.session.add(book)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_invalid_type(self):
        book = Book('Tytul', 'Autor', 2024, None)
        with self.assertRaises(Exception):
            db.session.add(book)
            db.session.commit()

    def test_duplicate(self):
        book1 = Book('Title', 'Author', 2024, 'Fiction')
        book2 = Book('Title', 'Author', 2024, 'Fiction')
        with self.assertRaises(Exception):
            db.session.add(book1)
            db.session.add(book2)
            db.session.commit()

    def test_delete_nonexisting(self):
        book1 = Book('Title', 'Author', 2024, 'Fiction')
        book2 = Book('Title2', 'Author2', 2025, 'Fiction')
        db.session.add(book1)
        db.session.commit()
        with self.assertRaises(Exception):
            db.session.delete(book2)
            db.session.commit()
	
    def test_xss(self):
        book = Book('Title', '<script>alert("XSS");</script>', 2024, 'Fiction')
        db.session.add(book)
        db.session.commit()
        self.assertNotIn('<script>', book.author)
	
    def test_sqli(self):
        book = Book('Title', 'Author\'); DROP TABLE books; --', 2024, 'Fiction')
        db.session.add(book)
        db.session.commit()
        self.assertNotIn('DROP TABLE books', book.author)
		
    def test_long_title(self):
        book = Book('T' * 200, 'Author', 2024, 'Fiction')
        db.session.add(book)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_long_author(self):
        book = Book('Title', 'A' * 200, 2024, 'Fiction')
        db.session.add(book)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_big_year(self):
        book = Book('Tytul', 'Author', 20000000, 'Fiction')
        db.session.add(book)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_add_long_type(self):
        book = Book('Tytul', 'Author', 2000, 't' * 100)
        db.session.add(book)
        with self.assertRaises(Exception):
            db.session.commit()
        
if __name__ == '__main__':
    unittest.main()