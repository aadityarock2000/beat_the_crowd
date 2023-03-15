## Setting up the project:

**Prerequisites:**
The project needs the user to have Microsoft SQL server in their machine where they intend to host/run the website. 

**Steps:**
1. Clone the repository
2. In the root folder, run the following commands to set up the project. <br> 
Windows:<br> 
py -m pip install --upgrade build<br> 
py -m build<br> 
Unix/macOS:<br> 
python3 -m pip install --upgrade build<br> 
python3 -m build
3. In the root folder, run the command `conda env create -f environment.yaml` to install all the required dependencies
4. Execute `stremalit run app.py` in the SmoothFly folder to launch the website and look at the analysis
5. To create the SQL Database, look at the pipeline_example.ipynb file in the examples doc to create the database and connect to your machine.
6. In the sql_parsing.py file in `SmoothFly/website_utils` path, edit the `connect_sql_server()` method, by adding in your server name.
7. Rerun using `streamlit run app.py` to look at the updated website, with the functionality to access the pipeline.
