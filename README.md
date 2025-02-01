# aihack

Proposed solution to Use case Enedis: determining the tone and theme of media documents

Problem: Large numbers of documents are collected each month from the media that mention Enedis. These articles need to be evaluated based on their tone (positive, negative, factual, ...) by theme (network, HR, connection, clients, ...). Doing this my hand is time-comsuming. Enedis requests an AI tool to help automate this task.

Sentient Coders: Emma Blanchard - École 42, Martha Evonuk - École 42, Charles Herr - Telecom Paris, Zakaria Kaddaoui - CentraleSupélec) proposes the following solution.

![architechture](https://github.com/user-attachments/assets/4594bd5c-a8c2-41ec-8670-bdf8a78d21e5)

As shown in the achitechture, the solution is a web application, screenshots of which are shown below.

![Enedis Analyzer-multiple](https://github.com/user-attachments/assets/590fdcf9-e7bd-4e3c-ab45-0459060fa633)

![Enedis Analyzer-single](https://github.com/user-attachments/assets/1f3e0665-7030-4ad9-b315-41d062c6725f)

At the frontend, the user uploads the text to be analyzed; this information is then sent to AWS Bedrock where it is treated by the AI. The results of the analysis are then returned to the user on the frontend.

Options include single document analysis and multi document analysis.
