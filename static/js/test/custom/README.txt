How to test:

1. Start development server with python manage.py runserver.

2. Start server in project root on different port.  For example:
python -m http.server 8080

3. Navigate to http://localhost:8080/static/js/test/custom/driver.html in browser.

4. Open browser console to see results of test.



This is a workaround until I can figure out a clean way to test ES6 modules with mocha unit tests in the browser.