## Easy start 
Just download PiEEG.zip, move to bundle folder, and launch PiEEG_app    

## Data details 
We save Raw data to allow researchers work with data without any limitations. 
Protocol has the next structure.   
<img src="https://github.com/pieeg-club/PiEEG/blob/main/images/protocol.bmp " alt="alt tag" title="aloha">

We use a bipolar voltage supply for PiEEG, so it is mean we should always check the first byte to detect the sign of voltage. 

Data visualisation from txt dataset from PiEEG app is [here](https://github.com/pieeg-club/PiEEG/blob/main/2.Software/Data_Processing/1.Data_visualisation.py)  

Our script that allows converting digital data to microvolts and saving it in Excel format is [here](https://github.com/pieeg-club/PiEEG/blob/main/2.Software/Data_Processing/2.Convert_data__save_excel.py)  


