import unittest
from library_mixed import *

class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.library.add_user("Gregor")
        self.library.add_user("Krto")
        self.library.add_user("Miso")
        self.library.add_book("Book 1")
        self.library.add_book("Book 1")
        self.library.add_book("Book 2")
        self.library.add_book("Book 3")

    def test_add_user(self):
        self.assertTrue(self.library.add_user("Jano"))
        self.assertFalse(self.library.add_user("Jano"))
        self.assertTrue(self.library.add_user("Martin"))

    def test_reserve_book(self):
        self.assertTrue(self.library.reserve_book("Gregor", "Book 3", 1, 5))
        self.assertFalse(self.library.reserve_book("Krto", "Book 3", 2, 3))
        self.assertFalse(self.library.reserve_book("Gregor", "Book 1", 7, 6))
        self.assertFalse(self.library.reserve_book("Ivica", "Book 1", 8, 9))
        self.assertTrue(self.library.reserve_book("Miso", "Book 1", 10, 15))
        self.assertTrue(self.library.reserve_book("Krto", "Book 1", 11, 15))

    def test_check_reservation(self):
        self.assertFalse(self.library.check_reservation("Krto", "Book 1", 17))
        self.library.reserve_book("Krto", "Book 1", 16, 18)
        self.assertTrue(self.library.check_reservation("Krto", "Book 1", 17))

    def test_change_reservation(self):
        self.library.reserve_book("Krto", "Book 1", 16, 18)
        self.assertTrue(self.library.check_reservation("Krto", "Book 1", 16))
        self.assertFalse(self.library.check_reservation("Miso", "Book 1", 16))
        self.library.change_reservation("Krto", "Book 1", 16, "Miso")
        self.assertFalse(self.library.check_reservation("Krto", "Book 1", 16))
        self.assertTrue(self.library.check_reservation("Miso", "Book 1", 16))

class ReservationTestCase(unittest.TestCase):
    def setUp(self):
        self.reservation1 = Reservation(1, 7, "Book 1", "Jano")
        self.reservation2 = Reservation(2, 7, "Book 1", "Gregor")
        self.reservation3 = Reservation(8, 9, "Book 2", "Miso")
        self.reservation4 = Reservation(8, 9, "Book 1", "Krto")

    def test_overlapping(self):
        self.assertTrue(self.reservation1.overlapping(self.reservation2))
        self.assertFalse(self.reservation1.overlapping(self.reservation3))
        self.assertFalse(self.reservation1.overlapping(self.reservation4))

    def test_includes(self):
        self.assertTrue(self.reservation1.includes(3))
        self.assertFalse(self.reservation1.includes(9))

    def test_identify(self):
        self.assertTrue(self.reservation4.identify(8, "Book 1", "Krto"))
        self.assertFalse(self.reservation4.identify(11, "Book 1", "Krto"))
        self.assertFalse(self.reservation4.identify(8, "Book 1", "Ivica"))
        self.assertFalse(self.reservation4.identify(8, "Book 3", "Krto"))

    def test_change_for(self):
        self.assertTrue(self.reservation4.identify(8, "Book 1", "Krto"))
        self.reservation4.change_for("Miro")
        self.assertFalse(self.reservation4.identify(8, "Book 1", "Krto"))
        self.assertTrue(self.reservation4.identify(8, "Book 1", "Miro"))

class MessagesTestCase(unittest.TestCase):
    def setUp(self):
        self.msg_creator = MsgCreator()

    def test_lib_created(self):
        self.assertEqual(self.msg_creator.get_msg(LIB_CREATED), F'Library created.')

    def test_user_exists(self):
        name = F'Gregor'
        self.assertEqual(self.msg_creator.get_msg(USER_EXISTS, name = name), F'User not created, user with name {name} already exists.')

    def test_res_wrong_date(self):
        book = F'Book 1'
        user = F'Krto'
        date_from = F'1'
        date_to = F'8'
        self.assertEqual(self.msg_creator.get_msg(RES_WRONG_DATE, book = book, user = user, date_from = date_from, date_to = date_to),
                         F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. Incorrect dates.')

    def test_res_exists(self):
        book = F'Book 1'
        user = F'Jano'
        date = '6'
        self.assertEqual(self.msg_creator.get_msg(RES_EXISTS, book = book, user = user, date = date),
                         F'Reservation for {user} of {book} on {date} exists.')

unittest.main()
