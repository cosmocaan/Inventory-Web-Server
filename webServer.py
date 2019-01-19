#!/usr/bin/env python
'''
Name: Ryan Bailis
CSCI204 P1 Phase 2
Due: Spet. 26, 2018
'''

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from build import inventoryHTML
from build import *

HOSTNAME = ''       # where this program is running
HOSTPORT = 8080     # required port number, typically a value > 1024

form_text = ''       # the content will be generated
home_page = ''       # the content will be generated
home_url  = ''       # default URL will be generated

class Handler(BaseHTTPRequestHandler):
    """  The class handles a set of basic HTTP requests, such as GET and POST
    """

    def _set_headers(self):
        """  Send the OK response to a client, such as browser.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """     Service HTTP GET request from a client, such as a browser.
        """
        self._set_headers()

        global form_text
        global home_page

        ret_text = home_page + '\n' + form_text
        self.wfile.write(bytes(ret_text, 'utf-8'))


    def do_HEAD(self):
        """     Service HTTP HEAD request.
        """
        self._set_headers()
        
    def do_POST(self):
        """     Service HTTP POST request, typically a form request
        """
        self._set_headers()

        # print( "incomming http: ", self.path )

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        # print(post_data.decode('utf-8'))
        text = self.convert_code(post_data)    # convert all html code to text
    
        data = self.parse_form_data(text)       # create dictionary for data

    
        ret_text = '<p>' + home_url + '<p>'

        inven = inventoryHTML.Inventory() #create inventory object

        #check all pulldown field options created in form.html and stored in dictionary 'data'
        if data['pulldown'] == "num1": #user wants to print inventory
            if data['line'] != '': #user has defined a range of inventory items
                txt = data['line'].split(",")
                begin = int(txt[0])
                end = int(txt[1])
                ret_text += inven.print_inventory(begin,end)
            else: #user has not defined a range of inventory items
                ret_text += inven.print_inventory()
        elif data['pulldown'] == "num2": #user wants to compute the total worth of all inventory items
            ret_text += inven.compute_inventory()
        elif data['pulldown'] == "num3": #user wants to print a specific inventory category 
            ret_text += inven.print_category(data['line'])
        elif data['pulldown'] == "num4": #user wants to search the entire inventory for a specific keyword
            print("here")
            ret_text += inven.search_item(data['line'])
        
        self.wfile.write(bytes(ret_text,'utf-8'))

    def convert_code(self, post_data):
        """     Convert all html code into plain text, e.g., %2B -> +, + -> spc
        post_data is a bytearray. 
        """
        post_data = post_data.decode()  # the original post_data is byte array
        post_data = post_data.replace('+', ' ')   # convert '+' back to space
        orig_text = list(post_data)

        # The following loop converts HTML code back to plain text,
        # e.g., %2B to '+'
        new_text = ''
        i = 0
        while i < len(orig_text):
            if orig_text[i] != '%':
                new_text += orig_text[i]
                i += 1
            else:   # orig_text[i] == '%'
                code = orig_text[i+1] + orig_text[i+2]  # 2 char code, e.g., 2B
                new_text += bytearray.fromhex(code).decode() # %2B -> '+'
                i += 3
        return new_text

    def parse_form_data(self, text):
        """   Create dictionary for all form data. E.g,
        FirstInput=input+one&SecondInput=two+input&Submit=Submit
        will result in
        d['FirstInput'] = 'input+one'
        d['SecondInput'] = 'two+input'
        d['Submit'] = 'Submit'
        """
        d = {}
        l = text.split('&')
        for item in l:
            pair = item.split('=')
            d[pair[0]] = pair[1]
            # print(pair[0], ' === ', pair[1])
        return d

def generate_form(fname = './build/form.html'):
    """ Generate the form used by the page. The default form is stored in
    the file 'form.html'
    """
    f = None
    try:
        f = open(fname, 'r')
    except OSError:
        print('OSError')
        
    if f != None:      # read form text from the given file
        text = f.read()
    else:              # file doesn't exist, use default
        text = '<form method= "POST">\
        <input type="text" name="FirstInput" size = "20">\
        <font color="red">\
        Type input into the box</font><br>\
        <br>\
        <input type="text" name="SecondInput" size = "20">\
        <font color="green">\
        Type input into the box</font><br>\
        <br>\
        <font color = "yellow"> <input type="submit" name="Submit" value = "Submit">\
        </font><br>\
        <br>\
        </form>'
            
    return text

def generate_home_page(fname = './build/home.html'):
    """ Generate the home page. The default home page is stored in 'home.html'
    """
    f = None
    try:
        f = open(fname, 'r')
    except OSError:
        print('OSError')

    if f != None:    # read the home page from the given file
        text = f.read()
    else:
        text = '<center><h3>My Home Page</h3></center>\
               <p><em>Hello World!</em></p>'

    return text

def run(server_class=HTTPServer, handler_class=Handler, port=HOSTPORT):

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print(time.asctime(), "Server Starts - %s:%s" % (HOSTNAME, port))
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        HOSTPORT = int(argv[1])

    form_text = generate_form()
    home_page = generate_home_page()
    home_url  = '<a href = http://localhost:' + str(HOSTPORT) + '>Home</a>'

    run(port=HOSTPORT)

