# 42913_A3
Social and Information Network Analysis Assignment 3 Repository


## Instructions to use the prototype

* `pip install -r requirements.txt` to install all the packages

* The dataset can be downloaded from https://www.cc.gatech.edu/projects/doi/WebbSpamCorpus.html

* All the downloaded data folders need to be placed in `/data`

* First run `src/graph_creation.py` to create and save the graph files.
  **Note**: This takes about an hour to run due to the number of files to process.
  
* Then run `src/search_engine.py`. Running this will start a server 
  and POST requests can be sent to `localhost:8000/search`.
  The format for sending data is {"text": YOUR_SEARCH_TERM_HERE}.
