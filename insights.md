# Insights page

[Home](./index.md) ||
[BPMN Model](./bpmn.md) ||
[Use Case Model](./use_case.md) ||
[ETL Pipeline](./etl_pipeline.md) ||
[Insights](./insights.md) ||
[Team Contributions](./team_contrib.md) ||
[About](./about.md) ||

![visualization_sample](./assets/Visualization.png)

## Key insights gained from the project:

We understood the ETL process better while working on the code (Extract, Transform, and Load). At first, we just saw the overall picture and understood a bit by reading about it in English, but we gained more insights when we actually implemented the whole thing using Python, which is another language. This gave us a more cohesive understanding of the project. Reading and writing in different languages enhanced our understanding.

We also got a better grasp of data structures and mapping while working with JSON files and converting them into dictionaries. Our understanding deepened when we encountered errors while mapping and got stuck—it really emphasized the importance of understanding data structures across different APIs.

Another key insight came from checking our work in multiple places, like Postman, the Primary Care EHR server, and the code results. Seeing the same thing from different perspectives gave us a more comprehensive understanding of what we were doing.



## Challenges Encountered :

API Complexities 

Using Extensions for Hermes Terminology Server Links:  Identifying and correctly applying extensions for the Hermes Terminology Server links proved to be difficult.  The links for parent and child term was separate which was rectified during the projects with the help from professor. 

Data Inconsistencies:

Empty Fields in Primary Care EHR System:  During the data transfer from OpenEMR, we encountered empty fields in the Primary Care EHR system.

Data Compatibility Challenges:

SNOMED CT Values and String Input: In Task 2, SNOMED CT values required string inputs, but the data initially had numerical values.  We made adjustments to ensure compatibility and proper processing of the data by converting numerical values into string inputs.

## Lessons Learned:

ETL Pipeline Demonstration: A valuable demonstration for professional use involves querying and posting data to an API server using a single key, such as a patient ID or name. This demonstrates how data can be extracted and updated in real-time, making it relevant for day-to-day professional tasks.


## Potential Improvements:

Incorporate Automation and AI: Using machine learning algorithms for tasks like data validation, anomaly detection, or predictive analysis might significantly improve data accuracy and produce outcomes that are more insightful.


User-Centric Design: By adding features that place the user's experience first, including simple user interfaces or improved error reporting, the pipeline would be more useful in the real world.