import os
from unittest import TestCase
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Favorites

os.environ['DATABASE_URL'] = "postgresql:///park_info"
from app import app, CURR_USER_KEY
app.config['WTF_CSRF_ENABLED'] = False
db.create_all()

class UserFavoritesModelTestCase(TestCase):
    """Test views for favorites."""
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.testuser_id= 1234
        self.testuser= User.register("testing", "testing@test.com", "password")
        self.testuser.id= self.testuser_id
        db.session.commit()

        self.client = app.test_client()
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_favorites_model(self):
        """ Does favorites model work? """
        favorite = Favorites(
            parkcode="park",
            user_id=self.testuser.id)
        db.session.add(favorite)
        db.session.commit()

        self.assertEqual(len(self.testuser.favorites), 1)
        self.assertEqual(self.testuser.favorites[0].parkcode, "park")

class UserViewTestCase(TestCase):
    """Test views for users."""
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        u1 = User.register("test1", "email1@email.com", "password")
        uid1 = 123
        u1.id = uid1

        u2 = User.register("test2", "email2@email.com", "password")
        uid2 = 321
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        """ Clean up fouled transactions """
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.favorites), 0)

    def test_valid_signup(self):
        """Is the user information valid?"""
        u_test=User.register("test", "test@email.com", "password")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "test")
        self.assertEqual(u_test.email, "test@email.com")
        self.assertNotEqual(u_test.password, "password")
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.register(None, "test@test.com", "password")
        uid = 12345
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.register("test", None, "password")
        uid = 112233
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.register("test", "email@email.com", "")

        with self.assertRaises(ValueError) as context:
            User.register("test", "email@email.com", None)

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(self.u1.id, self.uid1)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

class parkinfoViewsTestCase(TestCase):
    """Tests for views of API."""

    def test_list_parkinfo(self):
        with app.test_client() as client:
            resp = client.get("/parkinfo/gero")
            self.assertEqual(resp.status_code, 200)

    def test_park_favorite(self):
        with app.test_client() as client:
            resp = client.post("/park/lecl/addfavoritepark")
            self.assertEqual(resp.status_code, 302)

    def test_statepark_info(self):
        with app.test_client() as client:
            resp = client.get("/parks/state/NJ")
            self.assertEqual(resp.status_code, 200)
