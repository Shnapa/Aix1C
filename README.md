#### EffeTeX Analyzer

**EffeTeX Analyzer** is a simple web tool that allows users to enter a unit code and receive an automatic analysis using OpenAI.

##### What this project does
- The user enters a unit code on the webpage.
- The site sends the code to a backend server (Flask).
- The server uses the OpenAI API to generate a meaningful explanation or analysis of the code.
- The result is displayed on the page.


##### Technologies used
**Frontend**: HTML, CSS (Tailwind), JavaScript
**Backend:** Python, Flask
**AI:** OpenAI API


##### Requirements
Python 3.10 or higher
OpenAI API key in a .env file (OPENAI_API_KEY=...)
Internet connection

This tool was created for internal use at EffeTeX to quickly understand or interpret unit codes.
