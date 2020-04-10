from itertools import count
from constants import *

class MsgCreator:

    def get_msg(self, msg_type, **kwargs):
        switcher = {
            ID_WRONG_BOOK: F'Reservation {kwargs.get("_id")} reserves {kwargs.get("_book")} not {kwargs.get("book")}.',
            ID_WRONG_USER: F'Reservation {kwargs.get("_id")} is for {kwargs.get("_for")} not {kwargs.get("for_")}.',
            ID_WRONG_DATE: F'Reservation {kwargs.get("_id")} is from {kwargs.get("_from")} to {kwargs.get("_to")} ' +
                           F'which does not include {kwargs.get("date")}.',
            USER_EXISTS: F'User not created, user with name {kwargs.get("name")} already exists.',
            RES_WRONG_USER: F'We cannot reserve book {kwargs.get("book")} for {kwargs.get("user")} ' +
                            F'from {kwargs.get("date_from")} to {kwargs.get("date_to")}. User does not exist.',
            RES_WRONG_DATE: F'We cannot reserve book {kwargs.get("book")} for {kwargs.get("user")} from ' +
                            F'{kwargs.get("date_from")} to {kwargs.get("date_to")}. Incorrect dates.',
            RES_WRONG_BOOK: F'We cannot reserve book {kwargs.get("book")} for {kwargs.get("user")} from ' +
                            F'{kwargs.get("date_from")} to {kwargs.get("date_to")}. We do not have that book.',
            RES_NO_BOOKS: F'We cannot reserve book {kwargs.get("book")} for {kwargs.get("user")} from ' +
                          F'{kwargs.get("date_from")} to {kwargs.get("date_to")}. We do not have enough books.',
            RES_NOT_EXISTS: F'Reservation for {kwargs.get("user")} of {kwargs.get("book")} on ' +
                            F'{kwargs.get("date")} does not exist.',
            RES_USER_NOT_EXISTS: F'Cannot change the reservation as {kwargs.get("new_user")} does not exist.',
            INCL_DATE: F'Reservation {kwargs.get("_id")} includes {kwargs.get("date")}',
            NOT_INCL_DATE: F'Reservation {kwargs.get("_id")} does not include {kwargs.get("date")}',
            RES_OVERLAP: F'Reservations {kwargs.get("_id")} and {kwargs.get("other_id")} do overlap',
            RES_NOT_OVERLAP: F'Reservations {kwargs.get("_id")} and {kwargs.get("other_id")} do not overlap',
            RES_ID_VALID: F'Reservation {kwargs.get("_id")} is valid {kwargs.get("for_")} of ' +
                        F'{kwargs.get("book")} on {kwargs.get("date")}.',
            RES_CHG_FOR: F'Reservation for {kwargs.get("user")} of {kwargs.get("book")} on {kwargs.get("date")} ' +
                       F'changed to {kwargs.get("new_user")}.',
            USER_CREATED: F'User {kwargs.get("name")} created.',
            BOOK_ADDED: F'Book {kwargs.get("name")} added. We have {kwargs.get("_books")} coppies of the book.',
            RES_INCLUDED: F'Reservation {kwargs.get("desired_reservation_id")} included.',
            RES_EXISTS: F'Reservation for {kwargs.get("user")} of {kwargs.get("book")} on {kwargs.get("date")} exists.',
            RES_CHG_TO: F'Reservation for {kwargs.get("user")} of {kwargs.get("book")} on {kwargs.get("date")} ' +
                        F'changed to {kwargs.get("new_user")}.',
            LIB_CREATED: F'Library created.',
            RES_CREATED: F'Created a reservation with id {kwargs.get("_id")} of {kwargs.get("_book")} ' +
                        F'from {kwargs.get("_from")} to {kwargs.get("_to")} for {kwargs.get("_for")}.'
        }
        return switcher.get(msg_type)

class Logger:
    def write(self, issue_number, **kwargs):
        msg_creator = MsgCreator()
        print(msg_creator.get_msg(issue_number, **kwargs))

class Reservation(object):
    log = Logger()
    _ids = count(0)
    
    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to    
        self._book = book
        self._for = for_
        self._changes = 0
        self.log.write(RES_CREATED, _id = self._id, _book = book, _from = from_, _to = to, _for = for_)

    def overlapping(self, other):
        ret = (self._book == other._book and self._to >= other._from 
               and self._to >= other._from)

        if not ret:
            self.log.write(RES_NOT_OVERLAP, _id = self._id, other_id = other._id)
        self.log.write(RES_OVERLAP, _id = self._id, other_id = other._id)
        return ret
            
    def includes(self, date):
        ret = (self._from <= date <= self._to)
        if not ret:
            self.log.write(NOT_INCL_DATE, _id = self._id, date = date)
        self.log.write(INCL_DATE, _id = self._id, date = date)
        return ret        
        
    def identify(self, date, book, for_):
        if book != self._book:
            self.log.write(ID_WRONG_BOOK, _id = self._id, _book = self._book, book = book)
            return False
        if for_!=self._for:
            self.log.write(ID_WRONG_USER, _id = self._id, _for = self._for, for_ = for_)
            return False
        if not self.includes(date):
            self.log.write(ID_WRONG_DATE, _id = self._id, _from = self._from, _to = self._to, date = date)
            return False

        self.log.write(RES_ID_VALID, _id = self._id, for_ = for_, book = book, date = date)
        return True
        
    def change_for(self, for_):
        self.log.write(RES_CHG_FOR, _id = self._id, _for = self._for, for_ = for_)
        self._for = for_
        

class Library(object):
    log = Logger()

    def __init__(self):
        self._users = set()
        self._books = {}   #maps name to count
        self._reservations = [] #Reservations sorted by from
        self.log.write(LIB_CREATED)

    def add_user(self, name):
        if name in self._users:
            self.log.write(USER_EXISTS, name = name)
            return False
        self._users.add(name)
        self.log.write(USER_CREATED, name = name)
        return True

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1
        self.log.write(BOOK_ADDED, name = name, _books = self._books[name])

    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            self.log.write(RES_USER_NOT_EXISTS, book = book, user = user, date_from = date_from, date_to = date_to)
            return False
        if date_from > date_to:
            self.log.write(RES_WRONG_DATE, book = book, user = user, date_from = date_from, date_to = date_to)
            return False
        if book_count == 0:
            self.log.write(RES_WRONG_BOOK, book = book, user = user, date_from = date_from, date_to = date_to)
            return False
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        #we check that if we add this reservation then for every reservation record that starts 
        #between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    self.log.write(RES_NO_BOOKS, book = book, user = user, date_from = date_from, date_to = date_to)
                    return False
        self._reservations+=[desired_reservation]
        self._reservations.sort(key=lambda x:x._from) #to lazy to make a getter
        self.log.write(RES_INCLUDED, desired_reservation_id = desired_reservation._id)
        return True

    def check_reservation(self, user, book, date):
        res = any([res.identify(date, book, user) for res in self._reservations])
        if not res:
            self.log.write(RES_NOT_EXISTS, book = book, user = user, date = date)
        self.log.write(RES_EXISTS, book = book, user = user, date = date)
        return res

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations 
                                     if res.identify(date, book, user)]
        if not relevant_reservations:
            self.log.write(RES_NOT_EXISTS, book = book, user = user, date = date)
            return False
        if new_user not in self._users:
            self.log.write(RES_USER_NOT_EXISTS, new_user = new_user)
            return False

        self.log.write(RES_CHG_TO, book = book, user = user, date = date, new_user = new_user)
        relevant_reservations[0].change_for(new_user)
        return True
        
