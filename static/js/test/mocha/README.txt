How to test:

1. Start development server with python manage.py runserver.

2. Start server in project root on different port.  For example:
python -m http.server 8080
Note: 'static' folder should be directly underneath for step 3 to work.

3. Navigate to http://localhost:8080/static/js/test/mocha/runner/ in browser.

4. Open browser console to see results of test.
