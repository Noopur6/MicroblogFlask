'''
Created on Apr 16, 2019

@author: nsno
'''
import unittest
from app import microblogapp, db
from app.models import User, Post
from datetime import datetime, timedelta
class UserModelCase(unittest.TestCase):
    def setUp(self):
        microblogapp.config['SQLALCHEMY_DATABASE_URI']='sqlite://'
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.verify_password('dog'))
        self.assertTrue(u.verify_password('cat'))
        
    def test_avatar(self):
        u = User(username='john', email = 'john@example.com')
        self.assertEqual(u.avatar(128), 'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128')
        
    def test_follow(self):
        u1=User(username='john', email = 'john@gmail.com')
        u2=User(username='kate', email='kate@gmail.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])
        
        u1.follow(u2)
        db.session.commit()
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u1.followed.first().username, 'kate')
        self.assertEqual(u2.followers.first().username, 'john')
        
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)
        
    def test_show_posts(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='kate', email='kate@example.com')
        u3 = User(username='lily', email='lily@example.com')
        u4 = User(username='rolfe', email='rolfe@example.com')
        
        db.session.add_all([u1, u2, u3, u4])
        now = datetime.utcnow()
        p1 = Post(body="p1 post", author=u2, timestamp=now+timedelta(seconds=1))
        p2 = Post(body="p2 post", author=u4, timestamp=now+timedelta(seconds=2))
        p3 = Post(body="p3 post", author=u3, timestamp=now+timedelta(seconds=3))
        p4 = Post(body="p4 post", author=u1, timestamp=now+timedelta(seconds=4))
        
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()
        
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        u4.follow(u1)
        db.session.commit()
        
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        
        self.assertEqual(f1, [p4, p2, p1])
        self.assertEqual(f2, [p3, p1])
        self.assertEqual(f3, [p3, p2])
        self.assertEqual(f4, [p4, p2])
        
if __name__=='__main__':
    unittest.main(verbosity=2   )