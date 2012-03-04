from django.db import connection

class DBRequests(object):
    def __init__(self):
        self.html = '''<div style="float:right; margin-right:10px">
            <p>[ {0} queries for {1} sec ]</p>
        </div>'''

    def process_response(self, request, response):
        content = response.content
        index = content.upper().find('</BODY>')
        print(index)
        if index == -1: 
            return response
        response.content = content[:index] + self.html.format(len(connection.queries), sum([float(query['time']) for query in connection.queries])) + content[index:]
        return response
