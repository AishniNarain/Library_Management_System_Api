from app import Resource,ns
from flask import request
from issue_books.service import Issue_Books, email_observer
from issue_books.api_model import issuebooks_model


issue_books = Issue_Books()

# class Observer:
#     def update(self, message):
#         pass

# class SomeObserver(Observer):
#     def update(self, message):
#         # Process the updated data here
#         print("Message: ", message)
        
# Example usage:
# Create an instance of the issue books
issue_books_subject = Issue_Books()

# Attach observers
# some_observer = SomeObserver()
# issue_books_subject.attach(some_observer)

issue_books_subject.attach(email_observer)

@ns.route('/librarian/issue_books', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Issue(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.expect(issuebooks_model)
    def post(self):
        if request.method=='POST':
            return issue_books.issue_books(request.json)
        message = "This method is not allowed here please use the 'POST' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/librarian/return_book_request/<int:id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Initiate_Return_Request(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    def patch(self,id):
        if request.method=='PATCH':
            return issue_books.initiate_return_request(id)
        message = "This method is not allowed here please use the 'PATCH' method"
        return f"data="", error={True}, code='405', message={message}, details=''"

@ns.route('/librarian/return_book/<int:id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Return_Book(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    def patch(self,id):
        if request.method=='PATCH':
            return issue_books.return_book(id)
        message = "This method is not allowed here please use the 'PATCH' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/librarian/issued_books', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Issued_Book(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.doc(params={
        'page': {'in': 'query', 'description': 'Page no','type':'int', 'default': 1},
        'per_page': {'in': 'query', 'description': 'Per page details','type':'int', 'default': 5},
        'book_id': {'in': 'query', 'description': 'Id of the book','type':'int'},
        'issue_date': {'in': 'query', 'description': 'Issue date of the book','type':'string','format':'date'},
        'status': {'in': 'query', 'description': 'Status','type':'string'},
        'student_id': {'in': 'query', 'description': 'Id of the student','type':'int'}
    })
    def get(self):
        if request.method=='GET':
            page = request.args.get('page',type=int)
            per_page = request.args.get('per_page',type=int)
            book_id = request.args.get('book_id',type=int)
            issue_date = request.args.get('issue_date')
            status = request.args.get('status',type=str)
            student_id = request.args.get('student_id',type=int)
            return issue_books_subject.issued_details(page,per_page,book_id,issue_date,status,student_id)
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/librarian/all_students/issued_books', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class All_Students_Issued_Details(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.doc(params={
        'page': {'in': 'query', 'description': 'Page no','type':'int', 'default': 1},
        'per_page': {'in': 'query', 'description': 'Per page details','type':'int', 'default': 5},
        'issue_date': {'in': 'query', 'description': 'Issue date of the book','type':'string', 'format': 'date'},
        'status': {'in': 'query', 'description': 'Status','type':'string'},
        'student_id': {'in': 'query', 'description': 'Id of the student','type':'int'},
        'book_id': {'in': 'query', 'description': 'Id of the book','type':'int'},
        'issued_by': {'in': 'query', 'description': 'Book issuer','type':'int'}
    })
    def get(self):
        if request.method=='GET':
            page = request.args.get('page',type=int)
            per_page = request.args.get('per_page',type=int)
            issue_date = request.args.get('issue_date')
            status = request.args.get('status',type=str)
            student_id = request.args.get('student_id',type=int)
            book_id = request.args.get('book_id',type=int)
            issued_by = request.args.get('issued_by',type=int)
            return issue_books.get_all_students_issued_details(page,per_page,issue_date,status,student_id,book_id,issued_by)
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/issued_books/history', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Issued_Details_History(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.doc(params={
        'page': {'in': 'query', 'description': 'Page no','type':'int', 'default': 1},
        'per_page': {'in': 'query', 'description': 'Per page details','type':'int', 'default': 5},
        'book_id': {'in': 'query', 'description': 'Id of the book','type':'int'},
        'issue_date': {'in': 'query', 'description': 'Issue date of the book','type':'string','format':'date'},
        'student_id': {'in': 'query', 'description': 'Id of the student','type':'int'},
        'issued_by': {'in': 'query', 'description': 'Book issuer','type':'int'}
    })
    def get(self):
        if request.method=='GET':
            page = request.args.get('page',type=int)
            per_page = request.args.get('per_page',type=int)
            book_id = request.args.get('book_id',type=int)
            issue_date = request.args.get('issue_date')
            student_id = request.args.get('student_id',type=int)
            issued_by = request.args.get('issued_by',type=int)
            return issue_books.issued_details_history(page,per_page,book_id,issue_date,student_id,issued_by)
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/librarian/send_emails', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Notification(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    # @ns.expect(issuebooks_model)
    def post(self):
        if request.method=='POST':
            return issue_books_subject.send_emails(request.json)
        message = "This method is not allowed here please use the 'POST' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    