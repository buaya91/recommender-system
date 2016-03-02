# README #
This application is a recommender system uses collaborative filtering

### How do I get set up? ###

* Summary of set up
Download the file, extract it
Run
`sudo python3 webserver.py` to start the server

Run
`sudo python3 webclient.py` to run the client, enter CustomerID and it will return a list of ProductCode for recommendations, default maximum is 5

* Configuration
To configure the maximum item to introduce, one can either modify `recommender.Recommender.recommend(self,name,number=5)` change the number=5 to any integer u want

As this recommender use knn, the k can be configure by modifying 'recommender.Recommender.__kneighbors__(self,name,k=5)` 

* Dependencies
This application depends on
    1. Numpy
    1. Scipy
    1. Pandas
    1. sklearn
