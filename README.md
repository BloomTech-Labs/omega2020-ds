# Omega2020

You can find the project at [Omega2020 DS API](https://api.lambda-omega2020.com/)

## Contributors


|                                       [Rob Hamilton](https://github.com/rob1ham)                                        |                                       [Johana Luna](https://github.com/johanaluna)                                        |                                       [Hira Khan](https://github.com/Hira63S)                                        |                                       [Rudy Enriquez](https://github.com/RNEnriquez)                                        |               
| :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
|                      [<img src="https://i.imgur.com/HQryRZs.jpg" width = "200" />](https://github.com/)                       |                      [<img src="https://ca.slack-edge.com/T4JUEB3ME-ULJAKAQ66-88214d54e62a-512" width = "200" />](https://github.com/)                       |                      [<img src="https://www.dalesjewelers.com/wp-content/uploads/2018/10/placeholder-silhouette-male.png" width = "200" />](https://github.com/)                       |                      [<img src="https://www.dalesjewelers.com/wp-content/uploads/2018/10/placeholder-silhouette-female.png" width = "200" />](https://github.com/)                       
|                 [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/)                 |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/honda0306)             |           [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/Hira63S)            |          [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/RNEnriquez)          
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/rob1ham/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/) |




![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)

## Project Overview


[Trello Board](https://trello.com/b/vlvasPUF/labs19-omega2020)

[Product Canvas](https://www.notion.so/980697b5f8bf481db26a8dd57e393aeb?v=5fecee4136ae4e69b228b84f810610c2)

The Omega2020 DS API serves as the backbone for image processing and computer vision pipelines to enable a better experience of transferring analog paper Sudoku puzzles to a digital form.

[Deployed Front End](http://omega2020.netlify.com/)

### Tech Stack

Below is an annotated breakout of the Cloud Architecture for the Omega 2020 Solution. Each step is also explained below.

[<img src="https://raw.githubusercontent.com/Lambda-School-Labs/omega2020-ds/master/Omega2020%20-%20Annotated.png"/>](https://cloudcraft.co/view/7b1de017-7406-43f3-a54e-682fcdc7b28f?key=ZZYfXAD9cYsLAA_galrUGw)

(Black Arrow) - Standard Inflow of Data for uploading a Paper Sudoku Puzzle
(Orange Arrow) - Querying a Sudoku Puzzle String to solve.
(Green Arrow) - Responses to Front End

Data Pipeline:
1. Web Team's Front end Deployed on Netlify at Omega2020.netlify.com
2. Elastic Beanstalk endpoint, redirected from an HTTPS: hosted website.
3. Auto scales between 1-4 servers to be able to handle spikes in demand.
4. **(Black Arrow)** First entry point within the Flask App, posts the raw image to S3. 
**(Orange Arrow)** Passes Puzzle To Solver
5. After the raw image is uploaded, it goes the Image Processing Script. Cropping out the Sudoku Puzzle from the image background, and subdivides a Sudoku Puzzle to 81 cells, stored as a list of 81 Numpy Arrays. Each Numpy Array is 784 integers long, representing a 28x28 pixel image.
6. **(Orange Arrow)** With Digits Passed via GET request from front end, solver checks if submitted Sudoku Puzzle is valid, if valid, the solution is passed as well as forecasted difficulty. 
**(Green Arrow)** With predicted digits passed back from Sagemaker API Endpoint, solver checks if submitted Sudoku Puzzle is valid, if valid, the solution is passed as well as forecasted difficulty. 
7. Amazon API Endpoint called for Analysis. Acts as a handler between Flask App and Sagemaker back end.
8. Lambda Function receives URL metadata from the API Gateway, and transforms it into the Sagemaker format.
9. Amazon Sagemaker Scores the inbound predictions.
10. S3 Bucket is organized into different folders of Raw Images, Processed Images, Individual Sudoku Cells, 

Auxiliary Services:
A. AWS Ground Truth was used to initially bootstrap the training of our model where our team individually scored 5,000 digits from a Sudoku Puzzle Book.
B. The Sagemaker Train Function reads a specific folder in the S3 Bucket, and runs on a scheduled basis allowing **Omega2020 learns over time as more data is shared.**
C. Reference Puzzles generated from our scraper is pulled on request to the front end, organized by difficulty.

###  Models:

Sudoku Puzzle Difficulty Model:
##### To predict the difficulty level of a Sudoku we used a Logistic Regression that uses the result from the tracker after solve the puzzle to predict a level 

### Data Sources


-   [Reference Sudoku Puzzles Scraped](http://www.sudoku.org.uk/Daily.asp)
-   [Paper Sudoku Puzzles Processed](https://www.amazon.com/gp/product/1680524755/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
-   [MNIST](http://yann.lecun.com/exdb/mnist/)

### How to connect to the DS API

| route               | description                       |
|:----------------------------|:----------------------------------|
| `POST: /demo_file`              | With an image attached, the predicted digits, sudoku solution (if applicable), and puzzle difficulty (if applicable) |
| `GET: /solve?puzzle=*puzzle_string*`      | For submitted Sudoku String, returns sudoku solution (if applicable), and difficulty (if applicable) |
| `DEV ONLY /reset` | Drops Tables and reinitiates database. Use only in testing. |
| `/bulk_processing` | Batch Processing of images in raw_images folder in S3, useful for upates to image processing|
| `/train` | Submit all valid Sudoku Puzzles images (as numpy arrays) and predicted values to a validation S3 folder to be fed into Sagemaker Training |
| `/upload` | Simple HTML page to test image upload independent of front end (used for DS testing) |


### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

Sudoku Image Processing was developed with reference to: Sarthak Vajpayee's https://medium.com/swlh/how-to-solve-sudoku-using-artificial-intelligence-8d5d3841b872

Use your own Algorithim with AWS Sagemaker: https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms.html
AWS: Bring Your own Container: https://github.com/awslabs/amazon-sagemaker-examples/tree/master/advanced_functionality/scikit_bring_your_own/container

Call an Amazon SageMaker model endpoint using Amazon API Gateway and AWS Lambda: https://aws.amazon.com/blogs/machine-learning/call-an-amazon-sagemaker-model-endpoint-using-amazon-api-gateway-and-aws-lambda/

Help with Sudoku Solver Code: Peter Norvig, https://norvig.com/sudoku.html

Naked Twins Solver Technique Reference: http://hodoku.sourceforge.net/en/tech_naked.php


## Documentation

See [Backend Documentation](https://github.com/Lambda-School-Labs/omega2020-be) for details on the backend of our project.

See [Front End Documentation](https://github.com/Lambda-School-Labs/omega2020-fe) for details on the front end of our project.

