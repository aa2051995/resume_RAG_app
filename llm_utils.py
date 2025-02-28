import ollama
import chromadb

# documents = [
#   "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
#   "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
#   "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
#   "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
#   "Llamas are vegetarians and have very efficient digestive systems",
#   "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
# ]
candidate_data = [
   {0: ' Diann Kupha Python Developer',
  3: ' Contact Details  diannkupha@gmail.com (938) 032 7933 North Arjun, 36142-1983, New Jersey',
  5: ' Summary Experienced Python Developer with 5+years of developing high- performance applications.Expertise in web frameworks,databases, and system integration.',
  6: ' Work Experience Python Developer,Marks,Miller and Runte March 2023 - Presen  Developed and maintained various Python applications using Flask, Django, and PostgreSQL  Implemented a suite of automated tests for a Python-based web application using Pytest. Developed a RESTful API using Python and the Flask microframework. Python Developer, Fritsch, Bashirian and Steuber May 2021- February 2023 Used Python to develop and optimize data pipelines for ETL processes. Utilized object-oriented programming and design patterns in Python to create efficient and maintainable solutions. Developed a GUI application using Python and TkInter.',
  2: ' Education Bachelor of Science in Computer Science with a Concentration in Python Programming University of California, Berkeley 2017-2021',
  1: ' Skills Object-Oriented - Expert Data Structures-Expert Web Development-Expert Machine Learning - Expert Automation - Expert Algorithms - Expert',
  4: ' References References available upon request'},
 {0: ' RACHELFRANK PYTHON DEVELOPER',
  5: ' SUMMARY I am a python developer, I am interested in Automation using python. I have Automotive domain knownledge and I have experience designing Test Automation Frameworks. I like to build smart application using Al and python',
  2: ' CONTACT  info@resumekraft.com 202-555-0120  Chicago,Illinois, US in linkedin.com/resumekraft',
  6: ' EXPERIENCE Senior Project Engineer Jan 2018-Present Wipro Technologies Working as a Python developer in Test-suite Scheduler Application. I have developed python package for HPALM functionality using REST APIs querry. Developed the recovery framework for Test Bench Crashes which has improved the TestBench Utilization for Software-Build Execution. Automated the JIRA Tasks such as Issue creation, Check for Duplicate Tickets. Developed Selenium python based automation framework for enabling CICD for Application Automated the task for finding any duplicate test cases in test rail which has resulted in decrease the manual effort and improved requirement-test case mapping Project Engineer Jul 2015- Dec 2017 Wipro Technologies  Developed the test scripts to test the infotainmnet system. Developed the Test Automation framework for Android-Auto, AppleCarplay, In_Vehicle-Software-Update Feature Testing.',
  -1: ' SKILLS 2015-06-05 C, Linux internals, micro processors, socket programming https://github.com/simple-stockpredictions/blob/master/Linear_models-',
  3: ' Python Automation Selenium C++programming Machine learning',
  4: ' TOOLS GITHUB TESTRAIL JIRA HPALM',
  1: ' EDUCATION Bachelor of Engineering Sep 2010-Jun 2014 San Jose State University',
  7: ' CERTIFICATION Embedded system Vector India PERSONAL PROJECTS',
  8: ' Stock Price Prediction SP.ipynb Credit card fraud detection https://github.com/Credit- CardFraud/blob/master/Credit_card_prediction.ipynb'},
 {0: ' JOHN GONALEZ Python Developer',
  1: ' CONTACT Pittsburgh,PA 9 (123)456-7890 john1652@gmail.com Linkedin n Github Q',
  2: ' CAREER OBJECTIVE Experienced Python developer with extensive Django experience looking to continue to develop my skill set on the back-end at a company driven to addressing the climate crisis.',
  7: ' WORK EXPERIENCE Python Developer DoorDash / September 2018 - current / Chicago IL Worked on building new Angular components for the customer- facing web app which improved the time on page for the average user by 2 minutes Worked within an agile team and helped prioritize and scope feature requests to ensure that the biggest impact features were worked on first Built extensive test coverage for all new features which reduced the number of customer complaints by 7%',
  5: ' EDUCATION M.S. Computer Science University of Chicago Chicago, IL / 2014 - 2016',
  6: ' B.S. Computer Science University of Pittsburgh Pittsburgh, PA /2010 -2014',
  8: ' Python Developer Knewton /April 2016-September 2018 / Pittsburgh PA Worked alongside another developer to implement RESTful APIs  in Django that enabled our internal analytics team to increase reporting speed by 24% Using Selenium built out a unit testing infrastructure for a client web application that reduced the number of bugs reported by the client by 11% month over month',
  3: ' SKILLS HTML/CSS SQL (PostgreSQL, Oracle) JavaScript (Angular) Python (Django) REST APIs (GraphQL) AWS (Redshift, S3) Git',
  4: ' PROJECTS Cryptocurrency Price Tracker Creator Incorporated API calls to several applications and stored data efficiently in in our PostgreSQL backend Utilized D3.js to allow users to dynamically visualize price movements over time periods of their choosing'},
 {0: ' Nadin Friedberger Phone number: 555-555-5555 Email address: hello@kickresume.com',
  -1: ' H N PROFILE SKILLS',
  8: ' Dynamic Certified Python Developer with 3 years of robust experience, demonstrating exceptional analytical and critical thinking skills. Recognized as Employee of the Year for proactive problem-solving, strong work ethic, and adeptness at thriving in high-pressure, deadline-oriented team settings.',
  4: ' WORK EXPERIENCE',
  9: ' Python Developer LUT Digital, Inc. 06/2017-06/2020 PASADENA,CA,UNITED STATES Developed web application back end components and facilitated client communication to identify needs and goals. Improved data protection and security measures, creating innovative user information solutions. Maintained large databases, configured servers, and collaborated with colleagues to reduce software maintenance expenses - achieved a 15% cost reduction within one year. Trained and supervised new employees,offering technical support to clients and coworkers. Recognized as the Employee of the Year for consistently meeting and exceeding all assigned goals and objectives.',
  6: ' EDUCATION',
  13: ' Computer Science California Institute of Technology 09/2013-05/2017PASADENA,CA,UNITED STATES Achieved a GPA of 3.96,ranking in the top 3% of the program. Engaged in various clubs and societies including Business Club, Engineering . Society,and TEDx Club.',
  18: " Gymnasium Brunchman High School 09/2009-05/2013BERLIN,GERMANY Completed Gymnasium with Distinction, achieving Grade 1 (A/excellent equivalent in all 4 subjects Received the 2012 Principal's Award for exceptional representation of the school at multiple Maths competitions Society,and Riding Club",
  15: ' Participated in Extracurricular Activities including Computer Club,Physics',
  10: ' LANGUAGES German Native',
  3: ' English Full',
  1: ' French Elementary',
  11: ' COMPUTER SKILLS Python .0... TestComplete 0',
  7: ' HTML, JavaScript ..... Appium',
  2: ' Selenium .....',
  5: ' STRENGTHS',
  12: ' # Ability to prioritize# Analytical # Communication # Critical thinking # Determination # Detail oriented # Problem-solving #Teamwork'},
 {0: ' Alexander Taylor Python Developer|Data Specialist @ help@enhancv.com linkedin.com  San Antonio, Texas',
  13: " SUMMARY Enthusiastic Python Developer with over two years' experience in HTML JavaScript,and web development.Skilled in fetching and cleaning data, building APls and web crawling. Seeking a challenging opportunity to utilize these skills and grow further in the field of data science.",
  2: ' STRENGTHS Critical Thinking Effectively used critical thinking to troubleshoot and solve challenging',
  -1: ' EXPERIENCE Junior Python Developer Web Developer Worked on web development projects using HTML and JavaScript. Gained Python skills on the job. CERTIFICATION 00000',
  4: ' Communication At Cognizant, successfully communicated technical data complications and helped the team to overcome them.',
  17: ' Cognizant 2019-2020 San Antonio,Texas Worked on HTML, JavaScript and Python development projects, with a focus on data fetching and cleansing. Developed Python scripts for Web Crawling and Web scraping resulting in 30% increased efficiency. Assisted in building APIs on top of cleaned data sets, which helped to automate data flow from multiple sources Worked on storing extracted data into SQL/No SQL data store.',
  5: ' Teamwork Collaborated with development team to deliver over 10 successful projects within given deadlines at Accenture.',
  1: ' SKILLS Python HTML JavaScript Web Scraping Regular expressions Crawling Data Cleansing SQL/NoSQL API Development',
  15: ' Accenture 2018-2019 San Antonio,Texas',
  14: ' interaction by 40%. Developed complex JavaScript functions to improve web page efficiency Automated HTML and CSS tasks by implementing preprocessor scripting Language, decreasing production time by 25%.',
  10: ' EDUCATION Master of Science in Computer Science University of Texas',
  8: ' Python for Data Science A specialized course conducted by Coursera that focused on Python development for data science applications.',
  7: ' Data Structures and Algorithms An intensive course offered by Udacity that targeted understanding of key data structures and algorithms.',
  9: ' Bachelor of Science in Computer Science Texas Tech University 2012-20169 Lubbock,Texas',
  3: ' PASSIONS 7 Coding Love for coding started in college and continued professionally, always exploring new development techniques.',
  12: ' LANGUAGES English 00000 Native',
  11: ' Spanish Intermediate'},
 {0: ' GIULIA GONZALEZ PYTHONDEVELOPER',
  2: ' CONTACT ggonzalez@email.com 123)456-7890 Detroit,MI Linkedin in Github ',
  6: ' WORK EXPERIENCE Python Developer DoorDash September 2017-current / Detroit,MI Worked on building new Angular components for the customer-facing web app,which improved the time on page for the average user by 2 minutes Collaborated with an agile team of 6,and helped prioritize and scope feature requests to ensure that the biggest impact features were worked on first Built extensive test coverage for all newfeatures,which reduced the number of customer complaints by 23% Acquired and ingested data to build and maintain data pipelines that led to discovering an opportunity for a new site feature, boosting revenue by 6% Communicated with internal teams and stakeholders,working to determine solutions for the user experience',
  -1: ' EDUCATION B.S. Python Developer Intern Pittsburgh, PA',
  3: ' M.S. Computer Science University of Chicago 2014-2016 Chicago,IL',
  4: ' Computer Science University of Pittsburgh 2010 - 2014',
  5: ' Knewton April 2016-April 2017/ Chicago,IL Worked alongside another developer to implement RESTful APIs in Django that enabled internal analytics team to increase reporting speed by 24% Using Selenium, built out a unit testing infrastructure for a client web application that reduced the number of bugs reported by the client by 11% month over month Provided project updates to leadership team of 3, and offered recommendations for design Diagnosed issues causing slow speeds in applications, and documented the process to making the database query system more robust Participated in writing scalable code with a team of 4 interns and 1 developer for applications for a math course',
  1: ' SKILLS HTML/CSS SQLPostgreSQL,Oracle) JavaScript (Angular) Python (Django) REST APIs (GraphQL) AWS (Redshift, S3) Git'}
]
client = chromadb.Client()
def create_cvs():
    collection = client.get_or_create_collection(name="cvs")
    for i,candidate in enumerate(candidate_data):
        t = ""
        for k,val in candidate.items():
            t += " "+val
        # t = (
        #        f"Name: {candidate['Name']}\n"
        #        f"Education: {candidate['Education']}\n"
        #        f"Work Experience: {candidate['Work_Experience']}\n"
        #        f"Skills: {candidate['Skills']}\n"
        #        f"Certifications: {candidate['Certifications']}\n"
        #        f"Additional Info: {candidate['Additional_Info']}\n"
        #    )
        response = ollama.embed(model="mxbai-embed-large", input=t)
        embeddings1 = response["embeddings"]
        # print(embeddings)
        collection.add(
            ids=[str(i)],
            embeddings=embeddings1,
            documents=[t]
        )
def retrieve(prompt):
    # prompt = "who know how to program in c++?"
    collection = client.get_collection('cvs')
    # generate an embedding for the input and retrieve the most relevant doc
    response = ollama.embed(
    model="mxbai-embed-large",
    input=prompt
    )
    results = collection.query(
    query_embeddings=response["embeddings"],
    n_results=3
    )
    data = results['documents']
    return data

# # store each document in a vector embedding database
# for i, d in enumerate(documents):
#   response = ollama.embed(model="mxbai-embed-large", input=d)
#   embeddings = response["embeddings"]
#   collection.add(
#     ids=[str(i)],
#     embeddings=embeddings,
#     documents=[d]
#   )