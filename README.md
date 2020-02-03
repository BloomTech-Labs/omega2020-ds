# Omega2020

You can find the project at [Omega2020 DS API](https://api.lambda-omega2020.com/)

## Contributors


|                                       [Rob Hamilton](https://github.com/rob1ham)                                        |                                       [Johana Luna](https://github.com/johanaluna)                                        |                                       [Hira Khan](https://github.com/Hira63S)                                        |                                       [Rudy Enriquez](https://github.com/RNEnriquez)                                        |                                       [Student 5](https://github.com/)                                        |
| :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
|                      [<img src="https://i.imgur.com/HQryRZs.jpg" width = "200" />](https://github.com/)                       |                      [<img src="https://www.dalesjewelers.com/wp-content/uploads/2018/10/placeholder-silhouette-female.png" width = "200" />](https://github.com/)                       |                      [<img src="https://www.dalesjewelers.com/wp-content/uploads/2018/10/placeholder-silhouette-male.png" width = "200" />](https://github.com/)                       |                      [<img src="https://www.dalesjewelers.com/wp-content/uploads/2018/10/placeholder-silhouette-female.png" width = "200" />](https://github.com/)                       |                      [<img src="https://www.dalesjewelers.com/wp-content/uploads/2018/10/placeholder-silhouette-male.png" width = "200" />](https://github.com/)                       |
|                 [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/)                 |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/honda0306)             |           [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/Mister-Corn)            |          [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/NandoTheessen)           |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/wvandolah)             |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/rob1ham/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/) |




![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)

## Project Overview


[Trello Board](https://trello.com/b/vlvasPUF/labs19-omega2020)

[Product Canvas](https://www.notion.so/980697b5f8bf481db26a8dd57e393aeb?v=5fecee4136ae4e69b228b84f810610c2)

The Omega2020 DS API serves as the backbone for image processing and computer vision pipelines to enable a better experience of transferring analog paper Sudoku puzzles to a digital form.

[Deployed Front End](http://omega2020.netlify.com/)

### Tech Stack

Tech Stack Diagram to be inserted here.


###  Models:

Sudoku Puzzle Difficulty Model:
##### To predict the difficulty level of a Sudoku we used a Logistic Regression that uses the result from the tracker after solve the puzzle to predict a level 

### Data Sources


-   [Reference Sudoku Puzzles Scraped] (http://www.sudoku.org.uk/Daily.asp)
-   [Paper Sudoku Puzzles Processed] (https://www.amazon.com/gp/product/1680524755/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
-   [MNIST] (http://yann.lecun.com/exdb/mnist/)

### How to connect to the DS API

🚫 List directions on how to connect to the API here

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

