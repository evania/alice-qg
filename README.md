# alice-qg
Alice Question Generation (AQG) is an automatic question generation system that is created for a virtual human's domain knowledge. The virtual human is from ARIA-VALUSPA project and it is called Alice. The AQG system is trained and tested by using Alice in Wonderland summaries. AQG uses Semantic Role Labeling (SRL) and Stanford Dependency to retrieve the semantic structure of the input text.

The main program is `aqg.py`. Run the main program by following the **instruction**. This main program generates QA pairs and stores them in an XML file. To do an error analysis on the generated QA, run the `categorized_csv.py`. This helps the analysis by categorizing and converting the generated QAs on neat CSV files.

`write_to_qamatcher.py` and `historysearch.py` are additional scripts to test the generated QA using a virtual-human domain-knowledge tool called QAMatcher (http://hmi.ewi.utwente.nl/).

## Instruction

1. Download and Install SENNA and PyStanfordDependency
Go to http://ml.nec-labs.com/senna/ to download and install SENNA. SENNA is used to provide the SRL. 
Go to https://pypi.python.org/pypi/PyStanfordDependencies to download and install PyStanfordDependency. PyStanfordDependency is used to parse the Stanford Dependency.

2. Run the SRL
Find the file "input.txt" under senna folder. Put the text input in this file. If there is more than one sentence, put the next sentences on the next lines and delete the full stops that exist on the sentences (it is usully not a problem, but in a few sentences this prevents SENNA to process the text). Also, delete quotation marks (") and hypens (-). Next, run the following command (or adjust it by checking out the SENNA website link again):
`./senna -srl < input.txt > output.txt`
That command will generate the SRL from the input, and save the result in output.txt

3. Prepare the AQG
On the first run, go to part "Running the Program - Create the Semantic Representation". Check for the comment "only for the first run" (around the line 708) and uncomment the line below it (the fetch and load function). In addition to that, comment the line that consists "RerankingParser.from_unified_model_dir".

4. Run the AQG
Run the AQG by using this command:
`python aqg.py`
