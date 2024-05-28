# RPA Challenge - Thoughtful Automation

## The Challengue

### The Source
- From one of this sites, we choose one:
    - https://apnews.com/
    - https://www.aljazeera.com/
    - https://www.reuters.com/
    - https://gothamist.com/
    - https://www.latimes.com/  (The one I chose)
    - https://news.yahoo.com/

### Input Parameters:
- Search Phrase
- News Category / Section / Topic
- Number of Months to Consider
    - 0 or 1: Only the current month
    - 2: Current and previous month
    - 3: Current and Two previous months
    - And so on ...


### Steps of The Process

Here the steps of the challenge and my progress in each of them are detailed.

1. **Open the site by the chosen link: [I chose https://www.latimes.com/]**
   - [x] Done
2. **Enter a phrase in the search field.**
   - [x] Done
3. **If possible select a news category/section/topic from the list of categories/sections/topics list.**
   - [x] Done
4. **Get the values of Title, Date and Description of the current new.**
   - [x] Done
5. **Store in an Excel File: [Title, Date, Description(if available), Picture Filename, Count of search phrases in the title and description, True or False, depending on whether the title or description contains any amount of money(Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD)]**
   - [x] Done
6. **Download the news picture and specify the file name in the Excel file**
7. **Follow steps 4-6 for all news that falls within the required time period**

### Another Considerations
1. **Please leverage pure Python**
   - [x] Done
2. **Please leverage pure Selenium (Via rpaframework without utilizing Robot Framework.)**
   - [x] Done (But I have some feedback from my own about the use of the RPA.Browser.Selenium library)
3. **Leverage GitHub (Create a repo on GitHub for the code and when adding the robot to Robocloud add it via the GitHub app integration.)**
   - [x] Done
4. **Focus on RPA skillsets, do not use APIs or Web Requests**
   - [🔲] Partially done (I used Requests to use BeautifulSoup and understand the html tree in some isolated cases where I could not find any way to execute a javascript or find the correct web element)
5. **Bonus (Have Fun)**
   - [x] Done (Suffered a little bit with a few things but I had fun at last)
6. **Robocorp Robot Name (Please name the organization your name or your company’s name, and the robot name your first and last name.)**
   - [🔲] Partially done (I think I partially did this, because the robot name is Challenge_RPA_William_Rodriguez, it contains my name but I dont know it that is ok or not)
7. **Quality code.**
   - [ ] Pending evaluation
8. **Resiliency.**
   - [ ] Pending evaluation
9. **Best practices**
   - [ ] Pending evaluation

## Project Structure

### General Architecture

The project is organized as follows:
- **/news_browser**: Contains the source code of the project.
    - **/news_browser/__init__.py**: Initializes the code
    - **/news_browser/browser.py**: Contains a class to manage the web browser for scraping news.
    - **/news_browser/excel_creator.py**: Contains a class to create Excel files from news data.
    - **/news_browser/my_logger.py**: Specifies the log configurations.
    - **/news_browser/news_scraper.py**: Contains a class to scrape news articles from a website using Selenium.
- **/tests**: Contains the unit tests. (Partially, not every function is tested)
    - **tests/automated_test.py** : Runs an automated test.
    - **tests/test_excel_creator.py** : Runs unitary tests for excel_creator.py functions.
    - **tests/test_utils.py** : Runs unitary tests for test_utils.py functions.
- **main.py**: The main of our process.

### Clases y Funciones

#### Clase `NombreDeClase1`
- **Descripción**: Esta clase se encarga de [descripción general de la clase].
- **Funciones**:
  - `funcion1`: Realiza [breve descripción de la función].
  - `funcion2`: Se encarga de [breve descripción de la función].

#### Clase `NombreDeClase2`
- **Descripción**: Esta clase gestiona [descripción general de la clase].
- **Funciones**:
  - `funcion3`: Realiza [breve descripción de la función].
  - `funcion4`: Se encarga de [breve descripción de la función].

### Decisiones de Diseño

- **Decisión 1**: Opté por usar [patrón de diseño/tecnología] debido a [razones].
- **Decisión 2**: Implementé [función/característica] de esta manera porque [razones].

## Possible Improvements or Suggestions/Feedback

Although the project meets most of the requirements, there are several areas that could benefit from additional improvements:

- **The use of a wrapper**: Although the use of a wrapper should simplify things, that is not the case (for me) with the RPA.Browser.Selenium library, which is strictly a wrapper, and most of the Selenium benefits is its simplicity of use, finding web elements via tag name, list or any other way to find it.

    This is of course something that only affects me as a developer, you can still try to use the wrapper, but it makes the interaction with the site more complicated than it is with pure Selenium or PLaywright.
    
- **Code refactoring**: As said, the use of a wrapper, which I didnt know to use entirely, made the code a little bit overcoded in some parts, there is a good example on the `news_browser/news_scraper.py` function, where I could iterate over a list of web elements, but could not find any way to extract the web element inside the current web element of the cycle (I know, WebElementception).

- **Test coverage**: Expand unit test coverage and add integration tests. I could not test the most complicated functions correctly, with a little bit more of time I could have, but I already took most time than I thought at first with all this code you guys are reading, so I did not test it entirely.

- **Documentation**: Complete and further detail the technical and user documentation. There is always space for improvement and maybe my way to document is not of your please, so it can or may have changes.

## Conclusions

This was pretty much a great challenge for me, took me more than I would have spected, but just because I had to refactor Selenium logic for this challenge, as I said, I am not an expert on RPA.Browser.Selenium even if I have user Robocorp for more than 3 years now, but being a wrapper, it is not a library of my choice when coding.

I had a good time but I also put a good amount of time into trying to make the code correct, useful and usable, as well as well structured and readable.

Thanks for reading and hope you like the code :)
---