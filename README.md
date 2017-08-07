# alice-qg
Alice Question Generation System (AQG) is an automatic question generation system that is created for a virtual human's domain knowledge. The virtual human is from ARIA-VALUSPA project and it is called Alice. The initial AQG system was trained and tested by using Alice in Wonderland summaries. AQG uses Semantic Role Labeling (SRL) and Stanford Dependency to retrieve the semantic structure of the input text.

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
