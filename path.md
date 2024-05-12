## Path Parameters

The term "features" is more prevalent in machine learning and data science.
"factors" has a stronger association with statistics and social sciences.

TO DO: Update our [Industry Features Colab](https://colab.research.google.com/drive/1HJnuilyEFjBpZLrgxDa4S0diekwMeqnh?usp=sharing) to take data path parameters from [parameters.yaml](../../RealityStream/parameters.yaml) and run multiple models using -bkup.ipynb files. 

[Using our virtual environment](./) local Streamlit app.py run steps, the features dataset is merged with a 2-column "target" dataset on-the-fly using Pandas to avoid storing merged files.

We'll recognize two formats:

	python app.py [features] [target] [models]

The above 3 parameters can also reside in one yaml file called by:

	python app.py [parameters.yaml]

Example of parameters.yaml format:

	features: "industries"
		startyear: 2017
		endyear: 2021
	 	path: "https://raw.githubusercontent.com/ModelEarth/community-timelines/main/training/naics{naics}/US/counties/{year}/US-{state}-training-naics{naics}-counties-{year}.csv"
	targets: "bees"
	models: rbf"


Each target dataset will contain 2 columns.  
1. The location column with one of the following column names:  
Country (2-char), State (2-char), Fips (5-digits for state and county), Zip (5 char, 6 in China), or Voxel (2 char)
2. The "Target" column containing 1 or 0

Sample features and targets datasets will reside within the "input/[data]/features" and "input/[data]/targets" folders for each data source.

### About path name shortcuts

The parameters will have three versions: short ("bees"), medium ("input/bees/targets") and full ("input/bees/targets/bees-targets.csv").

Setting the models parameter to "all" would be the equivalent to "svc, rfc, lr, rbf, location-forest"
The default model will be "rbf" (Random Bits Forest) when blank.

**Parameter rules:**
If a slash / is in a parameter, treat it as a path.
If the file name is omitted from a path, append a file name.
For a target value of "bees" build the path "input/bees/targets/bees-targets.csv"
For a target value of "bees increase2024" build the path "input/bees/targets/bees-targets-increase2024.csv"

## Projects

1. Integrate XGBoost model Honglin created in Feature-Target Colab.
2. Add neural networks model CoLab.
3. Output features-importance reports for available models.
4. Formalize the Jupyter notebooks to convert them into a generalized pipeline, which takes different features and targets inputs.
5. Include industries-features-bkup.ipynb in the pipeline
6. Add startyear and endyear to parameters and Streamlit interface.
7. Maintain notes on how to run and update Streamlit interface locally.
8. Pull accuracy reports (from Ivy's yaml or json files) into one tabulator table for viewing. See our [tabulator sample page](../../data-pipeline/timelines/tabulator/) for merging within javascript.
9. Reuse report display process for other models
10. Push "toy" feature data from CoLabs directly to Github annually.

