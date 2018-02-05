### Requierments

- Python 3
- pip3
- virtualenv

### How to build and run the app
	
1. install virtualenv if you do not have it so far

	    pip3 install virtualenv

2. go to 

	    /project main directory

3. create virtualenv
        
        mkdir venv
        virtualenv venv

4. activate virtualenv

      on mac or linux : 
      
        . venv/bin/activate
	    
	  on windows: 
	    
	    venv\Scripts\activate.bat

5. install dependencies

		pip3 install -r requirements.txt
		
6. Run App

        python run.py
        
        or
        
        python3 run.py
        
      it depends which version of python is default, on my Windows machine 3 was default

### how to run tests

    python -m pytest
    
    or
    
    python3 -m pytest

### output / result

1. the raw scrapped files will be downloaded into 

        results/raw directory
        
2. the transformed csv file (which is the output of this app) with Soybean Condition report will be put into 

        results/cooked as soybean_condition_2016.csv file

### Notes

App is able to handle different years then 2016

But for now 2016 is hardcoded in usnass_app.py in reports_year variable for convenience
