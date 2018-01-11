from django.db import connection
class SqlPrintMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
	
    def __call__(self, request):
        response = self.get_response(request)
        sqltime = 0 # Variable to store execution time
        counter = 0
        # print('___________________________________________________________')
        for query in connection.queries:
            if query['sql'] != 'BEGIN':
                counter += 1
                print(query['sql'])
                sqltime += float(query["time"])  # Add the time that the query took to the total
                # print(query['time'])
                print('-----------------------------------------------------------')

        # # len(connection.queries) = total number of queries
        print('-----------------------------------------------------------')
        print("Page render: " + str(sqltime) + " sec for " + str(counter) + " queries")
        print('___________________________________________________________')
        print('___________________________________________________________')

        return response