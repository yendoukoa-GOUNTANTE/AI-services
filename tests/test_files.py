import unittest
from app import app, db, User, File
import json
import os
import asyncio

# Wrapper for async tests
def async_test(f):
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

class FileStorageTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            self.user = User(username='testuser', api_key='testkey')
            db.session.add(self.user)
            db.session.commit()
            self.user_id = self.user.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_doc(self):
        response = self.app.post('/api/v1/files/create-doc',
                                 data=json.dumps({
                                     'filename': 'test.txt',
                                     'content': 'Hello AI',
                                     'file_type': 'document'
                                 }),
                                 content_type='application/json',
                                 headers={'X-API-Key': 'testkey'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['filename'], 'test.txt')

        # Verify in DB
        with app.app_context():
            file = db.session.get(File, data['id'])
            self.assertIsNotNone(file)
            self.assertEqual(file.content, 'Hello AI')

    def test_list_files(self):
        with app.app_context():
            f1 = File(user_id=self.user_id, filename='f1.txt', file_type='document', content='c1')
            f2 = File(user_id=self.user_id, filename='f2.txt', file_type='document', content='c2')
            db.session.add(f1)
            db.session.add(f2)
            db.session.commit()

        response = self.app.get('/api/v1/files', headers={'X-API-Key': 'testkey'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_delete_file(self):
        with app.app_context():
            f = File(user_id=self.user_id, filename='del.txt', file_type='document', content='del')
            db.session.add(f)
            db.session.commit()
            file_id = f.id

        response = self.app.delete(f'/api/v1/files/{file_id}', headers={'X-API-Key': 'testkey'})
        self.assertEqual(response.status_code, 200)

        with app.app_context():
            self.assertIsNone(db.session.get(File, file_id))

if __name__ == '__main__':
    unittest.main()
